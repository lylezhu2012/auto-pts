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

import binascii
import logging
from time import sleep

import re

from autopts.wid import generic_wid_hdl
from autopts.ptsprojects.stack import get_stack
from autopts.pybtp import btp, defs
from autopts.pybtp.types import WIDParams, UUID, gap_settings_btp2txt, AdType, AdFlags, IOCap
from autopts.pybtp.types import L2CAPConnectionResponse

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

def hdl_wid_102(params: WIDParams):
    if params.test_case_name.startswith("GAP/IDLE/BON/BV-03-C") or params.test_case_name.startswith("GAP/IDLE/BON/BV-05-C"):
        btp.gap_set_io_cap(IOCap.no_input_output)
        btp.core_reg_svc_l2cap()
    elif params.test_case_name.startswith("GAP/IDLE/BON/BV-04-C") or params.test_case_name.startswith("GAP/IDLE/BON/BV-06-C"):
        btp.gap_set_io_cap(IOCap.display_yesno)
        btp.core_reg_svc_l2cap()
    else:
        btp.gap_set_io_cap(IOCap.keyboard_display)
    btp.gap_set_gendiscov()
    sleep(15)
    btp.gap_conn()
    btp.gap_wait_for_connection()
    if params.test_case_name.startswith("GAP/IDLE/BON/BV-04-C") or params.test_case_name.startswith("GAP/IDLE/BON/BV-06-C"):
        btp.l2cap_listen(psm=0x1001, transport=defs.L2CAP_TRANSPORT_BREDR, mtu=120, response=L2CAPConnectionResponse.insufficient_authentication)
    if not (params.test_case_name.startswith("GAP/IDLE/BON/BV-05-C") or params.test_case_name.startswith("GAP/IDLE/BON/BV-06-C")):
        btp.gap_pair()
    if params.test_case_name.startswith("GAP/IDLE/BON/BV-02-C"):
        btp.core_reg_svc_l2cap()
        btp.l2cap_listen(psm=0x1001, transport=defs.L2CAP_TRANSPORT_BREDR, mtu=120)
        btp.l2cap_conn(None, None, psm=0x1001,mtu=60)
    return True

def hdl_wid_105(_: WIDParams):
    btp.gap_set_conn()
    btp.gap_set_gendiscov()
    return True

def hdl_wid_146(_: WIDParams):
    btp.gap_start_discov(transport='bredr', discov_type='active', mode='general')
    return True

def hdl_wid_147(_: WIDParams):
    btp.gap_start_discov(transport='bredr', discov_type='active', mode='limited')
    return True

def hdl_wid_160(_: WIDParams):
    btp.gap_set_limdiscov()
    return True

def hdl_wid_164(_: WIDParams):
    return True

def hdl_wid_165(params: WIDParams):
    btp.gap_start_discov(transport='bredr', discov_type='active', mode='general')
    sleep(20)  # Give some time to discover devices
    # btp.gap_stop_discov()
    pts_name = re.findall(r'\'(.*)\'', params.description)
    if len(pts_name) > 0:
        pts_name = pts_name[0].encode('utf-8')
        pts_name = str(binascii.hexlify(pts_name)).lstrip('b\'').rstrip('\'').upper()
        return btp.check_scan_rep_and_rsp(pts_name, pts_name)
    else:
        return False

def hdl_wid_222(_: WIDParams):
    btp.gap_pair()
    return True

def hdl_wid_264(params: WIDParams):
    sleep(2)
    if params.test_case_name.startswith("GAP/IDLE/BON/BV-04-C") or params.test_case_name.startswith("GAP/IDLE/BON/BV-06-C"):
        pass
    else:
        btp.l2cap_listen(psm=0x1001, transport=defs.L2CAP_TRANSPORT_BREDR, mtu=120)
    btp.l2cap_conn(None, None, psm=0x1001,mtu=60)
    return True

def hdl_wid_2001(params: WIDParams):
    """
    The secureId is [passkey]
    """
    pattern = '[\d]{6}'
    passkey = re.search(pattern, params.description)[0]
    stack = get_stack()
    bd_addr = btp.pts_addr_get()
    bd_addr_type = btp.pts_addr_type_get()

    if stack.gap.get_passkey() is None:
        return False
    else:
        if "verify" in params.description:
            btp.gap_passkey_confirm_rsp(bd_addr, bd_addr_type, passkey)
        else:
            btp.gap_passkey_entry_rsp(bd_addr, bd_addr_type, passkey)
    return True