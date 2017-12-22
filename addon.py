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
    
    upnp_list = sorted(upnp.discover('upnp:rootdevice'), key=lambda x: x.friendlyName)
    upnp_string = '\n\n\n'.join(['{0}\n{1}\n{2}'.format(x.friendlyName, '-'*len(x.friendlyName), x.location) for x in upnp_list])
    xbmcgui.Dialog().textviewer('UPnP List', upnp_string)
