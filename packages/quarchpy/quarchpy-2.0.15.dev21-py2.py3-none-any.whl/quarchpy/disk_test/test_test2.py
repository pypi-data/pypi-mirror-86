from abc import ABC

import time
import sys
import os
import logging

from quarchpy.disk_test.Drive_wrapper import DriveWrapper
from quarchpy.disk_test.base_test import BaseTest
from quarchpy.disk_test.driveTestCore import specifyQuarchModule, DiskStatusCheck, checkDriveState, update_progress_bars
from quarchpy.disk_test.hostInformation import HostInformation


class Full_Range_HotPlugTest(BaseTest):
    def __init__(self):
        # run super.init after declaration of variables so it can request the variables needed
        super(Full_Range_HotPlugTest, self).__init__()

        self.my_host_info = HostInformation()

        # Declare custom variables for the test
        self.cv_repeats = self.declare_custom_variable(custom_name="repeats", default_value=1,
                                                       description="Number of times to repeat each hotplug")
        self.cv_ontime = self.declare_custom_variable(custom_name="onTime", default_value=15,
                                                      description="Time to wait for drive to enumerate on host")
        self.cv_offtime = self.declare_custom_variable(custom_name="offTime", default_value=10,
                                                       description="Time to wait for host to remove drive")
        self.cv_linkspeed = self.declare_custom_variable(custom_name="linkspeed", default_value="auto",
                                                         description="Value to compare drive's link speed, GB/s",
                                                         accepted_vals=['2.5GT/s', '5GT/s', '8GT/s', '16GT/s', '32GT/s',
                                                                        'auto'])
        self.cv_landwidth = self.declare_custom_variable(custom_name="lanewidth", default_value="auto",
                                                         description="Value to compare drive's lane width",
                                                         accepted_vals=['x1', 'x2', 'x4', 'x8', 'x16', 'x32', 'auto'])

        # Declare additional variables that may not be visible to the user by default
        # Should custom variables have a custom unit, like "ms"?  This may be easier than parsing strings
        self.cv_drivename = self.declare_custom_variable(custom_name="driveName", default_value="drive1",
                                                         var_purpose="internal")
        self.cv_quarchname = self.declare_custom_variable(custom_name="quarchName", default_value="module1",
                                                          var_purpose="internal")
        self.cv_inserttime = self.declare_custom_variable(custom_name="insertTime",
                                                          default_value=[25, 10, 50, 75, 100, 250, 500, 1000, 5, 0],
                                                          var_purpose="internal")

    def check_prerequisites(self, document_mode=False):
        # need the standard imports
        super(Full_Range_HotPlugTest, self).check_prerequisites()

    def start_test(self, document_mode=False):

        # Had to move this here as init is now called without a document mode parameter
        self._set_documentation_mode(document_mode)

        self.test_id.reset()

        #############################
        # SETUP
        #############################

        # Start object
        self.test_point(self.test_id.gen_next_id(), test_description="Setting up required test resources")
        self.test_id.up_tier(singular=True)

        # ID = 0.1
        self.cv_quarchname.custom_value = self.select_quarch_module(filter_module="drive")

        if not self.cv_quarchname.custom_value:
            self.comms.send_stop_test(reason="No Quarch Module Selected")
            return

        # ID = 0.2
        self.cv_drivename.custom_value = self.select_drive()

        if not self.cv_drivename.custom_value:
            self.comms.send_stop_test(reason="No Drive Selected")
            return

        ##############################
        # TEST - Core
        ##############################

        # ID 1.0
        self.test_id.down_tier(singular=True, description="Beginning tests core")

        for item in self.cv_inserttime.default_value:
            # ID = 1.1
            self.test_id.up_tier(
                description=str(item) + "mS Staged hot-plug test, with enumeration and link verification",
                singular=True)

            for loop in range(0, int(self.cv_repeats.custom_value)):
                self.test_id.up_tier(description="Repeat cycle " + str(int(loop) + 1) + " of " +
                                                 str(self.cv_repeats.custom_value))

                # ID = 1.1.1
                # why is this calling custom_value.index(x) instead of custom_value[x]?
                # If this iterates through four different insert times, shouldn't there be:
                # for delay_time in self.cv_inserttime.custom_value: ...
                self.test_point(self.test_id.gen_next_id(), function_description="Setting up hotplug test",
                                function=self.setup_simple_hotplug,
                                function_args={'delay_time': str(item),
                                               'step_count': 6})

                # ID = 1.1.2
                self.test_point(self.test_id.gen_next_id(),
                                function_description="hotplug_" + str(item) + "ms_delay, cycle " + str(loop))
                # Debug Item
                self.test_point(function=self._add_quarch_command,
                                function_args={"command": "run:power down",
                                               "quarch_device": self.cv_quarchname.custom_value})

                # Wait and check for drive
                enum_time = self.test_point(self.test_id.gen_next_id(), function=self.test_wait_for_enumeration,
                                            has_return=True,
                                            function_description="Polling system for indication of drive removal",
                                            function_args={'enumeration': False,
                                                           "drive": self.cv_drivename.custom_value,
                                                           "ontime": self.cv_ontime.custom_value,
                                                           "offtime": self.cv_offtime.custom_value})

                # ID = 1.1.3
                self.check_point(self.test_id.gen_next_id(),
                                 description="Checking device not enumerated when powered down",
                                 function=DiskStatusCheck,
                                 function_args={'driveId': self.cv_drivename.custom_value, 'expectedState': 0})

                # Debug Item
                self.test_point(function=self._add_quarch_command,
                                function_args={"command": "run:power up",
                                               "quarch_device": self.cv_quarchname.custom_value})

                enum_time = self.test_point(self.test_id.gen_next_id(), function=self.test_wait_for_enumeration,
                                            has_return=True,
                                            function_description="Polling system for indication of drive insertion",
                                            function_args={'enumeration': True, "drive": self.cv_drivename.custom_value,
                                                           "ontime": self.cv_ontime.custom_value,
                                                           "offtime": self.cv_offtime.custom_value})

                self.check_point(self.test_id.gen_next_id(), description="Checking device enumerated after power up",
                                 function=DiskStatusCheck, has_return=True,
                                 function_args={'driveId': self.cv_drivename.custom_value, 'expectedState': 1})

                self.check_point(self.test_id.gen_next_id(), description="Checking device's reported link speed",
                                 function=self.test_check_link_speed,
                                 function_args={"drive": self.cv_drivename.custom_value,
                                                "quarch_module": self.cv_quarchname.custom_value,
                                                "link_speed": self.cv_linkspeed.custom_value})

                self.check_point(self.test_id.gen_next_id(), description="Checking device's reported lane width",
                                 function=self.test_check_lane_width,
                                 function_args={"drive": self.cv_drivename.custom_value,
                                                "quarch_module": self.cv_quarchname.custom_value,
                                                "lane_width": self.cv_landwidth.custom_value})

                self.test_id.down_tier()
            self.test_id.down_tier(singular=True)
        # resetting the quarch-module to ensure it's not locked for next connection
        self._close_connection()

    def _close_connection(self):
        if not self.document_mode:
            self.cv_quarchname.custom_value.closeConnection()
        else:
            return

    def setup_simple_hotplug(self, delay_time, step_count):

        command_success = True
        # need to re-examine
        # delay_time = int(delay_time)
        # step_count = int(step_count)
        #
        # # Check parameters
        # if int(delay_time) < 0:
        #     # Currently asks test to stop. Could be changed to request new value
        #     comms.sendMsgToGUI(comms.send_gui_request(req_type="error", request_string="Stop"))
        #     logging.error("Invalid delay_time for hotplug setup")
        #     return False
        #
        # if step_count < 2 or step_count > 6:
        #     # Currently asks test to stop. Could be changed to request new value
        #     comms.sendMsgToGUI(comms.send_gui_request(req_type="error", request_string="Stop"))
        #     logging.error("Invalid step_count for hotplug setup")
        #     return False

        # Run through all 6 timed sources on the module
        for steps in range(1, 6):
            # Calculate the next source delay. Additional sources are set to the last value used
            if steps <= step_count:
                next_delay = (int(steps) - 1) * int(delay_time)

                if not self.test_point(function=self._add_quarch_command,
                                       function_args={
                                           "command": "source:" + str(steps) + ":delay " + str(int(next_delay)),
                                           "quarch_device": self.cv_quarchname.custom_value}):
                    command_success = False

        return command_success



