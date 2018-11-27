from pygame.locals import *
import pygame

class Render:
    unit_size = 32
    windowWidth = 600
    windowHeight = 400
    
    def __init__(self):
        self.display = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('SnakeEater')
        
        self.snek_image = pygame.Surface((self.unit_size, self.unit_size))
        self.snek_image.fill((255, 0, 0))
        
        self.fruit_image = pygame.Surface((self.unit_size, self.unit_size))
        self.fruit_image.fill((0, 255, 0))

    def set_window_size(self, w, h, unit_size=32):
        self.unit_size = unit_size
        self.windowWidth = w*self.unit_size
        self.windowHeight = h*self.unit_size
        self.display = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
    
    def draw_menu(self):
        pass
    
    def draw(self, players, fruits):
        self.display.fill((0,0,0))
        
        for player in players:
            for point in player.body:
                self.display.blit(self.snek_image, (point[0]*self.unit_size, point[1]*self.unit_size))
            
        for fruit in fruits:
            self.display.blit(self.fruit_image, (fruit[0]*self.unit_size, fruit[1]*self.unit_size))
        
        pygame.display.update()