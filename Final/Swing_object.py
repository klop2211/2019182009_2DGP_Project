import random
import game_framework
import game_world
from pico2d import *


def rotate(x, y, rad):
    return x * math.cos(rad) - y * math.sin(rad), x * math.sin(rad) + y * math.cos(rad)


class Sword_Swing():
    image = None
    sound = []

    def __init__(self, x, y, dir, power=0):
        if Sword_Swing.image == None:
            Sword_Swing.image = load_image('./Resource/Weapon/SwordSwing.png')
            Sword_Swing.sound.append(load_wav('./Resource/Audio/swing.wav'))
            Sword_Swing.sound.append(load_wav('./Resource/Audio/swing0.wav'))
            Sword_Swing.sound.append(load_wav('./Resource/Audio/swing1.wav'))
            Sword_Swing.sound.append(load_wav('./Resource/Audio/swing3.wav'))
            for sound in Sword_Swing.sound:
                sound.set_volume(80)
        Sword_Swing.sound[random.randint(0, 3)].play(1)
        self.x, self.y, self.dir, self.power = x, y, dir - 1.57, power
        self.frame = 0
        self.frames = 3
        self.w, self.h = Sword_Swing.image.w // self.frames * 4, Sword_Swing.image.h * 4
        self.state = 'live'
        self.destroy_time = 0.4

    def update(self):
        if self.state == 'destroy':
            self.destroy_time -= game_framework.frame_time
        if self.destroy_time <= 0:
            game_world.remove_object(self)
        self.frame = (self.frame + self.frames * 3 * game_framework.frame_time)
        if self.frame >= 3:
            game_world.remove_object(self)

    def draw(self, x, y):
        sx, sy = self.x + x, self.y + y
        frame_size = Sword_Swing.image.w // self.frames
        Sword_Swing.image.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, Sword_Swing.image.h, self.dir, '', sx, sy, self.w, self.h)

    def get_bb(self):
        return self.x - self.w // 2, self.y - self.h // 2, self.x + self.w // 2, self.y + self.h // 2

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


class Saber_Swing:
    image = None
    sound = []
    def __init__(self, x, y, dir, power=0):
        if Saber_Swing.image == None:
            Saber_Swing.image = load_image('./Resource/Weapon/SaberSwing.png')
            Saber_Swing.sound.append(load_wav('./Resource/Audio/swing.wav'))
            Saber_Swing.sound.append(load_wav('./Resource/Audio/swing0.wav'))
            Saber_Swing.sound.append(load_wav('./Resource/Audio/swing1.wav'))
            Saber_Swing.sound.append(load_wav('./Resource/Audio/swing3.wav'))
            for sound in Saber_Swing.sound:
                sound.set_volume(80)
        Saber_Swing.sound[random.randint(0, 3)].play(1)
        self.x, self.y, self.dir, self.power = x, y, dir, power
        self.frame = 0
        self.frames = 7
        self.w, self.h = Saber_Swing.image.w // self.frames * 4, Saber_Swing.image.h * 4
        self.state = 'live'
        self.destroy_time = 0.4

    def update(self):
        if self.state == 'destroy':
            self.destroy_time -= game_framework.frame_time
        if self.destroy_time <= 0:
            game_world.remove_object(self)
        self.frame = (self.frame + self.frames * 3 * game_framework.frame_time)
        if self.frame >= self.frames:
            game_world.remove_object(self)

    def draw(self, x, y):
        sx, sy = self.x + x, self.y + y
        frame_size = Saber_Swing.image.w // self.frames
        if math.cos(self.dir) >= 0:
            Saber_Swing.image.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, Saber_Swing.image.h,
                                                  0, ' ', sx, sy, self.w, self.h)
        else:
            Saber_Swing.image.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, Saber_Swing.image.h,
                                                  0, 'h', sx, sy, self.w, self.h)

    def get_bb(self):
        return self.x - self.w // 2, self.y - self.h // 2, self.x + self.w // 2, self.y + self.h // 2

    def handle_collision(self, other, group):
        if self.state == 'live':
            if group == 'effect:monster':
                other.hp -= max(self.power - other.defense, 0)
                self.state = 'destroy'
            if group == 'effect:boss' and other.invincible <= 0:
                other.hp -= max(self.power - other.defense, 0)
                self.state = 'destroy'
