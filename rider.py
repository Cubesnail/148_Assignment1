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
    # TODO: patience, status, origin, destination
    pass
    def __init__(self,identifier,patience,origin,destination):
        #patience = 0 #number of minutes the rider will wait
        self.status = WAITING
        self.id = identifier
        self.origin = origin
        self.destination = destination
        self.patience = patience
