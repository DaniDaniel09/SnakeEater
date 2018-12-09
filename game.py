import time
from random import randint
import pygame
from pygame.locals import *
from player import Player
from render import Render


# TODO:  1) render to client
#        2) handle_event - handle msgs instead of pygame events

class Game:
    update_time = 0.5
    frame_time = 0.1

    players = {}
    fruits = []
    leaderboard = {}

    def __init__(self):
        pygame.init()
        self.step_num = 0
        self.width = 0
        self.height = 0

    def set_field_size(self, w, h):
        self.width = w
        self.height = h

    def add_player(self, id):
        x = randint(0, self.width - 1)
        y = randint(0, self.height - 1)
        self.players[id] = Player(id, x, y)

    def add_fruit(self):
        x = randint(0, self.width - 1)
        y = randint(0, self.height - 1)
        self.fruits.append((x, y))

    def check_collisions(self):
        player_array = self.players.copy().items()

        for i, player in player_array:
            head = player.body[0]

            if head in player.body[1::]:
                self.leaderboard[self.players[i].id] = self.players[i].score
                del self.players[i]
                print("Collided with self")

            if (head[0] < 0 or head[0] >= self.width or
                    head[1] < 0 or head[1] >= self.height):
                self.leaderboard[self.players[i].id] = self.players[i].score
                del self.players[i]
                print("Collided with bounds:")

            if head in self.fruits:
                self.players[i].eat_fruit()
                self.players[i].grow_tail()  # this may put tail on top of the head
                self.fruits.remove(head)
                self.add_fruit()

            for j, p in player_array:
                if j == i:
                    continue

                for index, segment in p.body:
                    if head == segment and j < i:
                        for k in range(len(p.body) - index):
                            self.players[i].grow_tail()

                        if index == 0:
                            del self.players[p.id]
                        else:
                            self.players[p.id].body = self.players[p.id].body[:index]

    def update(self):
        for i, player in self.players.items():
            self.players[i].move()

    def handle_events(self, id, key):
        left, right, up, down = 1, 2, 3, 4

        if key == left:
            self.players[id].set_velocity(1, 0)

        if key == right:
            self.players[id].set_velocity(-1, 0)

        if key == up:
            self.players[id].set_velocity(0, -1)

        if key == down:
            self.players[id].set_velocity(0, 1)

        print(key)

    def run_step(self):
        self.step_num += 1

        if self.step_num * self.frame_time == self.update_time:
            self.step_num = 0
            self.update()
            self.check_collisions()

            if len(self.players) == 0:  # game is over when there are no players left
                return False

        return True
