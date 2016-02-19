"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""
from location import Location

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """ A rider for a ride sharing service

    === Attributes ===
    @type id: str
        A unique identifier for the rider.
    @type origin: Location
        The riders original location
    @type destination: Location
        The riders requested destination
    @type patience: int
        The amount of minutes the rider will wait
    """
    def __init__(self, identifier, patience, origin, destination):
        """Initialize a Rider.

        @type self: Rider
        @type identifier: str
        @type patience: int
        @type origin: Location
        @type destination: Location
        @rtype: None
        """
        self.status = WAITING  # The status of the rider.
        self.id = identifier  # The name of the rider.
        self.origin = origin  # The riders original location.
        self.destination = destination  # The riders requested destination.
        self.patience = patience # The amount of minutes the rider will wait.

    def __eq__(self,other):
        return self.