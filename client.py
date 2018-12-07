import socket

import pygame
from pygame.locals import *
from player import Player
from render import Render


def handle_input():
    global running

    pygame.event.pump()
    keys = pygame.key.get_pressed()
    v = 0

    if keys[K_RIGHT]:
        v = 1

    if keys[K_LEFT]:
        v = 2

    if keys[K_UP]:
        v = 3

    if keys[K_DOWN]:
        v = 4

    if keys[K_ESCAPE]:
        running = False

    return v


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    global running
    host = socket.gethostname()
    port = 9999

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.connect((host, port))

    # some sort of menu

    arr = server_socket.recv(7).decode('ascii').strip().split(' ')
    arr = [int(item) for item in arr]

    print(arr)

    render = Render()
    render.set_window_size(arr[0], arr[1])

    id = arr[2]

    input_result = 0
    running = True

    while running:
        input_result, prev_result = handle_input(), input_result

        if input_result and input_result != prev_result:
            server_socket.send('{id} {state}'.format(id=id, state=input_result).encode('ascii'))

        length = int(server_socket.recv(3).decode('ascii'))

        if length == -1:
            running = False
            break

        r = server_socket.recv(length).decode('ascii')

        # ! splits fruits and players arrays

        r = r.split('!')

        # ? splits each fruit and each player from each other

        fruit_strings = r[0].split('?')
        players_strings = r[1].split('?')

        # Splitting tuple-strings into two integers
        fruit_strings = [fruit.strip('()').split(',') for fruit in fruit_strings]
        fruits = [(int(fruit[0]), int(fruit[1])) for fruit in fruit_strings]

        # : splits keys (player ids) and values (bodies)
        players_strings = [player.split(': ') for player in players_strings]

        # splitting body strings into array of strings 'a, b'
        players_strings = {int(player[0]): player[1].strip('[()]').split('), (') for player in players_strings}

        # converting 'a, b' into tuples
        players_strings = {key: [item.split(',') for item in value] for key, value in players_strings.items()}
        players_strings = {key: [(int(item[0]), int(item[1])) for item in value] for key, value in
                           players_strings.items()}

        players = {id: Player.construct_player(id, body) for id, body in players_strings.items()}

        render.draw(players, fruits)

print('Game over, boi')
