import copy
from block import Question, Brick
import time

from special_object import Mushroom, Coin


class Mario:
    """ This class stores all the information needed for Mario"""

    def __init__(self, x: int, y: int, dir: bool, obstacles: list, enemies: list, special_objects: list):
        """ This method creates the Mario object
        @param x the starting x of Mario
        @param y the starting y of Mario
        @param dir a boolean to store the initial direction of Mario.
                True is facing right, False is facing left
        @param obstacles is a list that stores information of the obstacles that Mario can interact with. It is a copy of the original obstacles list of the class board
        @param enemies is a list that stores information of the enemies (Boombas and Turtles) that Mario can iteract with
        @param special_objects is a list that stores information of the special objects like the Mushroom and the Star"""
        self.x = x
        self.y = y
        self.direction = dir
        # store how far the map moved until the last move, we will use it later to update the positions of the objects that Mario can interact with
        self.previous_progress = 0

        self.sprite = [0, 48, 16, 16, 16]  # img bank, x and y of the image bank, width, height.
        # We assume that Mario will always have three lives in the beginning
        self.lives = 3
        self.special_objects = special_objects

        # we create a copy because we won't like to modify the original list, we would have to update the positions of the objects depeding how far the map has moved
        self.copy_special_objects = copy.deepcopy(self.special_objects)
        # jump_force decides the height that Mario jumps
        self.original_jump_force = 12
        self.jump_force = copy.copy(self.original_jump_force)

        self.obstacles = obstacles
        self.copy_obstacles = copy.deepcopy(obstacles)

        self.enemies = enemies
        self.big_mario = False

        self.score = 0
        self.coins = 0

    # this function evaluates if Mario is in the ground or obstacle by comparing the positions of x and y of mario and those of the obstacles
    def in_the_ground(self):
        for obstacle in self.copy_obstacles:
            if abs(self.y + self.sprite[4] - obstacle.y) < 5 \
                    and (round(self.x + self.sprite[3]) > obstacle.x) \
                    and (round(self.x) < (obstacle.x + obstacle.sprite[3])
            ):
                return True
        return False

    # this function evaluates if Mario is in the enemy and is used to evaluate Mario has killed them, the main difference with the function
    # in the ground is that there is an optional parameter that enables us to evaluate if Mario is in the head of a particular enemy
    def in_the_enemy(self, specific_enemies=[]):
        if specific_enemies == []:
            specific_enemies = self.enemies  # all the enemies, not specific
        for enemy in specific_enemies:  # comparing x and y of enemy and Mario, we subtract the x of enemy by the progress of the map to know its current position in the window
            if abs(self.y + self.sprite[4] - enemy.y) < 4 \
                    and (round(self.x + self.sprite[3]) > enemy.x - self.previous_progress) \
                    and (round(self.x) < (enemy.x + enemy.sprite[3]) - self.previous_progress):
                return True
        return False

    def at_the_ceiling(self):  # this function evaluates if Mario touching the ceiling or obstacle by comparing the positions of x and y of mario and those of the obstacles
        #also it allows us to get the special_objects
        for obstacle in self.copy_obstacles:
            if (((abs(self.y - (obstacle.y + obstacle.sprite[4])) < 7) \
                 and (round(self.x + self.sprite[3]) > obstacle.x) \
                 and (round(self.x) < obstacle.x + obstacle.sprite[3]))):

                if type(obstacle) == Question:

                    self.obstacles[self.copy_obstacles.index(obstacle)].sprite[2] = 152
                    for special_object in self.special_objects:
                        if special_object.x == obstacle.sprite[5] and special_object.y == obstacle.sprite[6]:
                            if type(special_object) == Mushroom:
                                special_object.y -= obstacle.sprite[4]
                            elif type(special_object) == Coin:
                                special_object.y -= obstacle.sprite[4]
                                self.score += 100
                                self.coins += 1
                if type(obstacle) == Brick and self.big_mario:

                    self.obstacles[self.copy_obstacles.index(obstacle)].sprite[3] = 0 #delete the obstacle in the original list
                    self.obstacles[self.copy_obstacles.index(obstacle)].sprite[4] = 0
                    obstacle.sprite[3] = 0 #delete the obstacle in the copied list, so mario stop interacting with it
                    obstacle.sprite[4] = 0
                    self.score += 50


                return True
        return False

    def go_right(self, speed, progress):  # this function make Mario move right, it receives the parameter progress (not previous_progress, the current one) and the speed that Mario moves, he can run or walk
        go = True
        for obstacle in self.copy_obstacles:
            obstacle.x -= (progress - self.previous_progress)  # update the x of the obstacle according to the progresssion of the map

            # if mario is touching an obstacle, he can't go right further, go = False
            if not (abs(round(self.x + self.sprite[3]) - obstacle.x) > 2 \
                    or (round(self.y) + self.sprite[4] < obstacle.y + 3 \
                        or round(self.y) > obstacle.y + obstacle.sprite[4])):
                go = False
        if go:  # if go = True, we increase the x of Mario
            self.x += speed

    def go_left(self, speed,
                progress):  # the same as above but for the left side, we won't have to change the x of Mario, because when Mario moves to the left, the map doen't move
        go = True
        for obstacle in self.copy_obstacles:

            if not (abs(round(self.x) - (obstacle.x + obstacle.sprite[3])) > 2 \
                    or (round(self.y) + self.sprite[4] < obstacle.y + 3 \
                        or round(self.y) > obstacle.y + obstacle.sprite[4])):
                go = False
        if go:
            self.x -= speed

    def mushroom_effect(self,
                        special_object):  # this function is called when Mario gets a Mushroom and has the functionaties to make to make Mario bigger
        previous_height = self.sprite[4]
        self.sprite = [0, 48, 32, 16, 32]  # a new sprite

        self.y -= self.sprite[4] - previous_height  # update the y, because now Mario is bigger
        # the Mushroom disappear in the original list, height and width = 0
        self.special_objects[self.copy_special_objects.index(special_object)].sprite[3] = 0
        self.special_objects[self.copy_special_objects.index(special_object)].sprite[4] = 0
        self.big_mario = True
        self.score += 500

    def special_object_right(self, progress):  # it checks if
        for special_object in self.copy_special_objects:  # we use the copy instead of the original one because we will change its x according the the movement of the map
            if self.special_objects[self.copy_special_objects.index(special_object)].sprite[3] != 0:  # we check in the original list if the special_object is not already taken by Mario, we can either check its width or height
                special_object.x -= (progress - self.previous_progress)
                # Comparing x and y of Mario and the x and y of the special objects, if Mario is touching them, look for what type of special object is
                if not (abs(round(self.x + self.sprite[3]) - special_object.x) > 5 \
                        or (round(self.y) + self.sprite[4] < special_object.y -6\
                            or round(self.y) +4  > special_object.y + special_object.sprite[4])):
                    if type(special_object) == Mushroom:
                        self.mushroom_effect(special_object)  # do the effects of eating a Mushroom

    def special_object_left(
            self):  # the same as above but for the left side, we won't have to change the x of Mario, because when Mario moves to the left, the map doesn't move
        for special_object in self.copy_special_objects:
            if self.special_objects[self.copy_special_objects.index(special_object)].sprite[3] != 0:
                if not (abs(round(self.x) - (special_object.x + special_object.sprite[3])) > 5 \
                        or (round(self.y) + self.sprite[4] < special_object.y -6 \
                            or round(self.y) +4 > special_object.y + special_object.sprite[4])):
                    if type(special_object) == Mushroom:
                        self.mushroom_effect(special_object)

    def move(self, direction: str, size: int, speed: int, progress: int):
        """ This is an example of a method that moves Mario, it receives the
        direction, the size of the board, the speed that Mario should move (Mario has two types of speed: walking or running) and the progress of the map with respect to the x axis"""
        # Checking the current horizontal size of Mario to stop him before and if mario is alive

        mario_x_size = self.sprite[3]

        if direction.lower() == 'right' and self.x < size - mario_x_size and self.lives > 0:
            self.sprite[1] = 48  # change the sprite
            self.go_right(speed, progress)  # call the function to go_right
            self.special_object_right(progress)  # check if it finds a special object
            self.previous_progress = progress  # update the progress


        elif direction.lower() == 'left' and self.x > 0 and self.lives > 0:  # the same as above but without the need to update self.previous_progress because the map does not move when you go left
            self.sprite[1] = 32  # change the sprite
            self.go_left(speed, progress)
            self.special_object_left()

    def jump(self):
        """ This is an example of a method that makes Mario jump, it receives the
                direction and the size of the board"""

        # check if he reaches the upper border, if he is hitting the ceiling (an obstacle) and if Mario is alive
        if not self.at_the_ceiling() and self.lives > 0 and self.y > 0:
            self.y = self.y - self.jump_force
            if self.jump_force > 0:
                self.jump_force -= 1
