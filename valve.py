import bluesky.plan_stubs as bps
from pcdsdevices.valve import VGC

from atef.plan_stubs import (assert_equals, assert_not_equals,
                             cache_value, restore_value)
from atef.plan_tools import dry_run, Dummy
from atef.preprocessors import cache_restore_decorator


# @cache_restore_decorator(['valve.at_vac_setpoint'])
def test_valve(valve: VGC):
    """
    Reactive:

    From open state, check PLC fast fault output is true (Beam Permitted)
    Adjust valve setpoint to break valve interlock
    Valve will close
    Verify fast fault output is now false (Beam Off)
    Restore valve setpoint
    Reopen valve
    Clear fast fault
    Clear fast fault output
    Verify all log messages were emitted by valve state change and fast fault.

    Preemtive:

    From open state, and Arbiter:Full-Rate Beam, issue a close valve command
    Observe arbiter requests 0-rate beam
    Observe valve closes
    Request valve open
    Observe arbiter releases 0-rate beam
    """
    # Must start in open state
    yield from assert_equals(valve.open_limit, 1,
                             error_message='Valve not open, cannot start test')
    yield from assert_equals(valve.closed_limit, 0,
                             error_message='Valve closed, cannot start test')
    # Fail if fast fault in open state
    yield from assert_equals(valve.mps_state, 1,
                             error_message='PLC FFO False with valve open')

    # Cache valve setpoint for restoration
    yield from cache_value(valve.at_vac_setpoint)
    # Adjust vac setpoint to break the interlock and close the valve
    yield from bps.abs_set(valve.at_vac_setpoint, 0, wait=True)
    # Check that we closed and that fast fault is active
    yield from assert_equals(valve.open_limit, 0,
                             error_message='Valve stayed open after an '
                                           'interlock break')
    yield from assert_equals(valve.closed_limit, 1,
                             error_message='Valve did not close after an '
                                           'interlock break')
    yield from assert_equals(valve.mps_state, 0,
                             error_message='PLC FFO did not go True after '
                                           'an interlock break')
    # Restore the cached value
    yield from restore_value(valve.at_vac_setpoint)

    # Re-open the valve
    yield from bps.abs_set(1, valve.open_command)

    # Clear fast fault
    # Clear fast fault output
    # I don't know how to do these

    # Prompt user to check the log messages
    yield from bps.input_plan('Check that all log messages were emitted '
                              'properly. Press enter when done.')


def valve_test_dry_run():
    dry_run(test_valve(Dummy(VGC, name='valve')))


if __name__ == '__main__':
    valve_test_dry_run()
