import socket
import httplib
import StringIO

import xml.dom.minidom
import urllib2
from urlparse import urlparse

from . import json_functions


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
        
        doc = xml.dom.minidom.parse(urllib2.urlopen(self.location))
        self.friendlyName = doc.getElementsByTagName("friendlyName")[0].firstChild.data
        
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
def find_kodi():
    kodi_dict = {}
    upnp_list = discover('upnp:rootdevice')

    for result in upnp_list:
        doc = xml.dom.minidom.parse(urllib2.urlopen(result.location))
        for modelName in doc.getElementsByTagName("modelName"):
            # Kodi
            if modelName.firstChild.data in ('XBMC Media Center', 'Kodi'):
                kodi_dict[urlparse(doc.getElementsByTagName("presentationURL")[0].firstChild.data).netloc] = doc.getElementsByTagName("friendlyName")[0].firstChild.data
                
            # Fire TV stick
            elif modelName.firstChild.data == 'AFTT':
                ip, port = result.location.split('/')[2].split(':')
                if json_functions.jsonrpc(method='JSONRPC.Ping', ip=ip, port='8080', timeout=5) == 'pong':
                    kodi_dict[ip] = json_functions.jsonrpc("XBMC.GetInfoLabels", {"labels": ["System.FriendlyName"]}, ip=ip, port='8080')['System.FriendlyName']

    return kodi_dict
