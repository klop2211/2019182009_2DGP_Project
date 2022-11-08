from pico2d import *

aD, dD, aU, dU, TIMER, SPACE, SHIFT = range(7)
key_event_table = {
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_a): aD,
    (SDL_KEYDOWN, SDLK_d): dD,
    (SDL_KEYUP, SDLK_a): aU,
    (SDL_KEYUP, SDLK_d): dU
}

class IDLE:
    @staticmethod
    def enter(self, event):
        self.frame %= self.frames['idle']
        print('ENTER IDLE')
        self.dir = 0
    @staticmethod
    def exit(self, event):
        print('EXIT IDLE')
    @staticmethod
    def do(self):
        pass
    @staticmethod
    def draw(self, x, y):
        frame_size = self.idle_left.w // self.frames['idle']
        if self.face_dir == 1:
            self.idle_right.clip_draw(frame_size * self.frame, 0, frame_size, self.idle_right.h, self.x + 20 + x,
                                      self.y + 20 + y, 40, 40)
        else:
            self.idle_left.clip_draw(frame_size * self.frame, 0, frame_size, self.idle_left.h, self.x + 20 + x,
                                     self.y + 20 + y, 40, 40)
        self.frame += 1
        self.frame %= self.frames['idle']

class RUN:
    @staticmethod
    def enter(self, event):
        self.frame %= self.frames['run']
        print('ENTER RUN')
        if event == dD:
            self.dir += 1
        elif event == aD:
            self.dir -= 1
        elif event == dU:
            self.dir -= 1
        elif event == aU:
            self.dir += 1
    @staticmethod
    def exit(self, event):
        print('EXIT RUN')
    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % self.frames['run']
        self.x += self.status['speed'] * self.dir
        self.x = clamp(40, self.x, 1160)
    @staticmethod
    def draw(self, x, y):
        frame_size = self.run_right.w // self.frames['run']
        if self.face_dir == 1:
            self.run_right.clip_draw(frame_size * self.frame, 0, frame_size, self.run_right.h, self.x + 20 + x,
                                    self.y + 20 + y, 40, 40)
        elif self.face_dir == -1:
            self.run_left.clip_draw(frame_size * self.frame, 0, frame_size, self.run_left.h, self.x + 20 + x,
                                    self.y + 20 + y, 40, 40)

class JUMP:
    @staticmethod
    def enter(self, event):
        self.frame %= self.frames['run']
        print('ENTER JUMP')
        if event == dD:
            self.dir += 1
        elif event == aD:
            self.dir -= 1
        elif event == dU:
            self.dir -= 1
        elif event == aU:
            self.dir += 1
        elif event == SPACE and self.state['jump'] == 0:
            self.state['jump'] = 7
    @staticmethod
    def exit(self, event):
        self.state['jump'] = 0
        print('EXIT JUMP')
    @staticmethod
    def do(self):
        if self.state['jump'] > 0:
            if self.state['jump'] > 2:
                self.y += 12 + self.status['jump'] + self.state['jump']
            self.state['jump'] -= 1
        self.y = clamp(80, self.y, 680)
        self.x += self.status['speed'] * self.dir
        self.x = clamp(40, self.x, 1160)
        if self.state['jump'] == 0:
            if self.dir == 0:
                self.add_event(TIMER)
            else:
                self.cur_state.exit(self, None)
                self.cur_state = RUN
                self.cur_state.enter(self, None)

    @staticmethod
    def draw(self, x, y):
        if self.face_dir == 1:
            self.jump_right.clip_draw(0, 0, self.jump_right.w, self.jump_right.h, self.x + 20 + x, self.y + 20 + y,
                                      40, 40)
        else:
            self.jump_left.clip_draw(0, 0, self.jump_left.w, self.jump_left.h, self.x + 20 + x, self.y + 20 + y, 40,
                                     40)

class DASH:
    runidle = False
    @staticmethod
    def enter(self, event):
        DASH.runidle = False
        print('ENTER DASH')
        if event == SHIFT and self.state['dash'] == 0:
            self.state['dash'] = 7
        if self.dir == 0:
            self.dir = self.face_dir
            DASH.runidle = True
    @staticmethod
    def exit(self, event):
        self.state['dash'] = 0
        print('EXIT DASH')
    @staticmethod
    def do(self):
        if self.state['dash'] > 0:
            if self.state['dash'] > 2:
                self.x += self.status['speed'] * 2.4 * self.dir
            self.state['dash'] -= 1
        self.x = clamp(40, self.x, 1160)
        if self.state['dash'] == 0:
            if DASH.runidle:
                self.add_event(TIMER)
            else:
                self.cur_state.exit(self, None)
                self.cur_state = RUN
                self.cur_state.enter(self, None)

    @staticmethod
    def draw(self, x, y):
        frame_size = self.run_right.w // self.frames['run']
        if self.face_dir == 1:
            self.run_right.clip_draw(0, 0, frame_size, self.run_right.h, self.x + 20 + x, self.y + 20 + y, 40, 40)
        else:
            self.run_left.clip_draw(0, 0, frame_size, self.run_left.h, self.x + 20 + x, self.y + 20 + y, 40, 40)

next_state = {
    IDLE: {aU: RUN, dU: RUN, aD: RUN, dD: RUN, TIMER: IDLE, SPACE: JUMP, SHIFT: DASH},
    RUN: {aU: IDLE, dU: IDLE, aD: IDLE, dD: IDLE, TIMER: RUN, SPACE: JUMP, SHIFT: DASH},
    JUMP: {aU: JUMP, dU: JUMP, aD: JUMP, dD: JUMP, SPACE: JUMP, TIMER: IDLE, SHIFT: DASH},
    DASH: {aU: DASH, dU: DASH, aD: DASH, dD: DASH, SPACE: JUMP, TIMER: IDLE, SHIFT: DASH},
}

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
        # 무기 이미지 dic로 바꿔서 문자열로 변경 예정
        self.weapon_image = load_image('./Resource/Weapon/Colt.png')
        self.equip_weapon = 'Colt'
        self.x = 400
        self.y = 300
        self.frame = 0
        self.frames = {'run': 8, 'idle': 5}
        self.status = {'speed': 10, 'jump': 30}
        # 오른쪽 : 1, 왼쪽 : -1
        self.dir = 0
        self.face_dir = 1
        self.state = {'run': False, 'jump': 0, 'dash': 0, 'die': False}
        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)
        self.mouse_x = 0

    def body_draw(self, x, y):
        # dash
        if self.state['dash']:
            frame_size = self.run_right.w // self.frames['run']
            if self.dir == 1:
                self.run_right.clip_draw(0, 0, frame_size, self.run_right.h, self.x + 20 + x, self.y + 20 + y, 40, 40)
            else:
                self.run_left.clip_draw(0, 0, frame_size, self.run_left.h, self.x + 20 + x, self.y + 20 + y, 40, 40)
            return
        # jump
        if self.state['jump'] > 0:
            if self.dir == 1:
                self.jump_right.clip_draw(0, 0, self.jump_right.w, self.jump_right.h, self.x + 20 + x, self.y + 20 + y,
                                          40, 40)
            else:
                self.jump_left.clip_draw(0, 0, self.jump_left.w, self.jump_left.h, self.x + 20 + x, self.y + 20 + y, 40,
                                         40)
            return
        # run
        if self.state['run']:
            frame_size = self.run_right.w // self.frames['run']
            if self.dir == 1:
                self.run_right.clip_draw(frame_size * self.frame, 0, frame_size, self.run_right.h, self.x + 20 + x,
                                         self.y + 20 + y, 40, 40)
            else:
                self.run_left.clip_draw(frame_size * self.frame, 0, frame_size, self.run_left.h, self.x + 20 + x,
                                        self.y + 20 + y, 40, 40)
            self.frame += 1
            self.frame %= self.frames['run']
            return
        # idle
        frame_size = self.idle_left.w // self.frames['idle']
        if self.dir == 1:
            self.idle_right.clip_draw(frame_size * self.frame, 0, frame_size, self.idle_right.h, self.x + 20 + x,
                                      self.y + 20 + y, 40, 40)
        else:
            self.idle_left.clip_draw(frame_size * self.frame, 0, frame_size, self.idle_left.h, self.x + 20 + x,
                                     self.y + 20 + y, 40, 40)
        self.frame += 1
        self.frame %= self.frames['idle']
        return

    def weapon_draw(self, x, y):
        width, height = self.weapon_image_L.w * 1.3, self.weapon_image_L.h * 1.3
        if self.dir == 1:
            self.weapon_image_R.clip_draw(0, 0, self.weapon_image_R.w, self.weapon_image_R.h, self.x + width // 2 + x + 20,
                                        self.y + height // 2 + y + 5, width, height)
        else:
            self.weapon_image_L.clip_draw(0, 0, self.weapon_image_L.w, self.weapon_image_L.h, self.x + width // 2 + x,
                                        self.y + height // 2 + y + 5, width, height)
    def draw(self, x, y):
        self.cur_state.draw(self, x, y)
        # self.body_draw(x, y)
        # self.weapon_draw(x, y)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        if event.type == SDL_MOUSEMOTION:
            self.mouse_x = event.x

    def update(self, x):
        self.cur_state.do(self)
        if self.mouse_x > self.x + x:
            self.face_dir = 1
        else:
            self.face_dir = -1
        # 중력
        self.y -= 12
        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state[self.cur_state][event]
            self.cur_state.enter(self, event)
        delay(0.04)
        # sum = [0, 0]
        # delay(0.05)
        # # 중력
        # sum[1] -= 12
        # # 좌우 이동
        # if self.state['run']:
        #     sum[0] += self.status['speed'] * self.dir
        # # 점프
        # if self.state['jump'] > 0:
        #     if self.state['jump'] > 2:
        #         sum[1] += 12 + self.status['jump'] + self.state['jump']
        #     self.state['jump'] -= 1
        # # 대쉬
        # if self.state['dash'] > 0:
        #     if self.state['dash'] > 2:
        #         sum[0] += self.status['speed'] * 2.4 * self.dir
        #     self.state['dash'] -= 1
        # self.x += sum[0]
        # self.y += sum[1]
        # return sum

