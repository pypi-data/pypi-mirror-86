#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import queue

PATHS_ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
PATHS_POCS = os.path.join(PATHS_ROOT, "easy_pocs")
PATHS_OUTPUT = os.path.join(PATHS_ROOT, "output")
VERSION = "v0.1"

POCS = []
WORKER = queue.Queue()
CONF = {}

RESULTS=[]
