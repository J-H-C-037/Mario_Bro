import time
import copy

class Enemy:
    def __init__(self, x: int, y: int, dir: bool, obstacles: list):
        """ This method creates the Enemy object
        @param x the starting x of the Enemy
        @param y the starting y of the Enemy
        @param dir a boolean to store the initial direction of the enemy.
                True is facing right, False is facing left
        @param obstacles is a list that stores information of the obstacles that the enemies can interact with. It is a copy of the original obstacles list of the class board

        """

        self.x = x
        self.y = y
        self.dir = dir

        self.alive = True

        self.obstacles = obstacles

    def move(self, progress: int, speed = 0.1):
        """ This is an example of a method that moves the enemy, it receives the
                direction and the speed (with default value). The speed
                only changes for the case of Turtle when it is shot because Mario step on him consecutively twice"""

        if self.alive or speed != 0.1: #moves if the enemy is still alive or if the velocity != 0, which means that the Turtle (though died) is being shot, so it can move
            for obstacle in self.obstacles:
                #comparing the coordinates of the enemy and those of the obstacles, if the enemy hit a obstacle, it changes the direction

                if (abs(round(self.x + self.sprite[3]) - obstacle.sprite[5]) < 2 \
                        and (round(self.y) + self.sprite[4] > obstacle.sprite[6] + 3 \
                             and round(self.y) < obstacle.sprite[6] + obstacle.sprite[4])):
                    self.dir = False #change direction to left
                elif (abs(round(self.x) - (obstacle.sprite[5] + obstacle.sprite[3])) < 2 \
                      and (round(self.y) + self.sprite[4] > obstacle.sprite[6] + 3 \
                           and round(self.y) < obstacle.sprite[6] + obstacle.sprite[4])):
                    self.dir = True #change direction to right

            if self.dir: #moves the enemy according to the direction
                self.x += speed
            else:
                self.x -= speed

    def in_the_ground(self): #check if the enemy is in the ground
        for obstacle in self.obstacles:
            if abs(self.y + self.sprite[4] - obstacle.sprite[6]) < 4 \
                    and (round(self.x + self.sprite[3]) > obstacle.sprite[5]) \
                    and (round(self.x) < (obstacle.sprite[5] + obstacle.sprite[3])
            ):
                return True
        return False


class Goomba(Enemy): #subclass of enemy
    def __init__(self, x: int, y: int, dir: bool, obstacles: list):
        self.sprite = [1, 0, 0, 16, 16, copy.copy(x), copy.copy(y),
                       copy.copy(dir)]  # img bank, x and y of the image bank, width, height, copy of x, copy of y and copy dir (because we will need them later to restart the game when Mario die
        super().__init__(x, y, dir, obstacles) #inherit these parameters from the motherclass


class Turtle(Enemy):
    def __init__(self, x: int, y: int, dir: bool, obstacles: list):
        self.sprite = [1, 0, 64, 16, 16, copy.copy(x), copy.copy(y),
                       copy.copy(dir)]  # img bank, x and y of the image bank, width, height, copy of x, y and dir
        self.death_time = 0 #record the time when the turtle died
        super().__init__(x, y, dir, obstacles)
        self.shot = False #this parameter tells us is mario is shot or not
        self.second_time = False #Mario second time in the back of the turtle
        self.third_time = False #Mario is killed when touching the tutle being shot

    def revive(self): #this function allows the turtle to revive in 5s after being step 1 time by Mario

        if not self.alive: #if turtle is not alive
            if self.death_time == 0: #if the turtle has just died
                self.death_time = time.time()
            elif time.time() - self.death_time > 5: #revive the turtle after 5s
                self.alive = True
                self.death_time = 0