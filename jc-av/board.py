import time
import pyxel
import copy
import random

from block import Question, Brick
from mario import Mario  # we import the class Mario
from enemies import Goomba, Turtle  # we import the enemies
from map import obstacles, background_elements, special_objects  # we import the variable obstacles, which is a list that contains all the information of the blocks in the map


class Board:
    """ This class contains all the information needed to represent the
    board of the Game"""

    def __init__(self, w: int, h: int):
        """ The parameters are the width and height of the board"""

        self.width = w
        self.height = h

        self.special_objects = special_objects # this list is gonna store the info of the special objects that is in the board/map

        self.enemies = []

        self.obstacles = obstacles  # the obstacles

        self.background_elements = background_elements  # the bushes and the clouds

        self.progress = 0  # store the progress of the map

        # only the obstacles one is a copy because the others won't be changed

        self.velocities = [0] * (
                    len(self.enemies) + 1)  # this list help us to generate gravitational effect on the enemies and Mario. Each number of the list corresponds to a particular enemy/Mario, and it is zero when they are in the ground

        self.big_x = copy.copy(
            self.width)  # it tells us what place of the map we are displacing, when starts from 255 (the width of the board) meaning that it is displacing from x = 0 to x = 255

        self.beginning_time = time.time()

        self.time_limit = 300  # seconds
        self.game_over = False

        self.mario = Mario(self.width / 2, 220, True, (self.obstacles), self.enemies,
                           self.special_objects)  # the mario, it starts in the middle of the screen in the ground, we pass 3 lists containing the objects that he can interact with
        self.time_remaining = 0
    def update(self):

        if self.time_limit < (int(time.time() - self.beginning_time)):  # why we don't surpass the time limit
            self.restart()

        self.mario_movements()

        if pyxel.btn(pyxel.KEY_R):
            self.restart(True)  # a new match

        if self.mario.in_the_ground() or self.mario.in_the_enemy():  # if Mario is in the grounf of in the enemy, we recharge his original jump_force
            self.mario.jump_force = self.mario.original_jump_force

        self.progress = self.big_x - self.width  # we update the progress of the map

        self.interaction_with_enemies()  # this function moves the enemies, see if a enemy touches/kills a Mario and also if Mario is killing a enemy

        # move the map if neccesary

        self.move_map()

        if self.mario.y > 255:
            self.restart()

        self.gravity_mario()  # the gravity, when it is not in the ground, Mario starts falling

        self.generate_and_delete_enemies()

    def mario_movements(self):
        if pyxel.btnp(pyxel.KEY_Q):  # finish the game if the user press "Q"
            pyxel.quit()
        elif pyxel.btn(pyxel.KEY_RIGHT):  # Mario go right if he can
            if pyxel.btn(
                    pyxel.KEY_X):  # if X is also pressed, Mario runs. we increase the velocity that the mario moves
                self.mario.move('right', self.width, 2, self.progress)
            else:  # otherwise Mario walks
                self.mario.move('right', self.width, 1, self.progress)
        elif pyxel.btn(pyxel.KEY_LEFT):  # the same but for the left
            if pyxel.btn(pyxel.KEY_X):
                self.mario.move('left', self.width, 2, self.progress)
            else:
                self.mario.move('left', self.width, 1, self.progress)
        if pyxel.btn(pyxel.KEY_Z):  # Mario jumps if he can is Z is pressed
            self.mario.jump()

    def generate_and_delete_enemies(self):
        if len(self.enemies) < 4 and random.randint(1, 50) == 1:  # generate enemies if the condition is fit
            ram = random.randint(1, 4)
            if ram == 1:
                self.enemies.append(Turtle(random.randint(self.big_x, self.big_x + 255), random.randint(180, 220), True, self.obstacles))
            else:
                self.enemies.append(Goomba(random.randint(self.big_x, self.big_x + 255), random.randint(180, 220), True, self.obstacles))

            self.velocities += [0]
        i = 0
        while i < (len(self.enemies)):  # delete enemies out of the screen
            if self.enemies[i].x < self.big_x - self.width:
                del self.enemies[i]

            i+= 1

    def draw(self):
        pyxel.cls(12)  # draw the background with blue colour

        # We draw the things
        self.print_obstacles_and_special_objects_and_background_elements()
        self.print_enemies()
        self.print_mario()

        if self.game_over:
            pyxel.text(5, self.height / 2, "Game over, restart the game pressing the key R", 2)
        else:
            pyxel.text(5, 10, "Time remaining: " + str(self.time_limit - (int(time.time() - self.beginning_time))), 0)
            pyxel.text(5, 30, "Lives:" + str(self.mario.lives), 0)
            pyxel.text(5, 50, "Score: " + str(self.mario.score), 0)
            pyxel.text(5, 70, "Coins: " + str(self.mario.coins), 0)

        if self.big_x > 3056 + self.width:
            if self.time_remaining == 0:
                self.time_remaining = self.time_limit - (int(time.time() - self.beginning_time))

            pyxel.text(20, 100, "Thank you for playing. The game is over. Score: " + str(self.mario.score + self.time_remaining *2),0)
        # draw the time with colour black (0) in (5,10)

    def dead_turtle(self, enemy):
        # if mario leaves the back of the turtle and jump again on it, second_time = True
        if not self.mario.in_the_enemy(
                [enemy]):  # we pass a list with the turtle to see specifically if Mario is on the turtle
            enemy.second_time = True
        enemy.revive()  # the turtle revive in 5s if it is not shot, if it is shot, it desappears in 5s

        if self.mario.in_the_enemy(
                [enemy]) and enemy.second_time:  # if mario is on the back of the turtle and this is the second time
            enemy.shot = True  # we shot the turtle
            enemy.sprite[1] = 32  # we change the sprite

        if enemy.shot:
            # we increase the velocity that the enemy moves, we don't gives it directly velocity 5 due to the design of the collision algorithm, which is based on a inequality, so we don't want to velocity to be too big at once. Instead, we increase the frequency to achive the same purpose and avoid errors
            enemy.move(self.progress, 1)  # turtle is shot by Mari
            enemy.move(self.progress, 1)

            # the turtle can kill other enemies when being shot
            for other_enemy in self.enemies:
                if (round(enemy.x + enemy.sprite[3]) - other_enemy.x) >= 0 and (
                        round(enemy.x) - (other_enemy.x + other_enemy.sprite[3])) <= 0 \
                        and round(enemy.y) + enemy.sprite[4] > other_enemy.y \
                        and round(enemy.y) < other_enemy.y + other_enemy.sprite[4]:
                    if other_enemy != enemy:
                        other_enemy.alive = False

            if enemy.alive:  # the turtle disappear after 5 seconds being shot, the function revive has double uses as we see: revive the turtle when it is only step by Mario once, and kills the turtle definitely after Mario shot it
                enemy.sprite[
                    3] = 0  # width = 0 we don't delete the object from the list, because we will have to use it again if the game restart
                enemy.sprite[4] = 0  # height = 0

    def mario_kill_enemies(self, enemy):
        for enemy in self.enemies:
            if enemy.alive:  # if anemy is alive, then he moves and we check if mario is in the enemy
                enemy.move(self.progress)
                if self.mario.in_the_enemy([enemy]):  # if mario is in the enemy, the enemy dies
                    enemy.alive = False
                    self.mario.score += 250
            else:  # is the enemy is dead
                if type(enemy) == Turtle:
                    self.dead_turtle(
                        enemy)  # although the turtle is supposed to be dead, it has some particular charascteristic that make us define another specific function for executing them after he is dead
                elif type(enemy) == Goomba:  # the goomba disappear when killed(not alive)
                    enemy.sprite[3] = 0  # width = 0
                    enemy.sprite[4] = 0  # height = 0

    def enemy_kill_mario(self, enemy):
        if enemy.alive:  # if enemy alive and the enemy is touching Mario, he dies
            if (round(self.mario.x + self.mario.sprite[3]) - enemy.x + self.progress) >= 0 and (
                    round(self.mario.x) - (enemy.x + enemy.sprite[3]) + self.progress) <= 0 \
                    and round(self.mario.y) + self.mario.sprite[4] > enemy.y \
                    and round(self.mario.y) < enemy.y + enemy.sprite[4]:
                if enemy.dir:  # enemy change direction
                    enemy.dir = False
                else:
                    enemy.dir = True
                self.restart()  # we restart the game

        elif type(
                enemy) == Turtle and enemy.third_time:  # if the enemy is dead but it is a turtle and it is the third time mario touches it, them Mario dies also because it implies that the turtle is being shot now
            if ((round(self.mario.x + self.mario.sprite[3]) - enemy.x + self.progress) >= 0 and (
                    round(self.mario.x) - (enemy.x + enemy.sprite[3]) + self.progress) <= 0 \
                and round(self.mario.y) + self.mario.sprite[4] > enemy.y \
                and round(self.mario.y) < enemy.y + enemy.sprite[4]) or self.mario.in_the_enemy():
                if enemy.dir:  # enemy change direction
                    enemy.dir = False
                else:
                    enemy.dir = True
                self.restart()  # we restart the game

        if type(enemy) == Turtle and enemy.shot and not self.mario.in_the_enemy():
            enemy.third_time = True

    def interaction_with_enemies(self):
        # this function moves the enemies, see if a enemy touches/kills a Mario and also if Mario is killing a enemy
        for enemy in self.enemies:
            self.enemies_gravity(enemy)
            enemy.move(self.progress)  # enemy will move if he is alive (evaluated inside the function move of enemy)
            # 1º Part, Mario kills the enemies
            self.mario_kill_enemies(enemy)
            # 2º Part. Enemies kills Mario
            self.enemy_kill_mario(enemy)

    def restart(self,rematch=False):  # if completely = True, the game restart completely, mario has 3 lives as beginning
        # reset the proper parameters
        self.mario.sprite = [0, 48, 16, 16, 16]  # mario returns to its normal size
        self.enemies = []
        if self.mario.big_mario:
            self.mario.big_mario = False
            self.mario.y += 16
        else:
            self.big_x = self.width
            self.mario.lives -= 1
            self.mario.score = 0
            self.mario.x = self.width / 2
            self.mario.y = 210
            self.mario.enemies = self.enemies
            self.mario.previous_progress = 0
            self.time_limit = 300
            self.beginning_time = time.time()
            self.mario.copy_special_objects = copy.deepcopy(self.special_objects)
            self.restart_enemies()
            self.restart_objects()

            if self.mario.lives == 0:
                self.game_over = True
            if rematch:
                self.mario.lives = 3
                self.game_over = False

            self.mario.obstacles = (self.obstacles)
            self.mario.copy_obstacles = copy.deepcopy(self.obstacles)

    def restart_enemies(self):
        for enemy in self.enemies:
            enemy.x = enemy.sprite[5]
            enemy.y = enemy.sprite[6]
            enemy.dir = enemy.sprite[7]
            enemy.alive = True
            enemy.sprite[
                3] = 16  # for now all enemies size are 16 *16, but it depends. If the size were not 16*16, we would have to use parameter to store this info
            enemy.sprite[4] = 16
            if type(enemy) == Turtle:
                enemy.shot = False
                enemy.second_time = False
                enemy.third_time = False
                enemy.sprite[1] = 0
    def restart_objects(self):
        for special_object in self.special_objects:
            special_object.sprite[3] = 16
            special_object.sprite[4] = 16
            special_object.x = special_object.sprite[5]
            special_object.y = special_object.sprite[6]

        for obstacle in self.obstacles:
            if type(obstacle) == Question:  # recover the external look of the question blocks
                obstacle.sprite[1] = obstacle.sprite[7]
                obstacle.sprite[2] = obstacle.sprite[8]
            if type(obstacle) == Brick:  # recover the bricks that might have been broken by mario
                obstacle.sprite[3] = 16
                obstacle.sprite[4] = 16

    def gravity_mario(self):
        if self.mario.in_the_ground() or self.mario.in_the_enemy():  # if mario in a object, he stop falling
            self.velocities[0] = 0
        else:  # otherwise he falls with acceleration
            self.velocities[0] += 0.18
            self.mario.y += self.velocities[0]
            time.sleep(0.001)

    def move_map(
            self):  # if mario x position is greater than half of the width of the board, we moves the map and increase the big_x
        if self.mario.x > (self.width / 2):
            self.big_x += (self.mario.x - (self.width / 2))
            self.mario.x = self.width / 2

    def print_mario(
            self):  # we print mario introducing all the datas: x,y,image bank, x and y in the image bank, width and height
        pyxel.blt(self.mario.x, self.mario.y, self.mario.sprite[0],
                  self.mario.sprite[1], self.mario.sprite[2], self.mario.sprite[3],
                  self.mario.sprite[4], colkey=12)

    def print_obstacles_and_special_objects_and_background_elements(self):
        for block in self.background_elements + self.special_objects + self.obstacles:
            if self.big_x >= block.sprite[
                4]:  # if big_x, the farest place of the map that is displacing so far is bigger than the x of the object, then it is displaced
                pyxel.blt(block.x - self.progress, block.y, block.sprite[0],
                          block.sprite[1], block.sprite[2], block.sprite[3],
                          block.sprite[4], colkey=12)

    def enemies_gravity(self, enemy):
        if enemy in self.enemies:
            if enemy.in_the_ground():
                self.velocities[self.enemies.index(enemy) + 1] = 0
            else:
                self.velocities[self.enemies.index(enemy) + 1] += 0.18

                enemy.y += self.velocities[self.enemies.index(enemy) + 1]

                time.sleep(0.001)

    def print_enemies(self):  # draw the enemies
        for enemy in self.enemies:
            if self.big_x >= enemy.sprite[4]:
                pyxel.blt(enemy.x - self.progress, enemy.y, enemy.sprite[0],
                          enemy.sprite[1], enemy.sprite[2], enemy.sprite[3],
                          enemy.sprite[4], colkey=12)
