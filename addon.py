import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import socket


# get the local IP address
# https://stackoverflow.com/a/25850698
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
local_ip_address = s.getsockname()[0]

xbmcgui.Dialog().ok('IP Address', local_ip_address)
