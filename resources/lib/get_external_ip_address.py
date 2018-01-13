import re
import urllib


# https://github.com/tvaddonsco/plugin.program.indigo/blob/193fbe1ec09d738496d68458a5f900a749a121ec/default.py#L241
def get_external_ip_address():
    f = urllib.urlopen("http://www.canyouseeme.org/")
    html_doc = f.read()
    f.close()
    m = re.search('IP"\svalue="([^"]*)', html_doc)
    
    return m.group(1)
