import sys; reload(sys); sys.setdefaultencoding('utf-8')
import base64
import urllib2
import requests
import re

from cgi import escape
from HTMLParser import HTMLParser

from Crypto.Cipher import AES

def decrypt(dlc):
    """encrypts data in dlc. Based on pyload's
    pyload/module/plugins/container/DLC_27.pyc. Requires an active internet
    connection and is limited to a maximum API-calls per hour per IP."""

    b = "last09"
    p = "2009"
    v = "9.581"

    jdkey = []

    api = "http://service.jdownloader.org/dlcrypt/service.php"
    payload = {"destType": "jdtc5", "b": "last09", "p": "2009", "srcType": "dlc", "v": "9.581"}
    payload["data"] = dlc[-88:]
    dlcdata = base64.standard_b64decode(dlc[:-88])
    resp = requests.post(api, data=payload)
    rc = resp.content.split("<rc>", 1)[1].split("</rc>", 1)[0]
    jdkey = resp.content.splitlines()[1][4:]

    data = "destType=jdtc5&b=" + b + "&p=" + p + "&srcType=dlc&data=" + dlc[-88:] + "&v=" + v
    header = {'User-agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.10) Gecko/2009042523 Ubuntu/9.04 (jaunty) Firefox/3.0.10', 'rev': v}
    req = urllib2.Request(api, data, header)
    h = urllib2.urlopen(req)

    key2 = re.search("<rc>(.*?)</rc>", h.read()).group(1)
    key2 = base64.b64decode(key2)

    decryptor = AES.new(jdkey, AES.MODE_ECB)
    key3 = base64.b64decode(decryptor.decrypt(key2))

    decryptor2 = AES.new(key3, AES.MODE_CBC, key3)
    f = decryptor2.decrypt(base64.b64decode(dlc[:-88]))
    content = base64.b64decode(f)
     
    s = ""
    for x in re.findall("<file>.*?<url>(.*?)</url>", content, re.DOTALL):
        s = s + base64.b64decode(x)+","
    return s

