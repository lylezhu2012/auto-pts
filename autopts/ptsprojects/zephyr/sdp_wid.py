#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2017, Codecoup Corporation.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#


import binascii
import logging
import threading
from threading import Lock, Timer, Event
from time import sleep

import re

from autopts.wid import generic_wid_hdl
from autopts.ptsprojects.stack import get_stack
from autopts.pybtp import btp, defs
from autopts.pybtp.types import WIDParams, UUID, gap_settings_btp2txt, AdType, AdFlags, IOCap
from autopts.pybtp.types import L2CAPConnectionResponse

log = logging.debug

def sdp_wid_hdl(wid, description, test_case_name):
    log(f'{sdp_wid_hdl.__name__}, {wid}, {description}, {test_case_name}')
    return generic_wid_hdl(wid, description, test_case_name, [__name__, 'autopts.wid.sdp'])

# wid handlers section begin
def hdl_wid_1(_: WIDParams):
    return True

def hdl_wid_6000(_: WIDParams):
    return True

def hdl_wid_6001(_: WIDParams):
    return True

def hdl_wid_6002(_: WIDParams):
    return True

def hdl_wid_6003(_: WIDParams):
    return True