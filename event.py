"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"

class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience, self.rider, driver))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider.id)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        # Notify the monitor about the request.

        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        monitor.notify(self, DRIVER, REQUEST, self.driver.id, self.driver.location)

        rider = dispatcher.request_rider(self.driver)
        events = []
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)  # changed destination to origin
            events.append(Pickup(self.timestamp + travel_time, rider, self.driver))  # rider.patience replaced
            # with travel time
            # events.append(Cancellation(self.timestamp + rider.patience, rider, self.driver))  # tab added here,
            # changed starter code
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str
        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    """A rider cancels the ride.
    === Attributes ===
    @type driver: Driver
        The driver.
    @type rider: Rider
        The rider.
    @type timestamp: int
        The timestamp.
    """
    def __init__(self, timestamp, rider, driver):
        """

        @param timestamp: int
        @param rider: Rider
        @param driver: Driver
        @return: None
        """
        super().__init__(timestamp)
        self.timestamp = timestamp
        self.rider = rider
        self.driver = driver

    def __str__(self):
        """Return a string representation of the event
        @return: str
        """
        return "{} -- {}: Cancelled.".format(self.timestamp, self.rider.id)

    def do(self, dispatcher, monitor):
        """

        @param dispatcher: Dispatcher
        @param monitor: Monitor
        @return: None
        """
        if self.rider.status == WAITING:
            monitor.notify(self.timestamp, RIDER, CANCEL, self.rider.id, self.rider.origin)

            dispatcher.cancel_ride(self.rider)
            # Cancel the ride, if the rider is waiting.

class Pickup(Event):
    """A driver picks up a passenger

    === Attributes ===
    @type driver: Driver
        The driver.
    @type rider: Rider
        The rider.
    @type timestamp: int
        The timestamp
    """
    def __init__(self, timestamp, rider, driver):
        """

        @param timestamp: int
        @param rider: Rider
        @param driver: Driver
        @return: None
        """
        super().__init__(timestamp)
        self.timestamp = timestamp
        self.rider = rider
        self.driver = driver

    def __str__(self):
        """Return a string representation of the event.

        @return: str
        """
        return "{} -- {}: Picks up {}.".format(self.timestamp,self.driver.id,self.rider.id)

    def do(self, dispatcher, monitor):
        """Set the drivers passenger as the rider.

        @param dispatcher:
        @param monitor:
        @return: list[Event]
        """
        if self.rider.status == WAITING:
            time = self.driver.start_ride(self.rider)
            monitor.notify(self.timestamp, DRIVER, PICKUP, self.driver.id, self.rider.origin)
            monitor.notify(self.timestamp, RIDER, PICKUP, self.rider.id, self.rider.origin)
            # Notify the monitor
            events = []
            events.append(Dropoff(self.timestamp + time, self.rider, self.driver))
            # Add a Dropoff event
            dispatcher.cancel_ride(self.rider)
            # Remove the rider from the queue
        else:
            self.driver.rider = None
        return events


class Dropoff(Event):
    """A driver drops off a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    @type rider: Rider
        The rider.
    @type timestamp: int
        The timestamp
    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a Dropoff event.

        @param timestamp: int
        @param rider: Rider
        @param driver: Driver
        @return: None
        """
        super().__init__(timestamp)
        self.rider = rider
        self.timestamp = timestamp
        self.driver = driver
        self.driver.end_ride()

    def __str__(self):
        """Return a string representation of the event.

        @return: str
        """
        return "{} -- {}: Drops off {}.".format(self.timestamp, self.driver.id, self.rider.id)

    def do(self, dispatcher, monitor):
        """Set the drivers passenger to None, finish the ride.
        @param dispatcher: Dispatcher
        @param monitor: Monitor
        @return: list[Event]
        """
        monitor.notify(self.timestamp, DRIVER, DROPOFF, self.driver.id, self.rider.destination)
        monitor.notify(self.timestamp, RIDER, DROPOFF, self.rider.id, self.rider.destination)
        events = []
        events.append(DriverRequest(self.timestamp, self.driver))
        return events


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """
    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            if event_type == "DriverRequest":
                temp_Driver = Driver(timestamp, tokens[2],deserialize_location(tokens[3]),int(tokens[4]))
                Event = DriverRequest(timestamp,temp_Driver)
                # Create a DriverRequest event.
                pass
            elif event_type == "RiderRequest":
                temp_Rider = Rider(timestamp, tokens[2],int(tokens[5]), deserialize_location(tokens[3]),
                                   deserialize_location(tokens[4]))
                Event = RiderRequest(timestamp,temp_Rider)
                # Create a RiderRequest event.
                pass
            events.append(Event)
    return events
