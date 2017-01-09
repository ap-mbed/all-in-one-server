#!/usr/bin/env python

import sys, os
from MbedTools import MbedTools

print os.getcwd()

inst = MbedTools(sys.argv[1:])
inst.copy(True)
