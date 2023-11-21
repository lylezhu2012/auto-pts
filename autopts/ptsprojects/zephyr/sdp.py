#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2017, Intel Corporation.
# Copyright (c) 2023, NXP.
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

"""SDP test cases"""
import binascii

from autopts.pybtp import btp
from autopts.pybtp.types import Addr, IOCap, AdType, AdFlags, Prop, Perm, UUID, UriScheme
from autopts.client import get_unique_name
from autopts.ptsprojects.stack import get_stack
from autopts.ptsprojects.testcase import TestFunc
from autopts.ptsprojects.zephyr.ztestcase import ZTestCase
from autopts.ptsprojects.zephyr.sdp_wid import sdp_wid_hdl

def set_pixits(ptses):
    """Setup SDP profile PIXITS for workspace. Those values are used for test
    case if not updated within test case.

    PIXITS always should be updated accordingly to project and newest version of
    PTS.

    ptses -- list of PyPTS instances"""

    pts = ptses[0]

    # Set SDP common PIXIT values
    pts.set_pixit("SDP", "TSPX_security_enabled", "FALSE")
    pts.set_pixit("SDP", "TSPX_delete_link_key", "FALSE")
    pts.set_pixit("SDP", "TSPX_bd_addr_iut", "DEADBEEFDEAD")
    pts.set_pixit("SDP", "TSPX_class_of_device_pts", "200404")
    pts.set_pixit("SDP", "TSPX_class_of_device_test_pts_initiator", "TRUE")
    pts.set_pixit("SDP", "TSPX_limited_inquiry_used", "FALSE")
    pts.set_pixit("SDP", "TSPX_pin_code", "0000")
    pts.set_pixit("SDP", "TSPX_time_guard", "200000")
    pts.set_pixit("SDP", "TSPX_device_search_time", "20")
    pts.set_pixit("SDP", "TSPX_use_implicit_send", "TRUE")
    pts.set_pixit("SDP", "TSPX_secure_simple_pairing_pass_key_confirmation", "FALSE")

    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern", "0100")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_no_results", "EEEE")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_additional_protocol_descriptor_list", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_bluetooth_profile_descriptor_list", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_browse_group_list", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_client_exe_url", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_documentation_url", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_icon_url", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_language_base_attribute_id_list", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_protocol_descriptor_list", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_provider_name", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_service_availability", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_service_data_base_state", "bddb")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_service_description", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_service_id", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_service_info_time_to_live", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_version_number_list", "1000")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_service_name", "")
    pts.set_pixit("SDP", "TSPX_sdp_service_search_pattern_service_record_state", "")
    pts.set_pixit("SDP", "TSPX_sdp_unsupported_attribute_id", "EEEE")

def test_cases(ptses):
    """Returns a list of SDP test cases
    ptses -- list of PyPTS instances"""

    pts = ptses[0]

    pts_bd_addr = pts.q_bd_addr

    iut_device_name = get_unique_name(pts)
    stack = get_stack()

    pre_conditions = [
        TestFunc(btp.core_reg_svc_gap),
        TestFunc(btp.core_reg_svc_l2cap),
        TestFunc(btp.core_reg_svc_sdp),
        TestFunc(stack.gap_init, iut_device_name),
        TestFunc(btp.gap_read_ctrl_info),
        TestFunc(lambda: pts.update_pixit_param(
            "SDP", "TSPX_bd_addr_iut",
            stack.gap.iut_addr_get_str())),
        TestFunc(lambda: pts.update_pixit_param(
            "SDP", "TSPX_delete_link_key", "TRUE")),

        # TestFunc(btp.core_reg_svc_gatt),
        # TestFunc(stack.gatt_init),
        TestFunc(btp.gap_set_io_cap, IOCap.keyboard_display),

        # We do this on test case, because previous one could update
        # this if RPA was used by PTS
        # TODO: Get PTS address type
        TestFunc(btp.set_pts_addr, pts_bd_addr, Addr.le_public),
        TestFunc(lambda: btp.gap_set_gendiscov()),
        ]

    custom_test_cases = []

    test_case_name_list = pts.get_test_case_list('SDP')
    tc_list = []

    for tc_name in test_case_name_list:
        instance = ZTestCase("SDP", tc_name,
                             cmds=pre_conditions,
                             generic_wid_hdl=sdp_wid_hdl)

        for custom_tc in custom_test_cases:
            if tc_name == custom_tc.name:
                instance = custom_tc
                break

        tc_list.append(instance)

    return tc_list
