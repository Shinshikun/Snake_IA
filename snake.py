class Snake:

    def __init__(self, spd=15, pos=[100,100]):
        self.spd = spd
        self.len = 4  
        self.pos = pos
        self.body = [[70,100], [80,100], [90,100], [100,100]]

    def move_up(self):
        self.pos[1] -= 10
        self.update()

    def move_down(self):
        self.pos[1] += 10
        self.update()

    def move_right(self):
        self.pos[0] += 10
        self.update()

    def move_left(self):
        self.pos[0] -= 10
        self.update()

    def update(self):
        self.body.pop(0)
        self.body.append(self.pos.copy())

    def add_body(self):
        self.body = [self.body[0],*self.body]