class Location:
    def __init__(self, row, column):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """
        # TODO
        pass
        self.row = row
        self.col = column

    def __str__(self):
        """Return a string representation.

        @rtype: str
        """
        # TODO
        pass

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool
        """
        # TODO
        pass
        return self == other


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int
    """
    # TODO
    return abs(origin.row - destination.row) + abs(origin.col - destination.col)


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location
    """
    # TODO
    pass
    result = Location()
    helper_list = location_str.split(',')
    result.col = int(helper_string[0])
    result.row = int(helper_list[1])