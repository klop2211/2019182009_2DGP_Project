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
