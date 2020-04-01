import math
TEN = 10
MINUS_FIVE = -5
class Asteroid:

    def __init__(self, location, speed, life):
        '''

        :param location: Takes in the initial location of the asteroid
        :param speed: Takes in the initial speed of the asteroid
        :param life: Takes in the initial life of the asteroid
        Initializes our class Asteroid
        '''

        self._x_location, self._y_location = location
        self._x_speed, self._y_speed = speed
        self._life = life
        self._radius = self._life * TEN + MINUS_FIVE

    def get_location(self):
        '''

        :return: Returns the location of the asteroid
        '''
        return self._x_location, self._y_location

    def get_speed(self):
        '''

        :return: Returns the speed of the asteroid
        '''
        return self._x_speed, self._y_speed

    def get_life(self):
        '''

        :return: Returns the life of the asteroid
        '''
        return self._life

    def get_radius(self):
        '''

        :return: Returns the radius of the asteroid
        '''
        return self._radius

    def set_location(self, new_location):
        '''

        :param new_location: New location for the asteroid
        :return: Sets a new location for the asteroid
        '''
        self._x_location, self._y_location = new_location

    def set_speed(self, new_speed):
        '''

        :param new_speed: New speed for the asteroid
        :return: Sets a new speed for the asteroid
        '''
        self._x_speed, self._y_speed =  new_speed

    def set_life(self, new_life):
        '''

        :param new_life: New life for the asteroid
        :return: Sets new life for the asteroid
        '''
        self._life = new_life

    def has_intersection(self, obj):
        '''

        :param obj: The object we want to check interaction with
        :return: Returns True if there is an interaction, otherwise False
        '''
        x_obj, y_obj = obj.get_location()
        x_asteroid, y_asteroid = self.get_location()
        distance = math.sqrt(math.pow((x_obj - x_asteroid), 2) + math.pow((y_obj - y_asteroid), 2))
        if(distance <= self._radius + obj.get_radius()):
            return True
        return False