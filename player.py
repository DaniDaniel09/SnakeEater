"""
:author: Daniel Zanón Lopez/DaniDaniel09
"""

class Player:

    def construct_player(id, body):
        """
        The function constructs a player object with a given id and body.
        
        :param id: The id parameter is an identifier for the player being constructed. It could be a unique
        identifier such as a username or a numerical ID
        :param body: The "body" parameter in the "construct_player" function is likely referring to the
        physical representation of the player in the game, such as an image or a sprite. It is not clear
        from the code snippet what the "id" parameter represents, but it is likely some sort of identifier
        for the
        :return: The function `construct_player` is returning an instance of the `Player` class with the
        specified `id`, `0` for the `x` coordinate, `0` for the `y` coordinate, and the `body` parameter
        passed to the function as the `body` attribute of the player object.
        """
        player = Player(id, 0, 0)

        player.body = body

        return player

    def __init__(self, id, x, y):
        """
        This is a constructor function that initializes the attributes of an object with an id, velocity,
        body, and score.
        
        :param id: The id parameter is used to uniquely identify an instance of the class. It is typically a
        string or an integer value
        :param x: The x-coordinate of the initial position of the object
        :param y: The parameter "y" represents the initial y-coordinate of the object's position in a 2D
        coordinate system
        """
        self.id = id

        self.velocity = (0, 0)
        self.body = [(x, y)]

        self.score = 0

    def set_velocity(self, v_x, v_y):
        """
        This function sets the velocity of an object, but checks if the new velocity would cause the object
        to collide with its own body.
        
        :param v_x: The velocity in the x-direction. This parameter determines how much the snake's head
        will move horizontally in each game tick
        :param v_y: v_y is the velocity in the y-direction, which determines the speed and direction of
        movement of an object along the vertical axis
        :return: If the condition in the if statement is True, then nothing is returned (the function ends).
        If the condition is False, then the velocity is set to (v_x, v_y) and nothing is returned (the
        function ends).
        """
        if len(self.body) > 1:
            if (self.body[0][0] + v_x, self.body[0][1] + v_y) == self.body[1]:
                return

        self.velocity = (v_x, v_y)

    def grow_tail(self):
        """
        This function adds a new element to the end of a list by duplicating the last element.
        """
        self.body.append(self.body[-1])
        
    def cut_at(self, index):
        """
        The "cut_at" function cuts the "body" attribute of an object up to a specified index.
        
        :param index: The index parameter is an integer that represents the position in the string where the
        cut should be made. The method `cut_at` takes this index as input and cuts the string stored in the
        `body` attribute of the object up to that index. The resulting string is then stored back in the `
        """
        self.body = self.body[:index]

    def move(self):
        """
        This function moves the snake's body by shifting its positions and updating its velocity.
        :return: If the velocity of the snake is (0, 0), then nothing is being returned and the function
        ends. If the velocity is not (0, 0), then the function updates the position of the snake's body
        based on its velocity and returns nothing.
        """
        if self.velocity == (0, 0):
            return

        n = len(self.body)

        if n > 1:
            self.body[n - 1:0:-1] = self.body[n - 2::-1]  # shift body
        self.body[0] = (self.body[0][0] + self.velocity[0], self.body[0][1] + self.velocity[1])

    def eat_fruit(self):
        """
        The function "eat_fruit" increases the score by 10.
        """
        self.score += 10
