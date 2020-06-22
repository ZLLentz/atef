"""
Module to inspect test plans before running them
"""
from ophyd.device import Component as Cpt


def dry_run(plan):
    """
    Run through the plan's steps without executing any of them.

    For this to work properly the plan needs to avoid adaptive branching logic.
    This is an extension of bluesky's summarize_plan, customized for dry
    running atef test runs and extended to include every message type.
    """
    for msg in plan:
        # summarizers[msg.command](msg)
        generic_summary(msg)


def generic_summary(msg):
    cmd_text = msg.command
    elems = []
    if msg.obj is not None:
        elems.append(summary_name(msg.obj))
    if msg.args:
        for arg in msg.args:
            elems.append(summary_name(arg))
    if msg.kwargs:
        for key, value in msg.kwargs.items():
            value = summary_name(value)
            elems.append(f'{key}={value}')
    if elems:
        args_text = ', '.join(elems)
        print(f'{cmd_text}({args_text})')
    else:
        print(cmd_text)


def summary_name(obj):
    try:
        try:
            return str(obj.dotted_name)
        except AttributeError:
            return str(obj.name)
    except AttributeError:
        return str(obj)


class Dummy:
    """
    Create a dummy object based on a device class to be used in a dry run.

    A dummy object will raise an exception if you try to access any control
    system values, call methods directly, or inspect the device heirarchy.
    These are all things that you shouldn't be doing in a plan.

    You will be able to refer to specific subcomponents as long as no actions
    are taken on them.
    """
    def __init__(self, device_class, name='dummy', dotted_name=None):
        self.name = name
        self.dotted_name = dotted_name or name
        for attr_name in dir(device_class):
            # Skip if we would override an existing attribute
            if hasattr(self, attr_name):
                continue
            attr_value = getattr(device_class, attr_name)

            # Placeholder value for a property
            if isinstance(attr_value, property):
                setattr(self, attr_name, None)
            # Copy ints, strs, etc. as-is
            elif attr_value.__class__.__module__ == '__builtins__':
                setattr(self, attr_name, attr_value)
            # Replace callables with something that errors
            elif callable(attr_value):
                setattr(self, attr_name, dummy_method)
            # Apply Dummy recursively to component classes
            elif isinstance(attr_value, Cpt):
                setattr(self, attr_name,
                        Dummy(attr_value.cls,
                              name=f'{name}_{attr_name}',
                              dotted_name=f'{name}.{attr_name}'))
            # Apply everything else as-is
            else:
                setattr(self, attr_name, attr_value)


def dummy_method(*args, **kwargs):
    raise RuntimeError('Cannot call methods directly in a bluesky plan.')
