from cvpoc.thirdparty.colorama.initialise import init as coloramainit
import os
import sys
try:
    import cvpoc
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from cvpoc.cv import verify_poc

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))


def banner():
    msg = """
  /$$$$$$$ /$$    /$$ /$$$$$$   /$$$$$$   /$$$$$$$
 /$$_____/|  $$  /$$//$$__  $$ /$$__  $$ /$$_____/
| $$       \  $$/$$/| $$  \ $$| $$  \ $$| $$      
| $$        \  $$$/ | $$  | $$| $$  | $$| $$      
|  $$$$$$$   \  $/  | $$$$$$$/|  $$$$$$/|  $$$$$$$
 \_______/    \_/   | $$____/  \______/  \_______/
                    | $$                          
                    | $$                          
                    |__/                          
        """
    print(msg)


def run_cvpoc():
    banner()
    # 兼容pocsuite3(python3) ,兼容大部分pocsuite(python2)
    poc_file = os.path.join(SITE_ROOT, 'pocsuite_pocs', 'thinkphp_rce2.py')

    # 支持cvpoc(精简化pocsuite3)
    poc_file = os.path.join(SITE_ROOT, 'cv_pocs', 'thinkphp_rce2.py')

    # 支持easy_poc
    # poc_file = os.path.join(SITE_ROOT, 'easy_pocs', 'thinkphp2.py')
    config = {
        'url': ["http://117.48.133.72:8085/"],
        'poc': poc_file,
        'http_headers': {'Host': 'baidu.com'}
    }
    print(poc_file)
    verify_poc(config)


if __name__ == '__main__':
    run_cvpoc()
