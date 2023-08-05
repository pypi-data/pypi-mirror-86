#!/usr/bin/env python
## @package ca: EPICS-CA interface module for Python.
"""$Source: /opt/epics/R314/modules/soft/kekb/python/PythonCA-dev/ca.py $
CA modlue : EPICS-CA interface module for Python.
This module provide a  version of EPICS-CA and Python interface.
It users C module _ca. _ca module basically maps C-API in EPICS ca library into python. Interface between ca.py and _ca module is  subject for change. You should not depend on it. API in ca.py will be preserved in future releases as much as possible.
Author: Noboru Yamamoto, KEK, JAPAN. -2007.
Contoributors:
$Revision: b4d07ff54edb $
"""
#__version__ = "$Revision: b4d07ff54edb $"

import time,gc,sys,atexit
import threading
import sys
from sys import version_info

from epicsVersion import *

if (version_info >= (3,)):
    def printfn(x):
        print(x)
else:
    from printfn import printfn

try:
    from exceptions import ValueError
except:
    pass

try:
    import signal
except:
    printfn("signal module is not avaialble")

# force thread module to call PyEval_InitThread in it.
import threading
threading.Thread().start()
#import thread
#thread.start_new_thread(thread.exit_thread,()) 

import _ca
# version from _ca314.cpp
version=_ca.version
#__version__ = "$Revision: b4d07ff54edb $"%version
__version__ = "{version:s}".format(version=version)
revision=_ca.revision
release=_ca.release
hg_release=_ca.hg_release
ca_version=_ca.ca_version

# mercurial keyword. usr 'hg ci' and 'hg kwexpand' to update the following keywords
HGTag="$HGTag: 1.23.1.14-b4d07ff54edb $"
HGTagShort="$HGTagShort: 1.23.1.14 $"
HGdate="$HGdate: Sun, 20 May 2018 13:12:01 +0900 "
HGLastLog="$lastlog: pybuildvalue uses l for int $"
HGcheckedIn="$checked in by: Noboru Yamamoto <noboru.yamamoto@kek.jp> $"

# some constants for EPICS channel Access library
from cadefs import *
from caError import *

# for FNAL version you need to provide _ca_fnal.py and import everything from them
from _ca_kek import *
#
#from _ca_fnal import *
