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
        return str(self.row) + ',' + str(self.col)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool
        """
        return self == other


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int
    """
    return abs(origin.row - destination.row) + abs(origin.col - destination.col)


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location
    """
    # Parse the string and type cast it
    temp_list = location_str.split(',')
    result = Location(int(temp_list[1]), int(temp_list[0]))
    return result
