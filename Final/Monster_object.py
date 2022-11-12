from pico2d import *
import game_framework
import play_state


class IDLE:
    def enter(self, event):
        self.frame %= self.frames['idle']
        print('ENTER IDLE')
        self.dir = 0
    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frames['idle']
    @staticmethod
    def draw(self, x, y):
        frame_size = self.idle.w // self.frames['idle']
        if self.face_dir == 1:
            self.idle.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 67 + x,
                                      self.y + 48 + y, 134, 96)
        else:
            self.idle.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h', self.x + 67 + x,
                                     self.y + 48 + y, 134, 96)

class SKILL:
    locate = [None, None]
    def enter(self, event):
        self.frame = 0
        SKILL.locate[0] = event[0]
        SKILL.locate[1] = event[1]
        print('ENTER SKILL')
    @staticmethod
    def exit(self, event):
        print('EXIT SKILL')
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == 7:
            self.x = SKILL.locate[0]
            self.y = SKILL.locate[1]
        if int(self.frame) == self.frames['skill']:
            self.cur_state.exit(self, None)
            self.cur_state = MOVE
            self.cur_state.enter(self, None)

    @staticmethod
    def draw(self, x, y):
        frame_size = self.skill.w // self.frames['skill']
        if self.face_dir == 1:
            self.skill.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 67 + x,
                                      self.y + 48 + y, 134, 96)
        else:
            self.skill.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h', self.x + 67 + x,
                                     self.y + 48 + y,134, 96)

class MOVE:
    def enter(self, event):
        self.frame = 0
        print('ENTER MOVE')
    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frames['move']
        self.set_dir()
        self.x += self.dir * 5 * PIXEL_PER_METER * game_framework.frame_time
    @staticmethod
    def draw(self, x, y):
        frame_size = self.move.w // self.frames['move']
        if self.dir == 1:
            self.move.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 67 + x,
                                      self.y + 48 + y,134, 96)
        else:
            self.move.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h', self.x + x,
                                     self.y + 48 + y, 134, 96)

class ATTACK:
    def enter(self, event):
        self.frame = 0
        print('ENTER MOVE')
    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if int(self.frame) == self.frames['attack']:
            self.cur_state.exit(self, None)
            self.cur_state = MOVE
            self.cur_state.enter(self, None)
    @staticmethod
    def draw(self, x, y):
        frame_size = self.attack.w // self.frames['attack']
        if self.dir == 1:
            self.attack.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 67 + x,
                                      self.y + 48 + y, 134, 96)
        else:
            self.attack.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h', self.x  + x,
                                     self.y + 48 + y, 134, 96)

PIXEL_PER_METER = 40
RUN_SPEED_MPS = 5
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Monster:
    pass



class Biggrayskul(Monster):
    idle = None
    attack = None
    move = None
    skill = None

    def __init__(self, x, y, power):
        self.x, self.y, self.power = x, y, power
        self.frames = {'idle': 8, 'attack': 13, 'move': 6, 'skill': 13}
        self.face_dir = 1
        self.dir = 0
        self.frame = 0
        if Biggrayskul.idle == None:
            Biggrayskul.idle = load_image('./Resource/BigGrayIceSkel/BigGrayIceSkelIdle.png')
            Biggrayskul.attack = load_image('./Resource/BigGrayIceSkel/BigGrayIceSkelAttack.png')
            Biggrayskul.move = load_image('./Resource/BigGrayIceSkel/BigGrayIceSkelMove.png')
            Biggrayskul.skill = load_image('./Resource/BigGrayIceSkel/BigGrayIceSkelSkill.png')
        self.idle = Biggrayskul.idle
        self.attack = Biggrayskul.attack
        self.move = Biggrayskul.move
        self.skill = Biggrayskul.skill
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def get_bb(self):
        if self.cur_state == IDLE:
            return self.x - 200, self.y - 200, self.x + 200, self.y + 200
        elif self.cur_state == SKILL:
            return self.x - 20, self.y - 48, self.x + 20, self.y + 48
        elif self.cur_state == MOVE:
            return self.x, self.y, self.x + 67, self.y + 96
        elif self.cur_state == ATTACK:
            return self.x, self.y, self.x + 134, self.y + 96

    def set_dir(self):
        if self.x - play_state.hero.x > 15 or self.x - play_state.hero.x < -15:
            if self.x - play_state.hero.x > 0:
                self.dir = -1
            else:
                self.dir = 1


    def handle_collision(self, other, group):
        if group == 'hero:biggrayskel':
            if self.cur_state == IDLE:
                locate = other.x, other.y
                self.cur_state.exit(self, None)
                self.cur_state = SKILL
                self.cur_state.enter(self, locate)
            if self.cur_state == MOVE:
                self.cur_state.exit(self, None)
                self.cur_state = ATTACK
                self.cur_state.enter(self, None)
        if group == 'biggrayskel:block':
            if self.cur_state != IDLE:
                self.y = clamp(other.top * 40, self.y, 660)

    def update(self):
        self.cur_state.do(self)
        if self.cur_state != IDLE:
            self.y -= 10 * PIXEL_PER_METER * game_framework.frame_time

    def draw(self, x, y):
        self.cur_state.draw(self, x, y)
        # draw_rectangle(self.x + x, self.y + y, self.x + 67 + x, self.y + 96 + y)


