from location import Location, manhattan_distance
from rider import Rider

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"

class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, timestamp, identifier, location, speed):
        """Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        self.id = identifier
        self.location = location
        self.speed = speed
        self.destination = None
        self.rider = None
        self.is_idle = True
        self.timestamp = timestamp

    def __str__(self):
        """Return a string representation.

        @type self: Driver
        @rtype: str
        """
        return self.id + ' ' + str(self.location.row) + ',' + str(self.location.col) + ' ' + str(self.speed)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool
        """
        return self.timestamp == other.timestamp

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int
        """
        return round(manhattan_distance(self.location,destination)/self.speed)

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int
        """
        time = self.get_travel_time(location)
        self.is_idle = False
        self.destination = location
        return time

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        self.location = self.destination
        self.is_idle = True

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int
        """
        self.rider = rider
        self.location = rider.origin
        rider.status = SATISFIED
        time = self.start_drive(rider.destination)
        return time

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        self.rider.status = SATISFIED
        self.rider = None
        self.end_drive()
        self.destination = None
