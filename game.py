import time
from random import randint
import pygame
from pygame.locals import *
from player import Player
from render import Render


#TODO:  1) render to client
#       2) handle_event - hangle msgs instead of pygame events


class Game:
    update_time = 0.5
    frame_time = 0.1
    
    players = []
    fruits = []
    leaderboard = {}

    def __init__(self):
        pygame.init()
        self.render = Render()
    
    def set_field_size(self, w, h):
        self.width = w
        self.heigth = h
        self.render.set_window_size(10,10)

    def add_player(self, id):
        x = randint(0, self.width-1)
        y = randint(0, self.heigth-1)
        self.players.append(Player(id, x, y))
        
    def add_fruit(self):
        x = randint(0, self.width-1)
        y = randint(0, self.heigth-1)
        self.fruits.append((x,y))

    def check_collisions(self):
        for i,player in enumerate(self.players):
            head = player.body[0]
                
            if head in player.body[1::]:
                self.leaderboard[self.players[i].id] = self.players[i].score
                del self.players[i]
                print("Collided with self")
                
            if (head[0] < 0 or head[0] >= self.width or
                head[1] < 0 or head[1] >= self.heigth):
                self.leaderboard[self.players[i].id] = self.players[i].score
                del self.players[i]
                print("Collided with bounds:")
                
            if head in self.fruits:
                self.players[i].eat_fruit()
                self.players[i].grow_tail() # this may put tail on top of the head
                self.fruits.remove(head)
                self.add_fruit()

    def update(self):
        for i,player in enumerate(self.players):
            self.players[i].move()
    
    def handle_events(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        
        if (keys[K_RIGHT]):
            self.players[0].set_velocity(1, 0)

        if (keys[K_LEFT]):
            self.players[0].set_velocity(-1, 0)

        if (keys[K_UP]):
            self.players[0].set_velocity(0, -1)

        if (keys[K_DOWN]):
            self.players[0].set_velocity(0, 1)

        if (keys[K_ESCAPE]):
            self.running = False
    
    def run(self):
        self.running = True
        
        self.add_player(id=1)
        self.add_fruit()
        self.render.draw(self.players, self.fruits)
        
        i = 0
        while self.running:          
            i += 1
            
            self.handle_events()
            
            if (i * self.frame_time == self.update_time):
                i = 0
                self.update()
                self.check_collisions()
                
                if len(self.players) == 0:  #game is over when ther's no players left
                    break
                
                self.render.draw(self.players, self.fruits)
            
            time.sleep(self.frame_time)
        print("Game's over.")
        print(self.leaderboard)
        pygame.quit()
        
if __name__ == "__main__" :
    game = Game()
    game.set_field_size(10, 10)
    game.run()