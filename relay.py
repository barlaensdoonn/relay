#!/usr/bin/python3
# murmur - 4-channel relay board
# 12/7/17
# updated: 4/15/18

# find GPIO pin mappings here:
# https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering

import time
import gpiozero


class Relay(gpiozero.OutputDevice):
    '''
    class to extend gpiozero's OutputDevice base class

    OutputDevice has several useful methods including on(), off(), and toggle(),
    and some variables including pin, active_high, and initial_value.
    documentation here: https://gpiozero.readthedocs.io/en/stable/api_output.html#outputdevice
    '''

    def __init__(self, pin, board_type='denkovi', *args, **kwargs):
        '''
        to use our own __init__ in the Relay class, we must explicitly call
        the base class's __init__, otherwise it will be overridden
        more here: https://stackoverflow.com/questions/6396452/python-derived-class-and-base-class-attributes#6396839

        change board type to 'sainsmart' to set active_high=False,
        which initializes the common Sainsmart relays as off
        '''

        self.GPIO_pin = pin
        self.board_type = board_type.lower()
        self.active_high = self._set_active_high()
        gpiozero.OutputDevice.__init__(self, self.GPIO_pin, active_high=self.active_high, *args, **kwargs)
        self.state = self.get_state()

    def _set_active_high(self):
        return False if self.board_type == 'sainsmart' else True

    def activate(self):
        self.on()
        self.state = self.get_state()

    def deactivate(self):
        self.off()
        self.state = self.get_state()

    def get_state(self):
        return self.value

    def test_connection(self):
        '''
        test the pi's ability to control a relay
        do this BEFORE hooking up anything to the relay and watch LED on the relay board
        '''

        self.on()
        time.sleep(1)
        self.off()


if __name__ == '__main__':
    # the following is an example of how to test multiple relays connected to one Pi
    pins = [4, 5, 6, 13]  # list to store GPIO pins being used
    relays = [Relay(pin) for pin in pins]  # list to hold initialized Relay objects

    # loop through the relays, turning them on for 1 second
    for relay in relays:
        relay.test_connection()
