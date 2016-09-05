import sys; reload(sys); sys.setdefaultencoding('utf-8')
import base64
import urllib2
import requests
import re

from Crypto.Cipher import AES


class DLC:

    def __init__(self):
        self.b = "last09"
        self.p = "2009"
        self.v = "9.581"
        self.api = "http://service.jdownloader.org/dlcrypt/service.php";
        self.user_agent = "'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.10) Gecko/2009042523 Ubuntu/9.04 (jaunty) Firefox/3.0.10'";

    def decrypt(self,dlc):
        #get response for dlc
        try:
            #set the data
            data = "destType=jdtc5&b=" + self.b + "&p=" + self.p + "&srcType=dlc&data=" + dlc[-88:] + "&v=" + self.v
            header = {'User-agent' : self.user_agent, 'rev': self.v}
            #call api and get response
            req = urllib2.Request(self.api, data, header)
            h = urllib2.urlopen(req)
        except:
            return "400"

        #decrypt dlc
        try:
            #get the response
            resp = h.read()
            #get jdkey from response
            jdkey = resp.splitlines()[1][4:]
            #decryption
            key2 = re.search("<rc>(.*?)</rc>", resp).group(1)
            key2 = base64.b64decode(key2)
            decryptor = AES.new(jdkey, AES.MODE_ECB)
            key3 = base64.b64decode(decryptor.decrypt(key2))
            decryptor2 = AES.new(key3, AES.MODE_CBC, key3)
            f = decryptor2.decrypt(base64.b64decode(dlc[:-88]))
            content = base64.b64decode(f)
        except:
            return "500"
        #return the response
        s = ""
        for x in re.findall("<file>.*?<url>(.*?)</url>", content, re.DOTALL):
            s = s + base64.b64decode(x)+","
        return s