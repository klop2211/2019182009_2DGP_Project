from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = 40
RUN_SPEED_MPS = 5
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

class Bullet:
    image = None

    def __init__(self, x = 800, y = 300, dx = 0, dy = 0, power=0):
        if Bullet.image == None:
            Bullet.image = load_image('./Resource/Weapon/Bullet10.png')
        self.x, self.y, self.dx, self.dy, self.power = x, y, dx, dy, power
        self.speed = 20
        self.state = 'live'
        self.destroy_time = 0.1

    def draw(self, x, y):
        if self.dx == -1:
            self.image.clip_composite_draw(0, 0, self.image.w, self.image.h, 1.57, ' ', self.x + x + 20, self.y + y + 20, 15, 15)
        else:
            self.image.clip_composite_draw(0, 0, self.image.w, self.image.h, 1.57, 'h', self.x + x + 20,
                                           self.y + y + 20, 15, 15)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def update(self):
        self.x += self.dx * self.speed * PIXEL_PER_METER * game_framework.frame_time
        self.y += self.dy * self.speed * PIXEL_PER_METER * game_framework.frame_time
        if self.state == 'destroy':
            self.destroy_time -= game_framework.frame_time
        if self.destroy_time <= 0:
            game_world.remove_object(self)
        if self.x < 20 or self.x > 1180:
            game_world.remove_object(self)
        if self.y < 60 or self.y > 720:
            game_world.remove_object(self)

    def handle_collision(self, other, group):
        if self.state == 'live':
            if group == 'effect:monster':
                other.hp -= max(self.power - other.defense, 0)
                print(other.hp)
                self.state = 'destroy'
            if group == 'effect:boss' and other.invincible <= 0:
                other.hp -= max(self.power - other.defense, 0)
                print(other.hp)
                self.state = 'destroy'


