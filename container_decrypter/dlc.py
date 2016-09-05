#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import base64
import logging
import re

import requests
from Crypto.Cipher import AES


class DLC:
    RC_REGEX = re.compile("<rc>(.*?)</rc>")
    URLS_REGEX = re.compile("<file>.*?<url>(.*?)</url>", re.DOTALL)
    NO_DATA_SUBMITTED = 'No data submitted'

    def __init__(self):
        self.b = "last09"
        self.p = "2009"
        self.v = "9.581"
        self.api = "http://service.jdownloader.org/dlcrypt/service.php"
        self.user_agent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.10) Gecko/2009042523 Ubuntu/9.04 (jaunty) Firefox/3.0.10"

    def decrypt(self, dlc):
        try:
            # call api and get response
            response = requests.post(self.api, data={'destType': 'jdtc5', 'b': self.b, 'p': self.p, 'srcType': 'dlc',
                                                     'data': dlc[-88:], 'v': self.v},
                                     headers={'User-agent': self.user_agent, 'Rev': self.v})
        except Exception as e:
            logging.error(e)
            return None

        content = response.content
        if self.NO_DATA_SUBMITTED in content:
            return None

        # decrypt dlc
        try:
            # get key1 from response
            key1 = content.splitlines()[1][4:]
            # decryption
            match = self.RC_REGEX.search(content)
            if match is None:
                logging.error("Invalid response received %s", content)
                return None
            key2 = base64.b64decode(match.group(1))
            if key2 is None:
                return None
            decryptor = AES.new(key1, AES.MODE_ECB)
            key3 = base64.b64decode(decryptor.decrypt(key2))
            if key3 is "":
                return None
            decryptor2 = AES.new(key3, AES.MODE_CBC, key3)
            f = decryptor2.decrypt(base64.b64decode(dlc[:-88]))
            content = base64.b64decode(f)
        except Exception as e:
            logging.error(e)
            return None

        return [base64.b64decode(x) for x in self.URLS_REGEX.findall(content)]
