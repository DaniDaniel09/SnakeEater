import socket

import pygame
from pygame.locals import *
from player import Player
from render import Render

def hangle_input():
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    v = 0
    
    if (keys[K_RIGHT]):
        v = 1

    if (keys[K_LEFT]):
        v = 2

    if (keys[K_UP]):
        v = 3

    if (keys[K_DOWN]):
        v = 4

    if (keys[K_ESCAPE]):
        running = False
        
    return v


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname()                           
port = 9999
s.connect((host, port))                               

# some sort of menu

render = Render()
render.set_window_size(10,10)

running = True
while running:
    v = hangle_input()
    s.send(v)
    

#msg = s.recv(1024)                                     

s.close()
#print (msg.decode('ascii'))
