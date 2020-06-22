from bluesky.utils import Msg


def assert_equals(obj, value, error_message='', halt=True):
    """
    Plan stub that asserts an object's .get equals a particular value.

    Parameters
    ----------
    obj : OphydObject
        The object we will call .get() on.
    value : any
        The value we will compare against.
    error_message : str, optional
        The error to present in the test suite if this fails.
    halt : bool, optional
        If True, end the test on failure. Otherwise, bundle for assertion at
        the end of the test with use of this module's fixtures.
    """
    return (yield Msg('assert_equals', obj, value,
                      error_message=error_message, halt=halt))


def assert_not_equals(obj, value, error_message='', halt=True):
    """
    Plan stub that asserts an object's .get does not equal a particular value.

    Parameters
    ----------
    obj : OphydObject
        The object we will call .get() on.
    value : any
        The value we will compare against.
    error_message : str, optional
        The error to present in the test suite if this fails.
    halt : bool, optional
        If True, end the test on failure. Otherwise, bundle for assertion at
        the end of the test with use of this module's fixtures.
    """
    return (yield Msg('assert_not_equals', obj, value,
                      error_message=error_message, halt=halt))


def cache_value(obj):
    """
    Plan stub that caches an object's .get for later restoration.

    Parameters
    ----------
    obj : OphydObject
        The object we will call .get() on.
    """
    return (yield Msg('cache_value', obj))


def restore_value(obj):
    """
    Plan stub that restores a cached value using .put.

    Parameters
    ----------
    obj : OphydObject
        The object we will call .put() on.
    """
    return (yield Msg('restore_value', obj))


def annotate(message):
    """
    Plan stub to add messages to a plan inspection routine.

    Parameters
    ----------
    message: str
        The message to include.
    """
    return (yield Msg('annotate', message))
