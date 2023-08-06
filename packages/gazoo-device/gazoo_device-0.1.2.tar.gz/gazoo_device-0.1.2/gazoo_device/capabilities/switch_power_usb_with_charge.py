# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Implementation of the switch_power_usb_with_charge capability."""
from gazoo_device import decorators
from gazoo_device import gdm_logger
from gazoo_device.capabilities import switch_power_usb_default

logger = gdm_logger.get_gdm_logger()

CHARGE = "charge"
OFF = "off"
SYNC = "sync"


class SwitchPowerUsbWithCharge(switch_power_usb_default.SwitchPowerUsbDefault):
    """Definition of the switch_power_usb_with_charge capability."""
    _REQUIRED_COMMANDS = ["SET_MODE", "GET_MODE"]
    _REQUIRED_REGEXS = ["GET_MODE_REGEX"]

    def __init__(self,
                 shell_fn,
                 regex_shell_fn,
                 command_dict,
                 regex_dict,
                 device_name,
                 serial_number,
                 total_ports):
        """Create an instance of the hub power with charge capability.

        Args:
            shell_fn (func): Function for calling shell on the device.
            regex_shell_fn (func): Function for calling shell_with_regex on the device.
            command_dict (dict): A dictionary containing the command used for each property.
                                 The dictionary must contain the following keys:

                                 - SET_MODE
                                 - GET_MODE

            regex_dict (dict): A dictionary containing the response regex to use to
                               determine the return value for the property.
                               The dictionary must contain the following keys:

                               - GET_MODE_REGEX

            device_name (str): name of the device this capability is attached to.
            serial_number (str): serial number of device this capability is attached to.
            e.g. {'OFF': 'off', 'POWER_ON': 'sync', 'POWER_CHARGE': 'charge'}
            total_ports (int): number of ports on device
        """
        super().__init__(shell_fn=shell_fn,
                         regex_shell_fn=regex_shell_fn,
                         command_dict=command_dict,
                         regex_dict=regex_dict,
                         device_name=device_name,
                         serial_number=serial_number,
                         total_ports=total_ports)

    @decorators.PersistentProperty
    def supported_modes(self):
        """Get the USB power modes supported by the USB hub."""
        return [OFF, SYNC, CHARGE]

    def get_mode(self, port):
        """Gets the USB mode for the specified port.

        Args:
          port (int): Use this port to get the mode.

        Returns:
            str: USB port mode settings
                 Example, 'off', 'sync', 'charge'

        Raises:
          GazooDeviceError: invalid port.
        """
        port = int(port)
        self._validate_port("get_mode", port)
        flags = self._regex_shell_fn(self._command_dict["GET_MODE"].format(port),
                                     self._regex_dict["GET_MODE_REGEX"],
                                     tries=5)
        if "O" in flags:
            mode = OFF
        elif "S" in flags:
            mode = SYNC
        else:
            mode = CHARGE
        return mode

    @decorators.CapabilityLogDecorator(logger, decorators.DEBUG)
    def power_off(self, port):
        """This command powers off the port specified.

        Args:
            port (int): Identifies which hub port to power off.
        """
        port = int(port)
        self._validate_port("power_off", port)
        self.set_mode(OFF, port)

    @decorators.CapabilityLogDecorator(logger, decorators.DEBUG)
    def power_on(self, port, data_sync=True):
        """This command powers on the port specified.

        Args:
            port (int): Identifies which hub port to power on.
            data_sync (bool): True if data should be enabled, false for power only
        """
        port = int(port)
        self._validate_port("power_on", port)
        if data_sync:
            self.set_mode(SYNC, port)
        else:
            self.set_mode(CHARGE, port)

    @decorators.CapabilityLogDecorator(logger, decorators.DEBUG)
    def set_mode(self, mode, port):
        """Sets the given USB port to the mode specified.

        Args:
          mode (str): USB mode to set. Options: 'off', 'sync', 'charge'
          port (int): The port to set.

        Raises:
          GazooDeviceError: invalid port, or mode.
        """
        port = int(port)
        self._validate_port("set_mode", port)
        self._validate_mode(mode)
        logger.debug("{} setting power mode to {} for usb port {}".
                     format(self._device_name, mode, port))
        self._shell_fn(self._command_dict["SET_MODE"].format(mode, port))
