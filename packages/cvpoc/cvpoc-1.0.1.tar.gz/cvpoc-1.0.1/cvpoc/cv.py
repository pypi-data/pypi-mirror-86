import sys
import os

try:
    import cvpoc
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from cvpoc.api import init_cvpoc
from cvpoc.api import start_cvpoc
from cvpoc.api import get_results

from cvpoc.easypoc.data import POCS, WORKER, CONF, RESULTS
from cvpoc.easypoc.loader import load_string_to_module
from cvpoc.easypoc.threads import run_threads
from cvpoc.easypoc.requests import patch_session, _disable_warnings


def init(config: dict):
    print("[*] target:{}".format(config["url"]))
    patch_session()
    _disable_warnings()
    with open(config.get('poc'), 'r') as f:
        model = load_string_to_module(f.read())
        POCS.append(model)
    CONF.update(config)


def worker():
    if not WORKER.empty():
        arg, poc = WORKER.get()
        try:
            ret = poc.verify(arg)
        except Exception as e:
            ret = None
            # print(e)
        if ret:
            ret = 'success'
        else:
            ret = 'failed'
        RESULTS.append({'status': ret})


def start():
    url_list = CONF.get("url", [])
    # 生产
    for arg in url_list:
        for poc in POCS:
            WORKER.put((arg, poc))
    # 消费
    run_threads(CONF.get("thread_num", 1), worker)


def verify_poc(config):
    poc_file = config.get('poc')
    with open(poc_file, 'r') as f:
        code = f.read()
    if 'pocsuite' in code or 'cvpoc' in code:
        init_cvpoc(config)
        start_cvpoc()
        result = get_results().pop()
        status = result.status

    else:
        init(config)
        start()
        result = RESULTS.pop()
        status = result.get('status', 'failed')

    return status
