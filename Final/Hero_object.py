from pico2d import *

# 주인공 : 크기 (40,40)
class Hero:
    def __init__(self):
        self.idle_left = load_image('./Resource/Char/CharIdle_L.png')
        self.idle_right = load_image('./Resource/Char/CharIdle_R.png')
        self.run_left = load_image('./Resource/Char/CharRun_L.png')
        self.run_right = load_image('./Resource/Char/CharRun_R.png')
        self.jump_right = load_image('./Resource/Char/CharJump_R.png')
        self.jump_left = load_image('./Resource/Char/CharJump_L.png')
        self.die = load_image('./Resource/Char/CharDie.png')
        self.hand = load_image('./Resource/Char/CharHand0.png')
        self.x = 400
        self.y = 300
        self.frame = 0
        self.frames = {'run': 8, 'idle': 5}
        self.status = {'speed': 10, 'jump': 5}
        # 오른쪽 : 1, 왼쪽 : -1
        self.dir = 1
        self.state = {'run': False, 'jump': 0, 'dash': False, 'die': False}

    def draw(self, x, y):
        # # dash
        # if self.state['dash']:
        #     frame_size = self.run_right.w // self.frames['run']
        #     if self.dir == 1:
        #         self.run_right.clip_draw(0, 0, frame_size, self.run_right.h, self.x + 20, self.y + 20, 40, 40)
        #     else:
        #         self.run_left.clip_draw(0, 0, frame_size, self.run_left.h, self.x + 20, self.y + 20, 40, 40)
        #     return
        # # jump
        # if self.state['jump']:
        #     if self.dir == 1:
        #         self.jump_right.clip_draw(0, 0, self.jump_right.w, self.jump_right.h, self.x + 20, self.y + 20, 40, 40)
        #     else:
        #         self.jump_left.clip_draw(0, 0, self.jump_left.w, self.jump_left.h, self.x + 20, self.y + 20, 40, 40)
        #     return
        # run
        if self.state['run']:
            frame_size = self.run_right.w // self.frames['run']
            if self.dir == 1:
                self.run_right.clip_draw(frame_size * self.frame, 0, frame_size, self.run_right.h, self.x + 20 + x, self.y + 20 + y, 40, 40)
            else:
                self.run_left.clip_draw(frame_size * self.frame, 0, frame_size, self.run_left.h, self.x + 20+ x, self.y + 20 + y, 40, 40)
            self.frame += 1
            self.frame %= self.frames['run']
            return
        # idle
        frame_size = self.idle_left.w // self.frames['idle']
        if self.dir == 1:
            self.idle_right.clip_draw(frame_size * self.frame, 0, frame_size, self.idle_right.h, self.x + 20+ x, self.y + 20 + y, 40, 40)
        else:
            self.idle_left.clip_draw(frame_size * self.frame, 0, frame_size, self.idle_left.h, self.x + 20+ x, self.y + 20 + y, 40, 40)
        self.frame += 1
        self.frame %= self.frames['idle']
        return

    def update(self):
        delay(0.05)
        # 중력
        self.y -= 10
        # 좌우 이동
        if self.state['run']:
            self.x += self.status['speed'] * self.dir

