import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

from resources.lib import get_local_ip_address
from resources.lib import upnp


if __name__ == '__main__':
    local_ip_address = get_local_ip_address.get_local_ip_address()
    xbmcgui.Dialog().ok('IP Address', local_ip_address)
    
    kodi_dict = upnp.find_kodi()
    xbmcgui.Dialog().ok('Kodi List', '\n\n'.join([str(x) for x in kodi_dict.items()]))
    
    upnp_list = upnp.discover('upnp:rootdevice')
    xbmcgui.Dialog().ok('UPnP List', '\n\n'.join([str(x) for x in upnp_list]))
