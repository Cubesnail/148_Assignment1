from driver import Driver
from rider import Rider
from container import PriorityQueue

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None
        """
        self.driver_list = []
        self.rider_queue = PriorityQueue()

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str
        """
        print("Drivers: ",end="")
        print(self.driver_list)

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        """
        if len(self.driver_list) == 0:
            self.rider_queue.add(rider)
            return None
        else:
            shortest_time = self.driver_list[0]
            for name in self.driver_list:
                if name.get_travel_time(rider.destination) < shortest_time.get_travel_time(rider.destination):
                    if name.is_idle:
                        shortest_time = name
        return shortest_time

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None
        """
        if not self.rider_queue.is_empty():
            return self.rider_queue.remove()
        else:
            self.driver_list.append(driver)
            return None

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None
        """
        if self.rider_queue.__contains__(rider):
            self.rider_queue.delete(rider)
            rider.status = CANCELLED
