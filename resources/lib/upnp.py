import socket
import httplib
import StringIO

import xml.dom.minidom
import urllib2
from urlparse import urlparse

from . import get_local_ip_address
from . import jsonrpc_functions


# https://gist.github.com/dankrause/6000248
class SSDPResponse(object):
    class _FakeSocket(StringIO.StringIO):
        def makefile(self, *args, **kw):
            return self
            
    def __init__(self, response):
        r = httplib.HTTPResponse(self._FakeSocket(response))
        r.begin()
        self.location = r.getheader("location")
        self.usn = r.getheader("usn")
        self.st = r.getheader("st")
        self.cache = r.getheader("cache-control").split("=")[1]
        
        try:
            self.doc = xml.dom.minidom.parse(urllib2.urlopen(self.location))
            self.friendlyName = self.doc.getElementsByTagName("friendlyName")[0].firstChild.data
        except:
            self.doc = None
            self.friendlyName = '<Unknown>'
        
    def __repr__(self):
        return "<SSDPResponse({location}, {st}, {usn}, {friendlyName})>".format(**self.__dict__)
        


# https://gist.github.com/dankrause/6000248
def discover(service, timeout=5, retries=1, mx=3):
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}',
        'MAN: "ssdp:discover"',
        'ST: {st}','MX: {mx}','',''])
    socket.setdefaulttimeout(timeout)
    responses = {}
    for _ in range(retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(message.format(*group, st=service, mx=mx), group)
        while True:
            try:
                response = SSDPResponse(sock.recv(1024))
                responses[response.location] = response
            except socket.timeout:
                break
    return responses.values()


# https://github.com/jonisb/KodiEventGhost/blob/master/__init__.py
def find_kodi(timeout=2, port='8080'):
    local_ip_address = get_local_ip_address.get_local_ip_address()
    local_port = jsonrpc_functions.jsonrpc("Settings.GetSettingValue", {"setting":"services.webserverport"})['value']
    local_friendlyname = jsonrpc_functions.jsonrpc("XBMC.GetInfoLabels", {"labels": ["System.FriendlyName"]})['System.FriendlyName']
    kodi_dict = {'{0}:{1}'.format(local_ip_address, local_port): local_friendlyname}
    
    upnp_list = discover('upnp:rootdevice', timeout=timeout)
    for result in upnp_list:
        if result.doc:
            for modelName in result.doc.getElementsByTagName("modelName"):
                # Kodi
                if modelName.firstChild.data in ('XBMC Media Center', 'Kodi'):
                    kodi_dict[urlparse(result.doc.getElementsByTagName("presentationURL")[0].firstChild.data).netloc] = result.friendlyName
                    
                # Fire TV stick
                elif modelName.firstChild.data == 'AFTT':
                    ip = result.location.split('/')[2].split(':')[0]
                    if jsonrpc_functions.jsonrpc(method='JSONRPC.Ping', ip=ip, port=port, timeout=1) == 'pong':
                        kodi_dict['{0}:{1}'.format(ip, port)] = jsonrpc_functions.jsonrpc("XBMC.GetInfoLabels", {"labels": ["System.FriendlyName"]}, ip=ip, port=port)['System.FriendlyName']

    return sorted(kodi_dict.items(), key=lambda x: x[0])


def find_kodi_brute_force(timeout=1, port='8080'):
    try:
        from multiprocessing.dummy import Pool
    
        ip_mask = '.'.join(get_local_ip_address.get_local_ip_address().split('.')[:3])
        pool = Pool(255)
        ping_list = pool.map(lambda x: ('{0}.{1}'.format(ip_mask, x), jsonrpc_functions.jsonrpc("JSONRPC.Ping", ip='{0}.{1}'.format(ip_mask, x), port=port, timeout=timeout)), range(256))
        pool.close()
        pool.join()
        
        kodi_list = [('{0}:{1}'.format(x[0], port), jsonrpc_functions.jsonrpc("XBMC.GetInfoLabels", {"labels": ["System.FriendlyName"]}, ip=x[0], port=port)['System.FriendlyName']) for x in ping_list if x[1] == 'pong']
        return kodi_list
        
    except:
        import xbmcgui
        xbmcgui.Dialog().ok('`find_kodi_brute_force()`', 'Could not import `multiprocessing.dummy`')
        return None
