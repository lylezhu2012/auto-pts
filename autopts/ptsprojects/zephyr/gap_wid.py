#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2017, Intel Corporation.
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

import logging
from time import sleep

from autopts.wid import generic_wid_hdl
from autopts.ptsprojects.stack import get_stack
from autopts.pybtp import btp, defs
from autopts.pybtp.types import WIDParams, UUID, gap_settings_btp2txt, AdType, AdFlags, IOCap

log = logging.debug


def gap_wid_hdl(wid, description, test_case_name):
    log(f'{gap_wid_hdl.__name__}, {wid}, {description}, {test_case_name}')
    return generic_wid_hdl(wid, description, test_case_name, [__name__, 'autopts.wid.gap'])


def hdl_wid_104(_: WIDParams):
    return True


def hdl_wid_114(_: WIDParams):
    return True


def hdl_wid_162(_: WIDParams):
    return True


def hdl_wid_224(_: WIDParams):
    return True

# Please make IUT not discoverable. Press OK to continue.
def hdl_wid_31(_: WIDParams):
    btp.gap_set_nonconn()
    return True

def hdl_wid_32(_: WIDParams):
    btp.gap_set_limdiscov()
    return True

def hdl_wid_33(params: WIDParams):
    if params.test_case_name.startswith("GAP/MOD/NBON/BV-03-C"):
        btp.gap_set_io_cap(IOCap.no_input_output)
    if params.test_case_name.startswith("GAP/SEC/SEM/BV-02-C"):
        btp.gap_set_io_cap(IOCap.keyboard_display)
        btp.core_reg_svc_l2cap()
        btp.l2cap_listen('0x1001', defs.L2CAP_TRANSPORT_BREDR, 120)
    btp.gap_set_gendiscov()
    return True

def hdl_wid_34(_: WIDParams):
    btp.gap_set_nonconn()
    return True

def hdl_wid_145(_: WIDParams):
    timeout = 0
    while True:
        stack = get_stack()
        if not stack.gap.current_settings_get(
            gap_settings_btp2txt[defs.GAP_SETTINGS_DISCOVERABLE]):
            return True
        else:
            sleep(5)
            timeout += 5
        if timeout >= 60:
            break
    return False

def hdl_wid_105(_: WIDParams):
    btp.gap_set_conn()
    btp.gap_set_gendiscov()
    return True

def hdl_wid_160(_: WIDParams):
    btp.gap_set_limdiscov()
    return True

def hdl_wid_222(_: WIDParams):
    btp.gap_pair()
    return True
