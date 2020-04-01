class Ship:

    def __init__(self, location, life):
        '''

        :param location: Initial Location of the ship
        :param life: Initial life of the ship
        Initializes our class Ship
        '''
        self._x_location, self._y_location  = location
        self._x_speed, self._y_speed = 0, 0
        self._heading = 0.0
        self._radius = 10
        self._life = life
    def get_location(self):
        '''

        :return: Returns the location of the ship
        '''
        return self._x_location, self._y_location

    def get_speed(self):
        '''

        :return: Returns the speed of the ship
        '''
        return self._x_speed, self._y_speed

    def get_heading(self):
        '''

        :return: Returns the heading of the ship
        '''
        return self._heading

    def get_radius(self):
        '''

        :return: Retuns the radius of the ship
        '''
        return self._radius

    def get_life(self):
        '''

        :return: Returns the life of the ship
        '''
        return self._life

    def set_life(self, new_life):
        '''

        :param new_life: New life for ship
        :return: Sets new life for ship
        '''
        self._life = new_life

    def set_location(self, new_location):
        '''

        :param new_location: New location for the ship
        :return: Sets new location for the ship
        '''
        self._x_location, self._y_location = new_location
        return

    def set_speed(self, new_speed):
        '''

        :param new_speed: New speed for the ship
        :return: Sets new speed for the ship
        '''
        self._x_speed, self._y_speed = new_speed
        return

    def set_heading(self, new_heading):
        '''

        :param new_heading: New heading for the ship
        :return: Sets new heading for the ship
        '''
        self._heading = new_heading
        return