"""
:author: Daniel Zanón Lopez/DaniDaniel09
"""


# The code is importing necessary modules and classes for implementing a server for a multiplayer game
# of Snake using sockets and the `select` module for I/O multiplexing. The `socket` module provides
# low-level network communication functionality, `select` module provides I/O multiplexing, `time`
# module provides time-related functions, `argparse` module provides a way to parse command-line
# arguments, and `Game` is a class representing a game of Snake.
import socket
import select
import time
import argparse

from game import Game

def arg_parse():
    """
    The function defines an argument parser with default values for width, height, and port, and returns
    the parsed arguments.
    :return: The function `arg_parse()` is returning the parsed arguments from the command line. It uses
    the `argparse` module to define and parse the arguments. The default values for the arguments are
    set to `20` for `width`, `10` for `height`, and `9999` for `port`. The parsed arguments are returned
    as an object with attributes corresponding to the argument names.
    """
    parser = argparse.ArgumentParser()
   
    parser.add_argument("--width", dest = 'width', help = "Field width", default = 20, type = int)
    parser.add_argument("--height", dest = 'height', help = "Field height", default = 10, type = int)
    parser.add_argument("--port", dest = 'port', help = "port", default = 9999, type = int)
    
    return parser.parse_args()

def disconnect_player(epoll, connections, snek_game, socket_to_id, fileno):
    """
    This function disconnects a player from a game and removes their connection and ID from relevant
    data structures.
    
    :param epoll: An instance of the `select.epoll()` class used for I/O multiplexing
    :param connections: A dictionary that maps file descriptors to socket objects representing
    connections to clients
    :param snek_game: It is likely an instance of a class representing a game of Snake, which may
    include information about the game board, the players, and their scores
    :param socket_to_id: A dictionary that maps socket file descriptors to player IDs
    :param fileno: fileno is a file descriptor, which is a unique identifier for an open file or socket.
    In this context, it is used to identify the specific socket connection that needs to be disconnected
    """
    epoll.unregister(fileno)
    connections[fileno].close()
    del connections[fileno]

    if socket_to_id[fileno] in snek_game.players:
        del snek_game.players[socket_to_id[fileno]]

    del socket_to_id[fileno]


# The code is implementing a server for a multiplayer game of Snake using sockets and the `select`
# module for I/O multiplexing. The `with` statement is used to create a socket object `server_socket`
# using the `socket.socket()` method with the `AF_INET` and `SOCK_STREAM` arguments. The `arg_parse()`
# function is called to parse command line arguments for the width, height, and port of the game
# field. The `server_socket` is then configured with the `setsockopt()` method to allow reuse of the
# address and bound to the specified host and port using the `bind()` method. The `listen()` method is
# called to start listening for incoming connections with a backlog of 5.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    args = arg_parse()
    
    host = '127.0.0.1'
    port = args.port

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    width, height = args.width, args.height

    snek_game = Game()
    snek_game.set_field_size(width, height)

    counter = 0

    epoll = select.epoll()
    epoll.register(server_socket.fileno(), select.EPOLLIN)
    connections = {}
    socket_to_id = {}

    while True:
        snek_game.run_step()
        events = epoll.poll(1)

        for fileno, event in events:
            if fileno == server_socket.fileno():
                connection, address = server_socket.accept()
                connection.setblocking(False)
                connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLOUT)

                connections[connection.fileno()] = connection

                snek_game.add_fruit()
                snek_game.add_player(counter)

                socket_to_id[connection.fileno()] = counter

                connection.send("{0} {1} {2}".format(width, height, counter).encode('ascii'))

                counter += 1
            elif event & select.EPOLLIN:
                client_socket = connections[fileno]

                res = client_socket.recv(3).decode('ascii')

                if res == '':
                    disconnect_player(epoll, connections, snek_game, socket_to_id, fileno)
                else:
                    res = [int(item) for item in res.strip().split(' ')]

                    snek_game.handle_events(res[0], res[1])
            elif event & select.EPOLLOUT:
                client_socket = connections[fileno]

                id = socket_to_id[fileno]

                if id not in snek_game.players:  # Collided with self or bounds
                    # Telling client to disconnect, at next iteration we
                    # will delete its information
                    client_socket.send(' -1'.encode('ascii'))
                    continue

                # Sending fruit and player positions
                msg = "{0}!{1}".format(
                    '?'.join([str(fruit) for fruit in snek_game.fruits]),
                    '?'.join(['{0}: {1}'.format(str(id), str(player.body)) for id, player in snek_game.players.items()])
                    ).encode('ascii')

                length = str(len(msg)).zfill(3).encode('ascii')

                client_socket.send(length)
                client_socket.send(msg)

        time.sleep(snek_game.frame_time)
