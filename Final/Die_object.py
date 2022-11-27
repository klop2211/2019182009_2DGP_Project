from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Die:
    image = None
    def __init__(self, x, y, w, h):
        if Die.image == None:
            Die.image = load_image('./Resource/Effect/Die.png')
        self.frames = 11
        self.frame = 0
        self.x, self.y, self.w, self.h = x, y, w, h

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.frame >= self.frames:
            game_world.remove_object(self)

    def draw(self, c_x, c_y):
        sx, sy = self.x + c_x, self.y + c_y
        width = Die.image.w // self.frames
        Die.image.clip_draw_to_origin((int)(self.frame) * width, 0, width, Die.image.h, sx, sy, self.w, self.h)