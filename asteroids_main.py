from screen import Screen
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import random
import math

ROUNDS = 200
DEFAULT_ASTEROIDS_NUM = 3
LEFT_CLICK = 7
RIGHT_CLICK = -7
LIFE_ASTEROID = 3
MAX_TORPEDOS = 15
ACC_FACTOR = 2
TORPEDO_LIST_ID = []
INITIAL_MAX_SPEED = 4
MAX_SPEED = 7
SHIP_LIFE = 3
TORPEDO_RADIUS = 4


class GameRunner:
    def __init__(self, asteroids_amnt=DEFAULT_ASTEROIDS_NUM):
        '''

        :param asteroids_amnt: Amount of asteroids on the screen
        This initializes our Game to get it started
        '''
        self._screen = Screen()

        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        random_x_loc = random.randint(self.screen_min_x, self.screen_max_x)
        random_y_loc = random.randint(self.screen_min_y, self.screen_max_y)
        ship_location = random_x_loc, random_y_loc
        self._ship = Ship(ship_location, SHIP_LIFE)  # Generates an object with Class type Ship
        self._score = 0
        data_list = [ship_location]
        times = 0
        self._asteroid_list = []
        self._torpedo_list = []
        while times < asteroids_amnt:  # Generates objects with Class type Asteroid
            loc_asteroid_x = random.randint(self.screen_min_x, self.screen_max_x)
            loc_asteroid_y = random.randint(self.screen_min_y, self.screen_max_y)
            asteroid_location = loc_asteroid_x, loc_asteroid_y
            if asteroid_location not in data_list:
                data_list.append(asteroid_location)
                x_speed_asteroid = random.randint(1, INITIAL_MAX_SPEED)
                y_speed_asteroid = random.randint(1, INITIAL_MAX_SPEED)
                asteroid_speed = x_speed_asteroid, y_speed_asteroid
                temp_asteroid = Asteroid(asteroid_location, asteroid_speed, LIFE_ASTEROID)
                self._asteroid_list.append(temp_asteroid)
                self._screen.register_asteroid(self._asteroid_list[times], self._asteroid_list[times].get_life())
                times += 1

    def move_object(self, speed, location, object):
        '''

        :param speed: Speed of the object
        :param location: Location of the object
        :param object: The object we want to move
        :return: Returns new location for the object according to some equation
        '''
        old_x_location, old_y_location = location
        old_x_speed, old_y_speed = speed
        delta_x = self.screen_max_x - self.screen_min_x
        delta_y = self.screen_max_y - self.screen_min_y
        new_x_location = (old_x_speed + old_x_location - self.screen_min_x) % delta_x + self.screen_min_x
        new_y_location = (old_y_speed + old_y_location - self.screen_min_y) % delta_y + self.screen_min_y
        new_location = new_x_location, new_y_location
        object.set_location(new_location)

    def rotate_ship(self):
        '''

        :return: Rotates the ship according to the left or right press
        '''
        if (self._screen.is_left_pressed()):
            self._ship.set_heading(self._ship.get_heading() + LEFT_CLICK)
        if (self._screen.is_right_pressed()):
            self._ship.set_heading(self._ship.get_heading() + RIGHT_CLICK)

    def acceleration(self):
        '''

        :return: Accelerates the ship according to an equation and limits it's speed so it won't get out of hand
        '''
        if (self._screen.is_up_pressed()):
            old_x_speed, old_y_speed = self._ship.get_speed()
            new_x_speed = old_x_speed + math.cos(math.radians(self._ship.get_heading()))
            if (math.fabs(new_x_speed) > MAX_SPEED and new_x_speed < 0):
                new_x_speed = -MAX_SPEED
            if (new_x_speed > MAX_SPEED):
                new_x_speed = MAX_SPEED
            new_y_speed = old_y_speed + math.sin(math.radians(self._ship.get_heading()))
            if (math.fabs(new_y_speed) > MAX_SPEED and new_y_speed < 0):
                new_y_speed = -MAX_SPEED
            if (new_y_speed > MAX_SPEED):
                new_y_speed = MAX_SPEED
            new_speed = new_x_speed, new_y_speed
            self._ship.set_speed(new_speed)

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def create_and_intersection_asteroid(self):
        '''

        :return: Creates asteroids and checks if there happens intersections with ship
        '''
        i = 0
        while i < (DEFAULT_ASTEROIDS_NUM - (DEFAULT_ASTEROIDS_NUM - len(self._asteroid_list))):
            # It runs with respect to the number of the current asteroids and not the initial
            x_location_asteroid, y_location_asteroid = self._asteroid_list[i].get_location()
            self.move_object(self._asteroid_list[i].get_speed(), self._asteroid_list[i].get_location(),
                             self._asteroid_list[i])
            self._screen.draw_asteroid(self._asteroid_list[i], x_location_asteroid, y_location_asteroid)
            if self._asteroid_list[i].has_intersection(self._ship):
                self._asteroid_list[i].set_life(self._asteroid_list[i].get_life() - 1)
                self._screen.show_message('Intersection', 'There has been an intersection')
                self._screen.unregister_asteroid(self._asteroid_list[i])
                del self._asteroid_list[i]
                self._ship.set_life(self._ship.get_life() - 1)
                if (self._ship.get_life() == 0):
                    self._screen.remove_life()
                    self._screen.show_message('Game Over!', 'Ran out of lives :/')
                    self._screen.end_game()
                    sys.exit()
                else:
                    self._screen.remove_life()
            i += 1

    def register_torpedo(self):
        '''

        :return: Generates objects with Class type Torpedo and draws them to the screen
        '''
        if self._screen.is_space_pressed() and len(self._torpedo_list) <= MAX_TORPEDOS:
            temp_x_speed, temp_y_speed = self._ship.get_speed()
            new_x_speed = temp_x_speed + ACC_FACTOR * math.cos(math.radians(self._ship.get_heading()))
            new_y_speed = temp_y_speed + ACC_FACTOR * math.sin(math.radians(self._ship.get_heading()))
            speed = new_x_speed, new_y_speed
            temp_torpedo = Torpedo(self._ship.get_location(), speed, self._ship.get_heading(), TORPEDO_RADIUS)
            if (id(temp_torpedo) not in TORPEDO_LIST_ID):
                TORPEDO_LIST_ID.append(temp_torpedo)
                self._screen.register_torpedo(temp_torpedo)
            x, y = temp_torpedo.get_location()
            self._screen.draw_torpedo(temp_torpedo, x, y, temp_torpedo.get_heading())
            self._torpedo_list.append(temp_torpedo)

    def intersection_with_asteroid_torpedo(self, asteroid, torpedo):
        '''

        :param asteroid: An asteroid on the screen
        :param torpedo: A torpedo fired from the ship
        :return: Deals with the occurrence where a torpedo hits an asteroid
        '''
        if asteroid.get_life() > 1:  # If the asteroid's life is greater than 1, then it divides into two smaller asteroids
            x_torpedo, y_torpedo = torpedo.get_speed()
            x_asteroid, y_asteroid = asteroid.get_speed()
            speed_x = (x_torpedo + x_asteroid) / math.sqrt(x_asteroid ** 2 + y_asteroid ** 2)
            speed_y = (y_torpedo + y_asteroid) / math.sqrt(x_asteroid ** 2 + y_asteroid ** 2)
            new_speed1 = speed_x, speed_y
            temp_asteroid1 = Asteroid(asteroid.get_location(), new_speed1, asteroid.get_life() - 1)
            new_speed2 = -speed_x, -speed_y
            temp_asteroid2 = Asteroid(asteroid.get_location(), new_speed2, asteroid.get_life() - 1)
            self._screen.unregister_asteroid(asteroid)
            self._asteroid_list.remove(asteroid)
            self._asteroid_list.append(temp_asteroid1)
            self._asteroid_list.append(temp_asteroid2)
            self._screen.register_asteroid(temp_asteroid1, temp_asteroid1.get_life())
            x_location1, y_location1 = temp_asteroid1.get_location()
            self._screen.draw_asteroid(temp_asteroid1, x_location1, y_location1)
            self._screen.register_asteroid(temp_asteroid2, temp_asteroid2.get_life())
            x_location2, y_location2 = temp_asteroid2.get_location()
            self._screen.draw_asteroid(temp_asteroid2, x_location2, y_location2)
        else:  # Else, it disappears
            self._screen.unregister_asteroid(asteroid)
            self._asteroid_list.remove(asteroid)

    def move_torpedo(self):
        '''

        :return: Moves the torpedo using the move.object function, also checks if there is intersections with the asteroids
        '''
        i = 0
        while i < (len(self._torpedo_list)):
            self._torpedo_list[i].set_life(self._torpedo_list[i].get_life() + 1)  #
            if (self._torpedo_list[i].get_life() > 200):
                self._screen.unregister_torpedo(self._torpedo_list[i])
                del self._torpedo_list[i]
                continue
            self.move_object(self._torpedo_list[i].get_speed(), self._torpedo_list[i].get_location(),
                             self._torpedo_list[i])
            x, y = self._torpedo_list[i].get_location()
            self._screen.draw_torpedo(self._torpedo_list[i], x, y, self._torpedo_list[i].get_heading())
            index = 0
            while (index < len(self._asteroid_list)):
                if (self._torpedo_list[i].has_intersection(self._asteroid_list[index])):
                    if (self._asteroid_list[index].get_life() == 3):
                        self._score += 20
                    if (self._asteroid_list[index].get_life() == 2):
                        self._score += 50
                    if (self._asteroid_list[index].get_life() == 1):
                        self._score += 100
                    self.intersection_with_asteroid_torpedo(self._asteroid_list[index], self._torpedo_list[i])
                    self._screen.set_score(self._score)
                    self._screen.unregister_torpedo(self._torpedo_list[i])
                    del self._torpedo_list[i]
                    break
                index += 1
            i += 1

    def _game_loop(self):
        '''

        :return: This is my main function, it only calls the help functions that I built
        '''
        x_location_ship, y_location_ship = self._ship.get_location()
        self.move_object(self._ship.get_speed(), self._ship.get_location(), self._ship)
        self._screen.draw_ship(x_location_ship, y_location_ship, self._ship.get_heading())
        self.create_and_intersection_asteroid()
        self.rotate_ship()
        self.acceleration()
        self.register_torpedo()
        self.move_torpedo()
        if (len(self._asteroid_list) == 0):
            self._screen.show_message('Congrats!!', 'You Won. Your score: ' + str(self._score))
            self._screen.end_game()
            sys.exit()
        elif (self._screen.should_end()):
            self._screen.show_message('Game Over!', 'Exiting Game. Score: ' + self._score)
            self._screen.end_game()
            sys.exit()


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
