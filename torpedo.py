import math
class Torpedo:

    def __init__(self, location, speed, heading, radius):
        '''

        :param location: Initial Location of the torpedo
        :param speed: Initial Speed of the torpedo
        :param heading: Initial Heading of the torpedo
        Initializes our Torpedo class
        '''
        self._x_location, self._y_location = location
        self._x_speed, self._y_speed = speed
        self._heading = heading
        self._life = 0
        self._radius = radius

    def get_location(self):
        '''

        :return: Returns location of the torpedo
        '''
        return self._x_location, self._y_location

    def get_speed(self):
        '''

        :return: Returns the speed of the torpedo
        '''
        return self._x_speed, self._y_speed

    def get_heading(self):
        '''

        :return: Returns the heading of the torpedo
        '''
        return self._heading

    def get_radius(self):
        '''

        :return: Returns the radius of the torpedo
        '''
        return self._radius

    def set_location(self, new_location):
        '''

        :param new_location: New location for the torpedo
        :return: Sets new location
        '''
        self._x_location, self._y_location = new_location

    def set_speed(self, new_speed):
        '''

        :param new_speed: New speed for the torpedo
        :return: Sets new speed
        '''
        self._x_speed, self._y_speed = new_speed

    def set_heading(self, new_heading):
        '''

        :param new_heading: New heading for the torpedo
        :return: Sets new heading for the torpedo
        '''
        self._heading = new_heading

    def get_life(self):
        '''

        :return: Returns the life of the torpedo
        '''
        return self._life

    def set_life(self, new_life):
        '''

        :param new_life: New life for the torpedo
        :return: Sets new life to the torpedo
        '''
        self._life = new_life

    def has_intersection(self, obj):
        '''

        :param obj: Object we want to check intersection with
        :return: Returns True if there is an intersection with another object, else False
        '''
        x_obj, y_obj = obj.get_location()
        x_torpedo, y_torpedo = self.get_location()
        distance = math.sqrt(math.pow((x_obj - x_torpedo), 2) + math.pow((y_obj - y_torpedo), 2))
        if(distance <= self._radius + obj.get_radius()):
            return True
        return False