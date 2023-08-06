import os
from termcolor import cprint
import sys

try:
    import cvpoc
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from cvpoc.cv import verify_poc
from cvpoc import __version__
import logging

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
LOGO = """
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
# 版本号
VERSION = 'v%s' % __version__


class HiddenPrints:
    def __enter__(self):
        logging.disable(logging.CRITICAL)

        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

        self._original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.disable(logging.DEBUG)

        sys.stdout.close()
        sys.stdout = self._original_stdout

        sys.stderr.close()
        sys.stderr = self._original_stderr


def logo_banner():
    usage = LOGO + '''
                                                    %s
                                                    ''' % VERSION
    cprint(usage, "cyan")


def help_banner():
    usage = '''
                极光漏扫，所向披靡!
        opt:
        ---------------------------------------------------
        -h              Get help
        -t              Target
        -l              List avalible pocs
        -s              Search poc key words
        -m              Use poc module
        -f              Load urls file
        -d              set header Host name
        ---------------------------------------------------
        Usage:  
        1.python3 poc.py -l 列出所有poc
        2.python3 poc.py -t http://www.example.com 对url执行所有poc检测(暴力)
        3.python3 poc.py -t http://www.example.com -d baidu.com 对url执行所有poc检测(暴力,设置header)
        4.python3 poc.py -s thinkphp  搜索出thinkphp的相关poc
        5.python3 poc.py -s thinkphp -t http://www.example.com 单一目标执行漏洞检测(针对搜索到的poc)
        6.python3 poc.py -s thinkphp -t http://www.example.com -d baidu.com 单一目标执行漏洞检测(针对搜索到的poc,设置header)
        7.python3 poc.py -m thinkphp_rce2|thinkphp_rce2.py|绝对路径 -t http://www.example.com 单一目标执行漏洞检测
        8.python3 poc.py -m thinkphp_rce2|thinkphp_rce2.py|绝对路径 -t http://www.example.com -d baidu.com 单一目标执行漏洞检测（设置header）
        9.python3 poc.py -m thinkphp_rce2|thinkphp_rce2.py|绝对路径 -f url.txt(默认与该文件在同一目录)|绝对路径 对url.txt中的所有url执行漏洞检测 
        '''
    cprint(usage, "cyan")


def get_all_poc_list():
    # 列出所有poc名称
    poc_file1 = os.path.join(SITE_ROOT, 'easy_pocs')
    poc_file2 = os.path.join(SITE_ROOT, 'cv_pocs')
    poc_file3 = os.path.join(SITE_ROOT, 'pocsuite_pocs')
    poc_list = []
    for file_name in os.listdir(poc_file1):
        if file_name != '__init__.py' and file_name.endswith('.py'):
            poc_list.append(('easy_pocs', file_name))
    for file_name in os.listdir(poc_file2):
        if file_name != '__init__.py' and file_name.endswith('.py'):
            poc_list.append(('cv_pocs', file_name))
    for file_name in os.listdir(poc_file3):
        if file_name != '__init__.py' and file_name.endswith('.py'):
            poc_list.append(('pocsuite_pocs', file_name))
    return poc_list


def get_poc_files(poc):
    poc_file_list = []
    if os.path.isfile(poc):
        poc_file = poc
        if os.path.exists(poc_file):
            poc_file_list.append(poc_file)
    else:
        poc = poc.split('.py')[0] + '.py'
        current_path = os.getcwd()
        if os.path.exists(os.path.join(current_path, poc)):
            poc_file_list.append(os.path.join(current_path, poc))
        else:
            for k in ['easy_pocs', 'cv_pocs', 'pocsuite_pocs']:
                if os.path.exists(os.path.join(SITE_ROOT, k, poc)):
                    poc_file_list.append(os.path.join(SITE_ROOT, k, poc))
    if len(poc_file_list) == 0:
        cprint("-m 文件不存在或者文件路径不对", "red")
    return poc_file_list


def main():
    logo_banner()
    if len(sys.argv) < 2 or sys.argv[1] == "-h":
        help_banner()
    elif sys.argv[1] == "-l":
        # 列出所有poc名称
        poc_list = get_all_poc_list()
        cprint("total:", "blue")
        cprint(len(poc_list), 'red')
        cprint("=" * 30, "blue")
        for index, poc in enumerate(poc_list):
            cprint('%s-%s-%s' % (index + 1, poc[0], poc[1]), "red")
        cprint("=" * 30, "blue")
    elif len(sys.argv) >= 3 and sys.argv[1] == "-s" and sys.argv[2]:
        # 搜索相关的poc
        key = sys.argv[2].strip()
        # 列出所有poc名称
        poc_list = get_all_poc_list()
        if len(sys.argv) >= 5 and sys.argv[3] == '-t' and sys.argv[4]:
            target = sys.argv[4].strip()
            header = {}
            if len(sys.argv) >= 7 and sys.argv[5] == '-d' and sys.argv[6]:
                header = {'Host': sys.argv[5].strip()}

            count = 0
            for poc in poc_list:
                if key in poc[1]:

                    poc_file = os.path.join(SITE_ROOT, poc[0], poc[1])
                    config = {
                        'url': [target],
                        'poc': poc_file,
                    }
                    if header:
                        config['http_headers'] = header
                    with HiddenPrints():
                        try:
                            result = verify_poc(config)
                        except:
                            result = 'failed'

                    if result == 'success':
                        count += 1
                        cprint("%s-%s-%s" % (count, poc[0], poc[1]), 'yellow')
                        cprint("命中", "red")
            if count == 0:
                cprint("没有命中漏洞", "blue")
        else:
            count = 0
            for poc in poc_list:
                if key in poc[1]:
                    count += 1
                    cprint("%s-%s-%s" % (count, poc[0], poc[1]), 'yellow')

    elif len(sys.argv) >= 5 and sys.argv[1] == "-m" and sys.argv[3] == "-t":
        poc = sys.argv[2].strip()
        target = sys.argv[4].strip()
        poc_files = get_poc_files(poc)
        for poc in poc_files:
            config = {
                'url': [target],
                'poc': poc,
            }

            # 设置请求头 Host
            try:
                if sys.argv[5] == "-d" and sys.argv[6]:
                    config['http_headers'] = {'Host': sys.argv[5].strip()}
            except:
                pass

            cprint(poc, "yellow")
            with HiddenPrints():
                try:
                    result = verify_poc(config)
                except:
                    result = 'failed'

            if result == 'success':
                cprint("命中", "red")
            else:
                cprint("没有命中", "blue")
    elif len(sys.argv) >= 5 and sys.argv[1] == "-m" and sys.argv[3] == "-f":
        url_file = sys.argv[4].strip()
        poc = sys.argv[2].strip()

        poc_files = get_poc_files(poc)
        for poc in poc_files:
            cprint(poc, "yellow")
            try:
                with open(url_file, 'r') as f:
                    for line in f.readlines():
                        line = line.strip()
                        if not line:
                            continue
                        cprint(line, "green")

                        try:
                            link = line.split(' ')[0]
                            header = {'Host': link[1].strip()}
                        except:
                            header = {}

                        config = {
                            'url': [link],
                            'poc': poc,
                        }
                        if header:
                            config['http_headers'] = header
                        with HiddenPrints():
                            try:
                                result = verify_poc(config)
                            except:
                                result = 'failed'

                        if result == 'success':
                            cprint("命中", "red")
                        else:
                            cprint("没有命中", "blue")
            except FileNotFoundError:
                cprint("-f 文件不存在或者文件路径不对", "red")

    elif len(sys.argv) >= 3 and sys.argv[1] == '-t' and sys.argv[2]:
        target = sys.argv[2].strip()
        poc_list = get_all_poc_list()
        header = {}
        if len(sys.argv) >= 5 and sys.argv[3] == '-d' and sys.argv[4]:
            header = {'Host': sys.argv[5].strip()}
        count = 0
        for poc in poc_list:
            count += 1
            cprint("%s-%s-%s" % (count, poc[0], poc[1]), 'yellow')
            poc_file = os.path.join(SITE_ROOT, poc[0], poc[1])
            config = {
                'url': [target],
                'poc': poc_file,
            }
            if header:
                config['http_headers'] = header
            with HiddenPrints():
                try:
                    result = verify_poc(config)
                except:
                    result = 'failed'

            if result == 'success':
                cprint("命中", "red")
            else:
                cprint("没有命中", "blue")
    else:
        help_banner()


if __name__ == "__main__":
    main()
