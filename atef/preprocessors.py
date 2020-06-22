import functools
import inspect

from bluesky.preprocessors import finalize_wrapper
from bluesky.utils import make_decorator

from .plan_stubs import cache_value, restore_value, annotate


def find_attr_in_args(attr, func, args, kwargs):
    """
    Find the signal or device represented by attr that was passed into func.
    """
    device_name, signal_name = attr.split('.')
    try:
        device = kwargs[device_name]
    except KeyError:
        args_list = inspect.getargspec(func).args
        index = args_list.index(device_name)
        device = args[index]
    return getattr(device, signal_name)


def cache_restore_wrapper(plan, attrs):
    """
    Wrapper to restore changed values at the end of a plan.
    """
    objs = []

    def inner(*args, **kwargs):
        for attr in attrs:
            obj = find_attr_in_args(attr, plan, args, kwargs)
            objs.append(obj)
            yield from cache_value(obj)
        return (yield from plan(*args, **kwargs))

    def cleanup():
        yield from annotate('Plan jumps here on failure')
        for obj in objs:
            yield from restore_value(obj)

    @functools.wraps(plan)
    def new_plan(*args, **kwargs):
        return (yield from finalize_wrapper(inner(*args, **kwargs), cleanup))

    return new_plan


cache_restore_decorator = make_decorator(cache_restore_wrapper)
