from pico2d import *

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        self.x -= dx
        if self.x <= -400:
            self.x = -400
        elif self.x >= 0:
            self.x = 0
        self.y -= dy
        if self.y <= -200:
            self.y = -200
        elif self.y >= 0:
            self.y = 0

    def update(self, hero):
        dx, dy = hero.x + self.x + 20, hero.y + self.y + 20
        self.move(-(400 - dx), -(300 - dy))

    def draw(self):
        pass

camera = Camera()
