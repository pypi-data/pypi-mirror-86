#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 上午10:49
# @Author  : chenghs
# @File    : console.py
import os
import sys

try:
    import cvpoc
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from cvpoc.cli import check_environment, module_path
from cvpoc import set_paths
from cvpoc.lib.core.interpreter import PocsuiteInterpreter
from cvpoc.lib.core.option import init_options


def main():
    check_environment()
    set_paths(module_path())
    init_options()
    poc = PocsuiteInterpreter()
    poc.start()


if __name__ == '__main__':
    main()
