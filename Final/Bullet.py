from pico2d import *
import game_world

class Bullet:
    image = None

    def __init__(self, x = 800, y = 300, dx = 0, dy = 0):
        if Bullet.image == None:
            Bullet.image = load_image('./Resource/Weapon/Bullet10.png')
        self.x, self.y, self.dx, self.dy = x, y, dx, dy

    def draw(self, x, y):
        if self.face_dir == -1:
            self.image.clip_composite_draw(0, 0, self.image.w, self.image.h, 1.57, ' ', self.x + x + 20, self.y + y + 20, 15, 15)
        else:
            self.image.clip_composite_draw(0, 0, self.image.w, self.image.h, 1.57, 'h', self.x + x + 20,
                                           self.y + y + 20, 15, 15)

    def update(self):

        if self.x < 20 or self.x > 1180:
            game_world.remove_object(self)
