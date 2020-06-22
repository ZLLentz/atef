"""
Module to define custom RE commands
"""


def register_atef_commands(RE):
    """
    Registers all custom atef commands with a run engine.
    """
    RE.register_command('assert_equals', _assert_equals)
    RE.register_command('assert_not_equals', _assert_not_equals)
    RE.register_command('cache_value', _cache_value)
    RE.register_command('restore_value', _restore_value)
    RE.register_command('annotate', _annotate)


assert_cache = []


def assert_handler(result, error_message, halt):
    """
    Handle assert messages for unit tests

    Parameters
    ----------
    result : bool
        The thing that must be true
    error_message : str
        To be shown in the case of failure
    halt: bool
        If True, assert now. If False, add to assert_cache.
    """
    if halt:
        assert result, error_message
    else:
        assert_cache.append((result, error_message))


async def _assert_equals(msg):
    """
    RE command that asserts an object's .get equals a particular value.

    Expected Message object is:
        Msg('assert_equals', signal, value, error_message='', halt=bool)
    """
    assert_handler(msg.obj.get() == msg.args[0],
                   msg.kwargs['error_message'],
                   msg.kwargs['halt'])


async def _assert_not_equals(msg):
    """
    RE command that asserts an object's .get does not equal a particular value.

    Expected Message object is:
        Msg('assert_not_equals', signal, value, error_message='', halt=bool)
    """
    assert_handler(msg.obj.get() != msg.args[0],
                   msg.kwargs['error_message'],
                   msg.kwargs['halt'])


value_cache = {}


async def _cache_value(msg):
    """
    RE command that caches a value to be restored later.

    Expected message object is:
        Msg('cache_value', signal)
    """
    value_cache[msg.obj.name] = msg.obj.get()


async def _restore_value(msg):
    """
    RE command that restores a cached value.

    Expected message object is:
        Msg('restore_value', signal)
    """
    msg.obj.put(value_cache[msg.obj.name])


async def _annotate(msg):
    """
    No-op used to add text to plan inspection routines.
    """
    pass
