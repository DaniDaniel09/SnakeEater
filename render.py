"""
:author: Daniel Zanón Lopez/DaniDaniel09
"""

# The code is importing the Pygame library and its local modules. The `*` symbol is used to import all
# the constants and functions defined in the Pygame.locals module. This allows the code to use Pygame
# functions and constants without having to prefix them with the module name. The `pygame` module is
# also imported separately, which is necessary to use Pygame functions and classes.
from pygame.locals import *
import pygame

class Render:
# The code is defining three class-level variables `unit_size`, `windowWidth`, and `windowHeight`.
# `unit_size` is set to 5, while `windowWidth` and `windowHeight` are set to 600 and 400 respectively.
# These variables are used to determine the size of the game window and the size of the snake and
# fruit images that will be displayed on the window.
    unit_size = 5
    windowWidth = 600
    windowHeight = 400
    
    def __init__(self):
        """
        The function initializes the game display and creates surfaces for the snake and fruit images.
        """
        self.display = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption('SnakeEater')
        
        self.snek_image = pygame.Surface((self.unit_size, self.unit_size))
        self.snek_image.fill((255, 0, 0))
        
        self.fruit_image = pygame.Surface((self.unit_size, self.unit_size))
        self.fruit_image.fill((0, 255, 0))

    def set_window_size(self, w, h):
        """
        This function sets the size of the Pygame display window based on the given width and height
        parameters multiplied by a unit size.
        
        :param w: The width of the game window in units
        :param h: The parameter "h" represents the desired height of the game window in terms of the
        number of units. The actual height of the window will be calculated by multiplying the unit size
        by the value of "h"
        """
        #self.unit_size = unit_size
        self.windowWidth = w*self.unit_size
        self.windowHeight = h*self.unit_size
        self.display = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
    
    def draw_menu(self):
        """
        The function "draw_menu" is defined but does not contain any code.
        """
        pass
    
    def draw(self, players, fruits):
        """
        This function draws the players and fruits on the game display using Pygame library.
        
        :param players: A dictionary containing information about all the players in the game. The keys
        are unique identifiers for each player, and the values are objects that contain information
        about the player's current state (such as their position and direction)
        :param fruits: The `fruits` parameter is a list of tuples representing the coordinates of each
        fruit in the game. Each tuple contains two integers, the x and y coordinates of the fruit on the
        game board
        """
        self.display.fill((0,0,0))
        
        for player in players.values():
            for point in player.body:
                self.display.blit(self.snek_image, (point[0]*self.unit_size, point[1]*self.unit_size))
            
        for fruit in fruits:
            self.display.blit(self.fruit_image, (fruit[0]*self.unit_size, fruit[1]*self.unit_size))
        
        pygame.display.update()