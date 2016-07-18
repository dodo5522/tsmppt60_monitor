#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#   Copyright 2016 Takashi Ando - http://blog.rinka-blossom.com/
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" Battery driver class to access service. """

from solar_monitor import logger
from solar_monitor.event.base import IEventTrigger


class DataIsUpdatedTrigger(IEventTrigger):
    """ Event trigger to pass the data to the registered event handlers
        whenever received any data. """

    def _is_condition(self, data):
        """ Trigger condition is matched or not. This class object should
            pass the data whenever received any data, so return True always.

        Args:
            data: To judge the condition.
        Returns:
            True if the trigger condition is matched.
        """
        return True


class BatteryLowTrigger(IEventTrigger):
    """ Event trigger to pass the data if battery volage is low. The instance
        object of this class has pre_voltage_ statical value, so you should
        keep this instance during monitoring solar system.

    Args:
        lowest_voltage: Low limit of battery voltage.
    Returns:
        Instance object.
    """
    def __init__(self, lowest_voltage, q_max=5):
        IEventTrigger.__init__(self, q_max=q_max)
        self.lowest_voltage_ = lowest_voltage
        self.pre_voltage_ = None

    def _is_condition(self, data):
        """ Returns True if battery voltage getting low and run over the limit
            of lowest voltage setting.

        Args:
            data: To judge the condition.
        Returns:
            True if the trigger condition is matched.
        Raises:
            KeyError: Some key doesn't exist in received data.
        """

        logger.debug("Got data on {} at {}".format(type(self).__name__, data["at"]))

        current_voltage = data["data"]["Battery Voltage"]["value"]

        if self.pre_voltage_ is None:
            self.pre_voltage_ = current_voltage

            # If the current voltage is already low when the first checking,
            # returns True and run some procedure to save the battery power.
            if self.lowest_voltage_ > current_voltage:
                return True

        # If the battery volate run over the limit of lowest batery voltate,
        # returns True and run some procedure to save the battery power.
        if self.pre_voltage_ >= self.lowest_voltage_:
            if self.lowest_voltage_ > current_voltage:
                return True

        return False


class BatteryFullTrigger(IEventTrigger):
    """ Event trigger to pass the data if battery volage is charged fully. The
        instance object of this class has pre_voltage_ statical value, so you
        should keep this instance during monitoring solar system.

    Args:
        full_voltage: Highet voltage if battery is charged full.
    Returns:
        Instance object.
    """
    def __init__(self, full_voltage, q_max=5):
        IEventTrigger.__init__(self, q_max=q_max)
        self.full_voltage_ = full_voltage
        self.pre_voltage_ = None

    def _is_condition(self, data):
        """ Returns True if battery voltage getting high and run over the limit
            of highest voltage setting.

        Args:
            data: To judge the condition.
        Returns:
            True if the trigger condition is matched.
        Raises:
            KeyError: Some key doesn't exist in received data.
        """

        logger.debug("Got data on {} at {}".format(type(self).__name__, data["at"]))

        current_voltage = data["data"]["Battery Voltage"]["value"]

        if self.pre_voltage_ is None:
            self.pre_voltage_ = current_voltage

            # If the current voltage is already high when the first checking,
            # returns True and run some procedure.
            if self.full_voltage_ <= current_voltage:
                return True

        # If the battery volate run over the limit of highest batery voltate,
        # returns True and run some procedure.
        if self.pre_voltage_ < self.full_voltage_:
            if self.full_voltage_ <= current_voltage:
                return True

        return False