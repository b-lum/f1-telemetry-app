class Lap:

    def __init__(self, num, coordinates) :
        self.num = num # lap number
        self.movement = {} # dictionary with key time (s) and values truple (speed, throttle, brake)
        self.coordinates = {} # dictionary with key time (s) and values truple (X World Coordinate, Y World Coordinate, Z World Coordinate)

    def add_movement(self, time, speed, throttle, brake) :
        self.movement[time] = (speed, throttle, brake) # type: ignore

    def add_coordinate(self, time, X, Y, Z) :
        self.coordinates[time] = (X, Y, Z)
