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

"""Internal Decorators used in GDM device classes and capabilities.

Included are the following:

* Log Decorator
* CapabilityLogDecorator
* CapabilityDecorator
* health_check
* DynamicProperty
* PersistentProperty
* SettableProperty


- BASIC USAGE:

***CapabilityDecorator***
Required for all capability properties in device classes.
Used to dynamically identify the capabilities and their flavors of a device class.

@decorators.CapabilityDecorator(<capability_flavor>)

Ex:

@decorators.CapabilityDecorator(light_events_default.LightEventsDefault)
def light_events(self):
    return self.lazy_init(light_events_default.LightEventsDefault,
                          shell_fn=self.shell,
                          device_name=self.name,
                          command_dict=self.commands)

Can declared multiple flavors, if the flavor is not determined until initiation
@decorators.CapabilityDecorator(
        [weave_default.WeaveDefault, weave_log_events_based.WeaveLogEventsBased,
         weave_shell_based.WeaveShellBased])
    def weave(self):
        ....


***LogDecorator***
Required for all public methods in a device lcass that don't return a value.

This decorator will:
    1. Log a start message at the start of decorated method
    2. Log a success message at the end of decorated method if method succeeds
        2.1 The success message will also contain the method execution time.
    3. Log a skip message if method is skipped
        3.1 To skip a method, raise SkipExceptionError("YOUR_REASON.")
    4. Wrap all your exceptions in GazooDeviceError (or a different wrap_type).
        4.1 The original exception type will be preserved in the error message.
    5. Add "<device> <method> failed. <Exception type>: <Exception message>."
        formatting to all exceptions.
        5.1 Note: don't specify the device name and method name in the exception message.
            This decorator does this for you!
            Example: use SomeError("Foo") instead of SomeError("Device <..> failed. Reason: Foo")

@decorators.LogDecorator(logger)
def your_method(self):
    pass

OR (to change the level)
Log_LEVEL can be one of NONE, DEBUG, INFO, WARNING, ERROR, CRITICAL
@decorators.LogDecorator(logger, level=decorators.<LOG_LEVEL>)
def your_method(self):
    pass


***CapabilityLogDecorator***
Required for all public methods in capability classes that don't return a value.
logger is the gdm_logger instance in the class

@decorators.CapabilityLogDecorator(logger)
def your_method(self):
    pass

OR (to change the level)
Log_LEVEL can be one of NONE, DEBUG, INFO, WARNING, ERROR, CRITICAL
@decorators.CapabilityLogDecorator(logger, level=decorators.<LOG_LEVEL>)
def your_method(self):
    pass

***health_check***
Used to identify all the public methods in a device class used for health checks.
Note: The only public methods allowed in device classes are those identified in the base template
 and health checks. All others must be in capabilities.

@decorators.health_check
def check_logs_streaming(self):

***DynamicProperty***
Used to identify dynamic properties, usually device states.

These properties change throughout testing. ex: firmware_version, pairing.state, etc.

@decorators.DynamicProperty
def firmware_version(self):

***PersistentProperty***
Used to identify all persistent properties.

These are properties that are persistent throughout device lifetime.
ex: hardware_model, serial_number, etc. These are either populated during device detection or
static for a device class.

@decorators.PersistentProperty
def serial_number(self):

***SettableProperty***
These are settable properties, usually initialized as None. They allow users to enable additional
capabilities or set properties undetectable via device communication.
Ex: power_switch_port to enable power cycling via powerswitch, alias, or device_usb_port if the
device is connected to a Cambrionix.

@decorators.SettableProperty
def alias(self):
"""
import functools
import inspect
import logging
import time
from gazoo_device import errors
from gazoo_device import gdm_logger

GDM_LOGGER = gdm_logger.get_gdm_logger()

# Enable specifying logger levels by decorators.<LEVEL> (so users don't have to import logging)
NONE = None
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

MESSAGES = {
    "START": "{device_name} starting {class_name}.{method_name}",
    "SKIP": "{device_name} {class_name}.{method_name} skipped. {skip_reason}.",
    "SUCCESS": "{device_name} {class_name}.{method_name} successful. It took {time_elapsed}s.",
    "FAILURE": "{device_name} {class_name}.{method_name} failed. {exc_name}: {exc_reason}"
}

DEFAULT_DEVICE_NAME = "Unknown_device"

# This attribute is added to decorated methods so it's possible
# to access the wrapped function. Same as "__wrapped__" attribute in Python 3.
WRAPS_ATTR_NAME = "_gdm_decorators_wraps"


class SkipExceptionError(Exception):
    """Used to tell info Error wrapper to skip last message."""


def unwrap(func):
    """Get the original function object of a wrapper function.

    Noop (returns func) if func is not decorated with decorator.

    Args:
        func (function): method, or property decorated with decorator

    Returns:
        function: the original function object (prior to decoration).
    """
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__
    return func


class CapabilityDecorator():
    """Decorator to define capabilities in device classes (wraps CapabilityProperty).

    @decorators.CapabilityDecorator(light_events_default.LightEventsDefault)
    def light_events(self):
        return self.lazy_init(light_events_default.LightEventsDefault,
                              shell_fn=self.shell,
                              device_name=self.name,
                              command_dict=self.commands)
    """

    def __init__(self, class_or_classes):
        """Initialize the capability decorator.

        Args:
            class_or_classes (object): single capability flavor class or list (or tuple) of
                                       capability flavor classes.
                                       GDM uses this to determine which capabilities are
                                       supported by a device class.

        Note:
            Input validation of class_or_classes is not done by the decorator at import time.
            Instead, it is performed by unit_tests/test_all_devices.py.
            This allows to avoid a circular import.
        """
        classes = class_or_classes
        if not isinstance(class_or_classes, (list, tuple)):
            classes = [classes]
        self._capability_classes = classes

    def __call__(self, fget):
        """Wrapper around CapabilityProperty to support decorator syntax.

        Args:
            fget (method): getter function (returns a capability instance).
                           Note that most capability getter functions should use
                           GazooDeviceBase.lazy_init().

        Returns:
            CapabilityProperty: property denoting a supported capability.
        """
        return CapabilityProperty(fget, classes=self._capability_classes)


class CapabilityProperty(property):
    """Property under which a capability is accessible in a device class. Do not use directly.

    Disambiguates device property definitions and device capability definitions.
    """

    def __init__(self, fget, classes):
        """Initialize the capability property.

        Args:
            fget (method): getter function (returns a capability instance).
                           Note that most capability getter functions should use
                           GazooDeviceBase.lazy_init().
            classes (sequence): list or tuple of capability flavor classes.
                                Used by GDM to determine which capabilities are supported by a
                                device class.
        """
        super().__init__(fget)
        self.capability_classes = set(classes)


class LogDecorator():
    """Wraps GDM methods with standard logger messages (logged to the provided logger).

    Catches all exceptions and wraps them in GazooDeviceError (or other wrap_type).
    Required for any public method that doesn't return a value.

    Note:
        GDM design asks for there to be a syntax for all info messsages and errors raised.
        This enforces that syntax.

        Example output when successful:
        cambrionix-1234 started factory_reset
        cambrionix-1234 successfully factory_reset in 10 s.

        Example out when failed:
        cambrionix-1234 started factory_reset
        cambrionix-1234 factory_reset failed. GazooDeviceError: device did not respond
            recognizably.
    """

    def __init__(self, logger, level=INFO, wrap_type=errors.GazooDeviceError, name_attr="name"):
        """Create a log decorator wrapper.

        Args:
            logger (logger): logger to use to print messages.
            level (int or None): logging level (see logging module level for integer values).
                                 (decorators.INFO, decorators.DEBUG, decorators.NONE)
                                 NONE disables logging messages (but errors are still wrapped).
            wrap_type (GazooDeviceError): wrap the errors in this class if it's not an instance of
                                         it already. Valid values are GazooDeviceError
                                         or its subclasses.
            name_attr (str): name of attribute containing the device name.
                             For example, if device name is under self.device_name,
                             the value should be "device_name".

        Raises:
            TypeError: if wrap_type is not a subclass of GazooDeviceError.
        """
        if not issubclass(wrap_type, errors.GazooDeviceError):
            raise TypeError("Invalid wrap_type: {}. "
                            "wrap_type can only be a subclass of GazooDeviceError."
                            .format(wrap_type))
        self.logger = logger
        self.level = level
        self.wrap_type = wrap_type
        self.name_attr = name_attr

    def __call__(self, func):
        """Wraps (decorates) the provided function.

        Args:
            func (function): function to be decorated

        Returns:
            function: a wrapper function (decorated input function)

        Raises:
            TypeError: incorrect type of func argument.
        """
        # Note: cannot use inspect.ismethod() here. At the time of decorator __init__ call,
        # python intepreter has not yet created the class of the method we're decorating.
        # At this time, the 'method' is still a function. Once all methods are created,
        # the python interpreter creates the class object, then binds the functions' self
        # arguments to make them 'methods.' Hence at this point func is considered a function
        # by python even if it's actually a method.
        if not callable(func):
            raise TypeError("Expected func to be callable, found {}.".format(func))

        error_template = ("Expected {} to be an instance method. "
                          "Decorating {} methods is not supported; remove the decorator.")
        func_args = inspect.getfullargspec(func).args

        if func_args and func_args[0] == "cls":
            raise TypeError(error_template.format(func, "class"))
        if not func_args or func_args[0] != "self":
            raise TypeError(error_template.format(func, "static"))

        @functools.wraps(func)
        def wrapped_func(instance, *args, **kwargs):
            """Wraps (decorates) the given function.

            Args:
                instance (object): class instance
                *args (tuple): positional arguments to the wrapped function
                **kwargs (dict): keyword arguments to the wrapped function

            Raises:
                TracebackError: wrapped error (the traceback is added to __str__ and __repr__).

            Note:
                this wrapper only works for methods, not functions (see the instance argument).

            Returns:
                object: same value as the wrapped function.
            """
            fmt_args = {
                "device_name": getattr(instance, self.name_attr, DEFAULT_DEVICE_NAME),
                "method_name": func.__name__,
                "class_name": self._find_defining_class_name(func, type(instance)),
                "skip_reason": None,
                "time_elapsed": None,
                "exc_name": None,
                "exc_reason": None
            }

            return_val = None
            method_skipped = False
            start_time = time.time()

            if self.level is not None:
                self.logger.log(self.level, MESSAGES["START"].format(**fmt_args))

            try:
                return_val = func(instance, *args, **kwargs)
            except SkipExceptionError as err:
                method_skipped = True
                fmt_args["skip_reason"] = str(err)
            except Exception as err:
                self._format_and_raise(fmt_args, err)

            if self.level is not None:
                if method_skipped:
                    self.logger.log(self.level, MESSAGES["SKIP"].format(**fmt_args))
                else:
                    fmt_args["time_elapsed"] = int(time.time() - start_time)
                    self.logger.log(self.level, MESSAGES["SUCCESS"].format(**fmt_args))

            return return_val

        wrapped_func.__dict__[WRAPS_ATTR_NAME] = func
        return wrapped_func

    def _find_defining_class_name(self, method, current_class):
        """Finds the name of the class from which the method was inherited from.

        Args:
            method (func): method object.
            current_class (type): class to start the search from.

        Returns:
            str: name of the class defining the given method.
            None: defining class wasn't found in the class hierarchy.

        Note:
            There are 2 subtleties:
            * to correctly identify the class for super().<method> calls, the method check has to
              compare the method by identity (to avoid matching overridden methods).
            * methods may need to be unwrapped (from the log decorator) to make the identity
              comparison work.
            Doesn't work on class methods, but they are not decorated with the log decorator.
        """
        for a_class in current_class.__mro__:
            a_class_method = vars(a_class).get(method.__name__)
            if a_class_method and unwrap(a_class_method) is method:
                return a_class.__name__
        return None

    def _format_and_raise(self, fmt_args, err):
        """Format the exception message & type before re-raising."""
        wrapped_exc = err
        if (not isinstance(err, errors.CheckDeviceReadyError)
                and not isinstance(err, self.wrap_type)):
            fmt_args["exc_name"] = type(err).__name__
            fmt_args["exc_reason"] = str(err)
            # Wrap the error in a different type and reraise.
            reraise_msg = MESSAGES["FAILURE"].format(**fmt_args)
            wrapped_exc = self.wrap_type(reraise_msg)

        # Note: do nothing for CheckDeviceReadyErrors & subclasses.
        # These have two mandatory positional arguments in their signatures,
        # unlike the other errors, which typically have just one (the message).
        # It would be nice to get rid of the extra arguments (device name) in the signatures
        # and instead just let the log decorator add the device name to the error message.
        # However, refactoring these errors to use the log decorator is non-trivial.
        # This is because many of these are raised in plain functions (not methods),
        # which are not supported by this log decorator...
        raise wrapped_exc


class CapabilityLogDecorator(LogDecorator):
    """Adds standardized log messages to capability methods."""

    def __init__(self, logger, level=INFO, wrap_type=errors.GazooDeviceError,
                 name_attr="_device_name"):
        """Log decorator for capabilities (with a different name_attr default value).

        Args:
            logger (logger): logger to use to print messages.
            level (int or None): logging level (see logging module level for integer values).
                                 For example, level=INFO or level=NONE.
                                 NONE disables logging messages (but errors are still wrapped).
            wrap_type (GazooDeviceError): wrap the errors in this class if it's not an instance of
                                         it already. Valid values are GazooDeviceError
                                         or its subclasses.
            name_attr (str): name of attribute containing the device name.
                             For example, if device name is under self.device_name,
                             the value should be "device_name".

        Note:
            All capabilities need to have a device name reference in the capability class.
            This is required for log and error messages in multi-device tests.
        """
        super().__init__(logger, level=level, wrap_type=wrap_type, name_attr=name_attr)


decorators_factory = LogDecorator(GDM_LOGGER, level=DEBUG)


def health_check(func):
    """Health Check Decorator.  Returns silenced log decorator."""
    func.__health_check__ = True
    return decorators_factory(func)


class DynamicProperty(property):
    """A property that is dynamic and involves a device query to return."""

    def __init__(self, fget):
        super().__init__(fget, doc=fget.__doc__)
        self.name = fget.__name__


class SettableProperty(property):
    """Usually defaults to null, a property that can be set."""

    def __init__(self, fget, fset=None, fdel=None, doc=None):
        if not doc:
            doc = fget.__doc__
        super().__init__(fget, fset=fset, fdel=fdel, doc=doc)
        self.name = fget.__name__


class PersistentProperty(property):
    """A property that is persistent throughout device interaction.

    Is static across device class or can only be reset during device detection.
    """

    def __init__(self, fget):
        super().__init__(fget, doc=fget.__doc__)
        self.name = fget.__name__
