class Player:
    def __init__(self, id, x, y):
        self.id = id
        
        self.velocity = (0, 0)
        self.body = [(x, y)]
        
        self.score = 0
        
    def set_velocity(self, v_x, v_y):
        new_velocity = (v_x, v_y)

        if len(self.body) > 1:
            if (self.body[0][0]+v_x, self.body[0][1]+v_y)  == self.body[1]:
                return

        self.velocity = (v_x, v_y)
        
    def grow_tail(self):
        self.body.append(self.body[-1])
        
    def move(self):
        if self.velocity == (0,0):
            return
        
        n = len(self.body)
        
        if (n > 1):
            self.body[n-1:0:-1] = self.body[n-2::-1]    #shift body
        self.body[0] = (self.body[0][0] + self.velocity[0], self.body[0][1] + self.velocity[1])
        
    def eat_fruit(self):
        self.score += 10