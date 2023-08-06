#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
from importlib.abc import Loader
from importlib.util import spec_from_file_location, module_from_spec


def get_md5(value):
    if isinstance(value, str):
        value = value.encode(encoding='UTF-8')
    return hashlib.md5(value).hexdigest()


def load_string_to_module(code_string, fullname=None):
    try:
        module_name = 'cvpocs_{0}'.format(get_md5(code_string)) if fullname is None else fullname
        file_path = 'cvpoc://{0}'.format(module_name)
        poc_loader = PocLoader(module_name, file_path)
        poc_loader.set_data(code_string)
        spec = spec_from_file_location(module_name, file_path, loader=poc_loader)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    except ImportError:
        error_msg = "load module '{0}' failed!".format(fullname)
        print(error_msg)
        raise


class PocLoader(Loader):
    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path
        self.data = None

    def set_data(self, data):
        self.data = data

    def get_filename(self, fullname):
        return self.path

    def get_data(self, filename):
        if filename.startswith('cvpoc://') and self.data:
            data = self.data
        else:
            with open(filename, encoding='utf-8') as f:
                data = f.read()
        return data

    def exec_module(self, module):
        filename = self.get_filename(self.fullname)
        poc_code = self.get_data(filename)
        obj = compile(poc_code, filename, 'exec', dont_inherit=True, optimize=-1)
        exec(obj, module.__dict__)
