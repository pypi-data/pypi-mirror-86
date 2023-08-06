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

"""Fire Manager module.

Used for GDM CLI-specific commands and flags. Built to work with Python Fire.
"""
import codecs
import enum
import inspect
import json
import logging
import os.path
import pydoc
import re
import sys
import textwrap
import time
from gazoo_device import config
from gazoo_device import decorators
from gazoo_device import errors
from gazoo_device import manager
from gazoo_device import gdm_logger
from gazoo_device import testbed
from gazoo_device.utility import parallel_utils
from gazoo_device.utility import usb_utils

logger = gdm_logger.get_gdm_logger()


class AttributeClassification(enum.Enum):
    """Types of class attributes recognized by GDM's "man" method."""
    CAPABILITY = "capability"
    DEPRECATED_METHOD = "deprecated method"
    DEPRECATED_PROPERTY = "deprecated property"
    HEALTH_CHECK = "health check"
    OTHER = "other"
    PRIVATE_METHOD = "private method"
    PROPERTY = "property"
    CLASS_PROPERTY = "class property"
    PUBLIC_METHOD = "public method"


HEALTHY_DEVICE_HEALTH = {
    "is_healthy": True,
    "unhealthy_reason": "",
    "err_type": "",
    "checks_passed": [],
    "properties": {}
}
MAX_TIME_TO_WAIT_FOR_INITATION = 5

_DOC_INDENT_SIZE = 4
# Capability attributes visible on device summary man page (such as "man cambrionix").
_VISIBLE_CAPABILITY_ATTRIBUTES = [AttributeClassification.PROPERTY,
                                  AttributeClassification.PUBLIC_METHOD]


class FireManager(manager.Manager):
    """Manages the setup and communication of Gazoo devices."""

    def __init__(self, debug=False, dev_debug=False, quiet=False):
        stream_debug = debug or dev_debug
        debug_level = logging.WARNING if quiet else logging.DEBUG

        super().__init__(debug_level=debug_level, stream_debug=stream_debug)

    def exec(self, identifier):
        """Alias for create_device with health checks disabled.

        Important: ensure the device is in a healthy state before using "exec" by running health
        checks via `gdm health-check device-1234`.
        Usage from the CLI: `gdm exec device-1234 - shell "echo 'foo'"`.

        Args:
            identifier (str): The identifier string (name) which specifies the device.

        Returns:
            Object: The device found and created by the identifier specified.
        """
        return self.create_device(identifier, make_device_ready="off")

    def get_persistent_prop_devices(self, devices):
        """Gets the persistent properties of one or more devices and returns a json response.

        Args:
          devices (list): Device identifiers to get properties of.

        Returns:
          str: json formatted persistent properties, e.g.
            {
              'device-1234': {
                'build_date': '180124',
                'ftdi_serial_number': '1f824023'
              },
              'device-5678': {},
              ...
            }

        Note:
          This assumes the provided devices are healthy. If properties are unable to be fetched,
          an empty json object will be returned for the device for which the properties could not
          be retrieved.
        """
        logger.setLevel(logging.ERROR)  # silence logging to reduce CLI output
        devices_props = {}
        if isinstance(devices, str):
            devices = devices.split(",")

        for device_name in devices:
            persistent_props = {}
            try:
                device_props = self.get_device_configuration(device_name)
                persistent_props = device_props.get("persistent", {})
            except errors.GazooDeviceError:
                pass  # unhealthy devices will have empty props
            devices_props[device_name] = persistent_props

        return json.dumps(devices_props)

    def get_prop(self, device_name, prop=None):
        """Prints the device properties.

        Args:
          device_name (str): identifier for device.
          prop (str): identifier for property.
        """
        format_line = "  {:22s}  {}"

        if prop is not None:  # If requested a single property...
            value = self.get_device_prop(device_name, prop)
            logger.info(format_line.format(prop, str(value)))
        else:
            props_dicts = self.get_device_prop(device_name, prop)
            property_types = ["persistent", "settable", "dynamic"]
            for property_type in property_types:
                title = "{} Properties:".format(property_type.capitalize())
                logger.info("")
                logger.info(title)
                for prop_name in sorted(props_dicts[property_type]):
                    prop_value = props_dicts[property_type][prop_name]
                    if isinstance(prop_value, list) and len(prop_value) > 1:
                        logger.info(format_line.format(prop_name, ""))
                        for value in prop_value:
                            if callable(value):
                                value = value.__name__
                            logger.info(
                                "\t\t\t  {}".format(str(value)))
                        logger.info("")
                    elif isinstance(prop_value, dict) and len(prop_value) > 1:
                        logger.info(format_line.format(prop_name, ""))
                        for key in sorted(prop_value):
                            logger.info("\t\t\t  {:25s} {!r}".format(key, prop_value[key]))
                        logger.info("")

                    else:
                        logger.info(format_line.format(prop_name, prop_value))

    def health_check(self, identifier, recover=False):
        """CLI command for running device health checks.

        Usage from the CLI: `gdm health-check device-1234`.

        Args:
            identifier (str): The identifier string (name) which specifies the device.
            recover (bool): whether to automatically recover from health check failures.
        """
        make_device_ready_setting = "check_only"
        if recover:
            make_device_ready_setting = "on"
        device = self.create_device(identifier, make_device_ready="off")
        try:
            device.make_device_ready(setting=make_device_ready_setting)
        finally:
            device.close()

    @classmethod
    def helpfull(cls):
        """Prints a general overview of GDM's features. Invoked by 'man' without arguments."""
        description = textwrap.dedent("""
        Gazoo Device Manager (gdm) command line interface is a single utility for control of a
        variety of smart devices.

        Commands:
            The CLI is dynamic, meaning commands are generated from API methods (see
            https://github.com/google/python-fire).
            There are several groups of commands.
                "Manager" commands operate on local config files on the pc.
                These commands are generated from API methods in the Manager class.
                    The command may talk to devices (detect), but they don't change the state of
                    the device (i.e. read-only)
                    The command may change the config files stored on the pc, to detect new
                    devices, add an alias, etc.
                    To see a list of available manager commands, run "gdm".
                "Device" commands talk to or modify a Gazoo device.
                These commands are generated from API methods in device classes.
                    This includes upgrade, reboot, etc.
                    In general you enter a device command as "gdm issue <device_name> -
                    <command>"
                    Examples::
                    gdm issue cambrionix-zdwm - reboot
                    gdm issue device-1234 - upgrade --build-number 1.0d1038
                    To see the list of device commands available for a device, run "gdm man
                    <device_type>"
                    For example:: gdm man cambrionix

            You can get more details on a particular command at the command line with:
            "gdm <command> -h"
            For example::  gdm detect -h

            You can pass in flags to the CLI with:
            "gdm --<flag> - <command>"
            For example:: gdm --debug - devices
            To see a list of available flags, run "gdm -h"

        Supported device types:
        Primary:
        {}

        Auxiliary:
        {}

        Virtual:
        {}

        To explore available device functionality through the dynamic CLI, you will need a device
        attached to your host.

        Use "gdm man" to access static documentation (no devices necessary, but has limitations):
            "gdm man <device_type>" to see all functionality supported by a device.
            "gdm man <device_type> --deprecated" to see just deprecated functionality for a device.
            "gdm man <device_type> <class_attribute>" for detailed documentation.
        """).format(cls._indent_doc_lines(cls.get_supported_primary_device_types()),
                    cls._indent_doc_lines(cls.get_supported_auxiliary_device_types()),
                    cls._indent_doc_lines(cls.get_supported_virtual_device_types()))[1:-1]
        logger.info(description)

    def issue(self, identifier, **kwargs):
        """Alias for create_device with health checks enabled by default.

        Usage from the CLI: `gdm issue device-1234 - shell "echo 'foo'"`.

        Args:
            identifier (str): The identifier string (name) which specifies the device.
            **kwargs (dict): keyword-only arguments passed on to create_device:
                "log_file_name" (str) -- a string log file name to use for log results.
                "log_directory" (str) -- a directory path to use for storing log file.
                "make_device_ready" (str) -- health check setting ("on", "check_only", "off").

        Returns:
            Object: The device found and created by the identifier specified.
        """
        return self.create_device(identifier,
                                  log_file_name=kwargs.get("log_file_name"),
                                  log_directory=kwargs.get("log_directory"),
                                  make_device_ready=kwargs.get("make_device_ready", "on"))

    def log(self, device_name, log_file_name=None, duration=2000):
        """Streams device logs to stdout.

        Args:
          device_name (str): device identifier.
          log_file_name (str): log_file_name. Used for testing purposes.
          duration (float): how long to stream logs for.

        Raises:
          GazooDeviceError: if unable to initiate log file to stream in 10 seconds.
        """
        logger.info("Streaming logs for max {}s".format(duration))
        device = self.create_device(device_name, log_file_name=log_file_name)
        # Disable log rotation feature
        if hasattr(type(device), "switchboard"):
            device.switchboard.set_max_log_size(0)

        try:
            # Wait up to 10 seconds for log file to be created
            end_time = time.time() + MAX_TIME_TO_WAIT_FOR_INITATION
            while time.time() < end_time:
                if os.path.exists(device.log_file_name):
                    break
                time.sleep(0.001)
            else:
                raise errors.GazooDeviceError(
                    "Streaming logs for {} failed. "
                    "Log file not created within {} seconds".format(
                        device_name, MAX_TIME_TO_WAIT_FOR_INITATION))

            start_time = time.time()
            end_time = start_time + duration
            # Open log file and process log file
            with codecs.open(device.log_file_name,
                             "r",
                             encoding="utf-8",
                             errors="replace") as log_file:

                while time.time() < end_time:
                    line = log_file.readline()
                    if line:
                        sys.stdout.write(line)
                        sys.stdout.flush()
                    else:
                        time.sleep(0.001)

        finally:
            sys.stdout.flush()
            device.close()

    def make_devices_ready(self, devices, testing_props=None, aggressive=False):
        """Makes one or more devices ready and returns a json response.

        Args:
          devices (list): Devices identifiers to make ready.
          testing_props (dict): Properties of the testbed used for testing.
          aggressive (bool): Re-flash the device with a valid build if recovery fails.

        Returns:
          str: json formatted device health, e.g.
            {
              'device-1234': {
                'is_healthy': true or false if the device is healthy or not,
                'unhealthy_reason': error message if device is unhealthy,
                'err_type': type of exception raised, if any
              },
              'device-5678': {
                'is_healthy': ...,
                'unhealthy_reason': ...,
                'err_type': ...
              },
              ...
            }
        """
        logger.setLevel(logging.ERROR)  # silence logging to reduce CLI output
        combined_results = {}
        if isinstance(devices, str):
            devices = devices.split(",")

        # create device instances and construct parameter dicts
        device_instances = []
        parameter_dicts = {}
        for device_name in devices:
            try:
                device = self.create_device(device_name, make_device_ready="off")
            except errors.GazooDeviceError as err:
                combined_results[device_name] = self._construct_health_dict_from_exception(err)
            else:
                device_instances.append(device)

                # pass make_device_ready setting to support aggressive recovery
                setting = "flash_build" if aggressive else "on"
                parameter_dicts[device.DEVICE_TYPE] = {"setting": setting}

        # execute testbed health checks if testing props provided
        # property keys that exist in Testbed.PROP_TO_HEALTH_CHECK trigger health checks
        if testing_props:
            try:
                testbed.Testbed(device_instances, testing_props).make_testbed_ready()
            except errors.GazooDeviceError as err:
                combined_results["testbed"] = self._construct_health_dict_from_exception(err)
            else:
                combined_results["testbed"] = HEALTHY_DEVICE_HEALTH

        # execute manager method with each device instance in parallel
        if device_instances:
            results = parallel_utils.parallel_process(
                action_name="make_device_ready",
                fcn=self._make_devices_ready_single_device,
                devices=device_instances,
                parameter_dicts=parameter_dicts)

            # combine results of parallel calls
            for result in results:
                if isinstance(result, dict):
                    combined_results.update(result)
                else:
                    logger.info(result)

        # device instances no longer needed
        for device in device_instances:
            device.close()

        return json.dumps(combined_results)

    @classmethod
    def man(cls, device_type=None, class_attr_name=None, deprecated=False):
        """Prints documentation without reliance on device instance creation.

        Args:
            device_type (str): device type.
            class_attr_name (str): name of the class attribute to display documentation for.
            deprecated (bool): display only deprecated methods and properties.

        Raises:
            GazooDeviceError: if called for documentation on a nested class attribute,
                             such as "touch.zoom".

        Note: dynamic device documentation ("gdm <command> --help") is more complete, but
              requires a device attached to the host to generate documentation.
        """
        if device_type and "." in device_type and class_attr_name is None:  # "man device.method"
            device_type, class_attr_name = device_type.split(".", 1)
        if class_attr_name and "." in class_attr_name:
            raise errors.GazooDeviceError(
                "Static documentation for nested class attributes is not available. "
                "Refer to dynamic CLI documentation instead.")

        if device_type is None and class_attr_name is None:
            cls.helpfull()
        elif class_attr_name is None:
            cls._man_device(device_type, deprecated)
        else:
            cls._man_class_attribute(device_type, class_attr_name)

    def print_usb_info(self):
        """Prints the usb_info dictionary in a human readable form."""
        values = usb_utils.get_address_to_usb_info_dict().values()
        logger.info("{} USB connections found.".format(len(values)))
        for num, usb_info_dict in enumerate(values):
            keys = usb_info_dict.get_properties()
            logger.info("Connection {}:".format(num))
            for key in keys:
                logger.info("\t{:15} {:15}".format(key, str(getattr(usb_info_dict, key))))

    @classmethod
    def _classify_attribute(cls, class_attr):
        """Classifies the class attribute."""
        class_attr = decorators.unwrap(class_attr)
        if isinstance(class_attr, decorators.CapabilityProperty):
            return AttributeClassification.CAPABILITY
        if (hasattr(class_attr, "__deprecated__")
                or hasattr(getattr(class_attr, "fget", None), "__deprecated__")):
            if inspect.isroutine(class_attr):
                return AttributeClassification.DEPRECATED_METHOD
            if isinstance(class_attr, property):
                return AttributeClassification.DEPRECATED_PROPERTY
        if isinstance(class_attr, config.CLASS_PROPERTY_TYPES):
            return AttributeClassification.CLASS_PROPERTY
        if isinstance(class_attr, property):
            return AttributeClassification.PROPERTY
        if inspect.isroutine(class_attr):
            if hasattr(class_attr, "__health_check__"):
                return AttributeClassification.HEALTH_CHECK
            if class_attr.__name__.startswith('_'):
                return AttributeClassification.PRIVATE_METHOD
            return AttributeClassification.PUBLIC_METHOD
        return AttributeClassification.OTHER

    def _construct_health_dict_from_exception(self, exc):
        """Constructs a dictionary containing information about an unhealty device's issues.

        Args:
          exc (Exception): the exception raised that is causing the device's issues

        Returns:
          str: json formatted device health, e.g.
            {
              device-1234: {
                'is_healthy': true,
                'unhealthy_reason': "",
                'err_type': "",
                'checks_passed': [],
                'properties': {}
              }
            }
        """
        device_health = {}
        device_health["is_healthy"] = False
        device_health["unhealthy_reason"] = str(exc)
        device_health["err_type"] = type(exc).__name__
        device_health["checks_passed"] = getattr(exc, "checks_passed", [])
        device_health["properties"] = getattr(exc, "properties", {})
        return device_health

    @classmethod
    def _indent_doc_lines(cls, doc_lines, indent=_DOC_INDENT_SIZE):
        """Indents docstring lines."""
        indent_str = " " * indent
        return "\n".join(indent_str + line for line in doc_lines)

    def _make_devices_ready_single_device(self, device, parameter_dict):
        """Execute make_device_ready for a single device.

        Args:
          device (GazooDeviceBase or AuxiliaryDeviceBase): device to execute make_device_ready on
          parameter_dict (dict): dictionary storing the setting to pass to make_device_ready.

        Returns:
          dict: device health, e.g.
            'device-1234': {
              'is_healthy': true or false if the device is healthy or not,
              'unhealthy_reason': error message if device is unhealthy,
              'err_type': type of exception raised, if any
            }

        Note:
          Intended to be executed in parallel by parallel_utils, triggered by the
          make_devices_ready method.
        """
        device_health = HEALTHY_DEVICE_HEALTH
        try:
            device.make_device_ready(setting=parameter_dict.get("setting"))
        except errors.GazooDeviceError as err:
            device_health = self._construct_health_dict_from_exception(err)

        device_health["logs"] = device.log_file_name
        return {device.name: device_health}

    @classmethod
    def _man_class_attribute(cls, device_type, class_attr_name):
        """Prints class attribute documentation. Invoked by 'man' with 2 args (device, attribute).

        Args:
            device_type (str): device type.
            class_attr_name (str): name of the class attribute to display documentation for.

        Raises:
            GazooDeviceError: if the requested class attribute isn't present for the device type.
        """
        # Find the device class, fetch the requested attribute, and determine what the attribute is
        device_class = cls.get_supported_device_class(device_type)
        if not hasattr(device_class, class_attr_name):
            raise errors.GazooDeviceError("{} ({}) does not have attribute {!r}".format(
                device_type, device_class, class_attr_name))
        attribute = getattr(device_class, class_attr_name)
        classification = cls._classify_attribute(attribute)
        description = classification.value

        if classification == AttributeClassification.CAPABILITY:
            capability_classes = list(attribute.capability_classes)
            attribute = capability_classes[0]
            description += "; flavor: {}".format(attribute.__name__)

            if len(capability_classes) > 1:
                # Capabilities can have multiple flavors in one device class.
                # The flavor used is determined based on device firmware at runtime.
                # Print pydoc just for the first class to avoid clutter and add a warning.
                flavors = [a_cls.__name__ for a_cls in capability_classes]
                logger.warning(
                    "{flavor_num} flavors ({flavors}) of capability `{cap_name}` are available "
                    "for {device_type}.\nShowing documentation for flavor {first_flavor}.\n"
                    .format(flavor_num=len(capability_classes),
                            flavors=flavors,
                            cap_name=class_attr_name,
                            device_type=device_type,
                            first_flavor=attribute.__name__))

        doc_title = "Manual for {class_name}.{attribute_name} ({description})\n".format(
            class_name=device_class.__name__,
            attribute_name=class_attr_name,
            description=description)
        pydoc_lines = pydoc.render_doc(attribute).splitlines()
        doc = doc_title + "\n".join(pydoc_lines[1:])  # Replace pydoc's title
        logger.info(doc)

    @classmethod
    def _man_device(cls, device_type, deprecated):
        """Prints supported device features. Invoked by 'man' with 1 argument (device type)."""
        device_class = cls.get_supported_device_class(device_type)

        # Group device class attributes into properties, health checks, methods, and capabilities
        capability_name_to_classes = {}
        property_names = []
        class_properties = []
        public_methods_names = []
        health_check_names = []
        deprecated_methods = []
        deprecated_properties = []
        for name, attribute in inspect.getmembers(device_class):
            classification = cls._classify_attribute(attribute)
            if classification == AttributeClassification.PROPERTY:
                property_names.append(name)
            elif classification == AttributeClassification.CLASS_PROPERTY:
                if not name.startswith("_"):
                    class_properties.append(f"{name}: {attribute}")
            elif classification == AttributeClassification.HEALTH_CHECK:
                health_check_names.append(name)
            elif classification == AttributeClassification.PUBLIC_METHOD:
                public_methods_names.append(name)
            elif classification == AttributeClassification.CAPABILITY:
                capability_name_to_classes[name] = list(attribute.capability_classes)
            elif classification == AttributeClassification.DEPRECATED_METHOD:
                deprecated_methods.append(f"{name} ({attribute.__deprecated__})")
            elif classification == AttributeClassification.DEPRECATED_PROPERTY:

                # Parse alias from deprecated property docstring
                match = re.search(r'See "(?P<alias>.*)".', attribute.__doc__)
                alias = match.group("alias")
                deprecated_properties.append(f"{name} ({alias})")

        # Generate a summary of supported capability methods and properties for each capability
        capability_lines = []
        for cap_name, cap_classes in capability_name_to_classes.items():
            # There may be several flavors of a capability for a device class.
            for cap_class in cap_classes:
                capability_lines.append("{} ({})".format(cap_name, cap_class.__name__))
                methods_and_props = [
                    name for name, member in inspect.getmembers(cap_class)
                    if cls._classify_attribute(member) in _VISIBLE_CAPABILITY_ATTRIBUTES
                ]
                indented_lines = [" " * _DOC_INDENT_SIZE + line for line in methods_and_props]
                capability_lines.extend(indented_lines)

        docs_capabilities = cls._indent_doc_lines(capability_lines)
        docs_methods = cls._indent_doc_lines(public_methods_names)
        docs_health_checks = cls._indent_doc_lines(health_check_names)
        docs_properties = cls._indent_doc_lines(property_names)
        docs_class_properties = cls._indent_doc_lines(class_properties)
        docs_deprecated_methods = cls._indent_doc_lines(deprecated_methods)
        docs_deprecated_properties = cls._indent_doc_lines(deprecated_properties)

        if deprecated:
            template = textwrap.dedent("""
            Deprecated manual for device type '{device_type}' (class {device_class})

            Deprecated methods:
            {deprecated_methods}

            Deprecated properties:
            {deprecated_properties}

            Use 'gdm man {device_type} <deprecated_attribute>' for detailed documentation.""")[1:]
        else:
            template = textwrap.dedent("""
            Manual for device type '{device_type}' (class {device_class})

            {ownership}
            Supported capabilities:
            {capabilities}

            Supported methods:
            {methods}

            Supported health check methods:
            {health_checks}

            Supported properties:
            {properties}

            Class properties:
            {class_properties}

            Use 'gdm man {device_type} <class_attribute>' for detailed documentation.""")[1:]

        ownership = ""
        owner = getattr(device_class, "_OWNER_LDAP", None)
        if owner:
            ownership = "Owned by {}\n".format(owner)

        doc = template.format(device_type=device_type,
                              device_class=device_class,
                              capabilities=docs_capabilities,
                              methods=docs_methods,
                              ownership=ownership,
                              health_checks=docs_health_checks,
                              properties=docs_properties,
                              class_properties=docs_class_properties,
                              deprecated_methods=docs_deprecated_methods,
                              deprecated_properties=docs_deprecated_properties)
        logger.info(doc)
