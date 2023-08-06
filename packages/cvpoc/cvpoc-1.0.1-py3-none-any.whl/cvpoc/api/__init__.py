from cvpoc.lib.controller.controller import start
from cvpoc.lib.core.common import single_time_warn_message
from cvpoc.lib.core.data import conf, kb, logger, paths
from cvpoc.lib.core.datatype import AttribDict
from cvpoc.lib.core.enums import PLUGIN_TYPE, POC_CATEGORY, VUL_TYPE
from cvpoc.lib.core.option import init, init_options
from cvpoc.lib.core.plugin import PluginBase, register_plugin
from cvpoc.lib.core.poc import POCBase, Output
from cvpoc.lib.core.register import (
    load_file_to_module,
    load_string_to_module,
    register_poc,
)
from cvpoc.lib.core.settings import DEFAULT_LISTENER_PORT
from cvpoc.lib.request import requests
from cvpoc.lib.utils import get_middle_text, generate_shellcode_list, random_str
from cvpoc.modules.listener import REVERSE_PAYLOAD
from cvpoc.modules.spider import crawl
from cvpoc.modules.httpserver import PHTTPServer
from cvpoc.lib.core.interpreter_option import OptDict, OptIP, OptPort, OptBool, OptInteger, OptFloat, OptString, \
    OptItems, OptDict

__all__ = (
    'requests', 'PluginBase', 'register_plugin',
    'PLUGIN_TYPE', 'POCBase', 'Output', 'AttribDict', 'POC_CATEGORY', 'VUL_TYPE',
    'register_poc', 'conf', 'kb', 'logger', 'paths', 'DEFAULT_LISTENER_PORT', 'load_file_to_module',
    'load_string_to_module', 'single_time_warn_message',
    'PHTTPServer', 'REVERSE_PAYLOAD', 'get_listener_ip', 'get_listener_port',
    'get_results', 'init_cvpoc', 'start_cvpoc', 'get_poc_options', 'crawl',
    'OptDict', 'OptIP', 'OptPort', 'OptBool', 'OptInteger', 'OptFloat', 'OptString',
    'OptItems', 'OptDict', 'get_middle_text', 'generate_shellcode_list', 'random_str', "parse_output")


def parse_output(result):
    output = Output()
    if result.get('status') is True:
        output.success(result)
    else:
        output.fail('target is not vulnerable')
    return output


def get_listener_ip():
    return conf.connect_back_host


def get_listener_port():
    return conf.connect_back_port


def get_current_poc_obj():
    pass


def get_poc_options(poc_obj=None):
    poc_obj = poc_obj or kb.current_poc
    return poc_obj.get_options()


def get_results():
    return kb.results


def init_cvpoc(options={}):
    init_options(options)
    init()


def start_cvpoc():
    start()
