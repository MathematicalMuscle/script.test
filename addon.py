import xbmc
import xbmcgui

import sys

from resources.lib import get_external_ip_address
from resources.lib import get_local_ip_address
from resources.lib import jsonrpc_functions
from resources.lib import upnp


def menu():
    opts = ['Get local IP address',
            'Get external IP address',
            'Find Kodi systems',
            'Find Kodi systems (brute force)',
            'Find UPnP devices']
    
    select = xbmcgui.Dialog().select('TEST', opts, 0)
    if select >= 0:
        selection = opts[select]
        
        if selection == 'Get local IP address':
            local_ip_address = get_local_ip_address.get_local_ip_address()
            xbmcgui.Dialog().ok('Local IP Address', local_ip_address)

        elif selection == 'Get external IP address':
            external_ip_address = get_external_ip_address.get_external_ip_address()
            xbmcgui.Dialog().ok('External IP Address', external_ip_address)
        
        elif selection == 'Find Kodi systems':
            kodi_list = upnp.find_kodi()
            xbmcgui.Dialog().ok('Kodi List', '\n\n'.join([str(x) for x in kodi_list]))
            
        elif selection == 'Find Kodi systems (brute force)':
            kodi_list = upnp.find_kodi_brute_force()
            if kodi_list is not None:
                xbmcgui.Dialog().ok('Kodi List (brute force)', '\n\n'.join([str(x) for x in kodi_list]))
        
        elif selection == 'Find UPnP devices':
            upnp_list = sorted(upnp.discover('upnp:rootdevice'), key=lambda x: x.friendlyName)
            upnp_string = '\n\n\n'.join(['{0}\n{1}\n{2}'.format(x.friendlyName, '-'*len(x.friendlyName), x.location) for x in upnp_list])
            xbmcgui.Dialog().textviewer('UPnP List', upnp_string)
    

if __name__ == '__main__':
    if len(sys.argv) == 1:
        menu()
