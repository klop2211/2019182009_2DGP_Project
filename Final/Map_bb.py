
class Map_bb:

    def __init__(self, l, b, r, t):
        self.left, self.bottom, self.right, self.top = l, b, r, t

    def draw(self, x, y):
        pass

    def get_bb(self):
        return self.left * 40, self.bottom * 40, self.right * 40, self.top * 40

    def update(self):
        pass


# 측면 벽
class Wall(Map_bb):

    def handle_collision(self, other, group):
        pass


# 발판, 바닥
class Block(Map_bb):

    def handle_collision(self, other, group):
        pass


# 문
class Door(Map_bb):

    def handle_collision(self, other, group):
        pass

