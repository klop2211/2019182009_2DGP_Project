from pico2d import *

import play_state
import Bullet_object
import Camera
import game_world
import game_framework
import time

aD, dD, aU, dU, TIMER, SPACE, SHIFT, MOUSE_LD = range(8)
key_event_table = {
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_a): aD,
    (SDL_KEYDOWN, SDLK_d): dD,
    (SDL_KEYUP, SDLK_a): aU,
    (SDL_KEYUP, SDLK_d): dU
}

mouse_event_table = {
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): MOUSE_LD,
}

class IDLE:
    @staticmethod
    def enter(self, event):
        self.frame %= self.frames['idle']
        self.dir = 0
    @staticmethod
    def exit(self, event):
        if event == MOUSE_LD:
            self.attack()

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frames['idle']
    @staticmethod
    def draw(self, x, y):
        frame_size = self.idle_left.w // self.frames['idle']
        if self.face_dir == 1:
            self.idle_right.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle_right.h, self.x + 20 + x,
                                      self.y + 20 + y, 40, 40)
        else:
            self.idle_left.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle_left.h, self.x + 20 + x,
                                     self.y + 20 + y, 40, 40)

class RUN:
    @staticmethod
    def enter(self, event):
        self.frame %= self.frames['run']
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
        if event == MOUSE_LD:
            self.attack()
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frames['run']
        self.move()
    @staticmethod
    def draw(self, x, y):
        frame_size = self.run_right.w // self.frames['run']
        if self.face_dir == 1:
            self.run_right.clip_draw(frame_size * int(self.frame), 0, frame_size, self.run_right.h, self.x + 20 + x,
                                    self.y + 20 + y, 40, 40)
        elif self.face_dir == -1:
            self.run_left.clip_draw(frame_size * int(self.frame), 0, frame_size, self.run_left.h, self.x + 20 + x,
                                    self.y + 20 + y, 40, 40)

class JUMP:
    runtime = 0
    @staticmethod
    def enter(self, event):
        if event == dD:
            self.dir += 1
        elif event == aD:
            self.dir -= 1
        elif event == dU:
            self.dir -= 1
        elif event == aU:
            self.dir += 1
        if event == SPACE and time.time() - JUMP.runtime > 0.3 and self.fall:
            self.fall = False
            JUMP.runtime = time.time()


    @staticmethod
    def exit(self, event):
        if event == MOUSE_LD:
            self.attack()
    @staticmethod
    def do(self):
        self.y += PIXEL_PER_METER * game_framework.frame_time * (self.status['jump'] + 10)
        self.move()
        if time.time() - JUMP.runtime > 0.3:
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

    runtime = 0
    @staticmethod
    def enter(self, event):
        if event == dD:
            self.dir += 1
        elif event == aD:
            self.dir -= 1
        elif event == dU:
            self.dir -= 1
        elif event == aU:
            self.dir += 1
        if event == SHIFT and time.time() - DASH.runtime > 0.1:
            DASH.runtime = time.time()
    @staticmethod
    def exit(self, event):
        if event == MOUSE_LD:
            self.attack()
    @staticmethod
    def do(self):
        self.x += 10 * PIXEL_PER_METER * game_framework.frame_time * 5 * self.dir
        if time.time() - DASH.runtime > 0.1:
            if self.dir == 0:
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
    IDLE: {aU: RUN, dU: RUN, aD: RUN, dD: RUN, TIMER: IDLE, SPACE: JUMP, SHIFT: DASH, MOUSE_LD: IDLE},
    RUN: {aU: IDLE, dU: IDLE, aD: IDLE, dD: IDLE, TIMER: RUN, SPACE: JUMP, SHIFT: DASH, MOUSE_LD: RUN},
    JUMP: {aU: JUMP, dU: JUMP, aD: JUMP, dD: JUMP, SPACE: JUMP, TIMER: IDLE, SHIFT: DASH, MOUSE_LD: JUMP},
    DASH: {aU: DASH, dU: DASH, aD: DASH, dD: DASH, SPACE: JUMP, TIMER: IDLE, SHIFT: DASH, MOUSE_LD: DASH},
}

PIXEL_PER_METER = 40
RUN_SPEED_MPS = 5
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
import math

def distance(x, y):
    return math.sqrt(x * x + y * y)

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
        # 0 근접무기, 1 원거리무기
        self.weapon_type = 1
        self.x = 80
        self.y = 80
        self.frame = 0
        self.frames = {'run': 8, 'idle': 5}
        self.status = {'speed': 10, 'jump': 15}
        # 오른쪽 : 1, 왼쪽 : -1
        self.dir = 0
        self.face_dir = 1
        self.state = {'run': False, 'jump': 0, 'dash': 0, 'die': False}
        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)
        self.mouse_x = 0
        self.normal = [0, 0]
        self.fall = True
        self.hp = 100
        self.power = 50
        self.invincible = 0


    def move(self):
        self.x += self.dir * self.status['speed'] * PIXEL_PER_METER * game_framework.frame_time

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, other, group):
        match group:
            case 'hero:wall':
                self.x = clamp(40, self.x, 1160)
            case 'hero:block':
                self.y = clamp(other.top * 40, self.y, 660)
                if self.cur_state != JUMP:
                    self.fall = True
            case 'hero:door':
                if other.left < 20:
                    if play_state.map.state == 0 or play_state.map.state == 2:
                        if play_state.map.map_num > 0:
                            play_state.map.map_num -= 1
                            play_state.set_map()
                            self.x = 1120
                        else:
                            self.x = clamp(40, self.x, 1160)
                    else:
                        self.x = clamp(40, self.x, 1160)
                else:
                    if play_state.map.state == 2:
                        if play_state.map.map_num < 3:
                            play_state.map.map_num += 1
                            play_state.map.state = 0
                            play_state.set_map()
                            self.x = 80
                        else:
                            self.x = clamp(40, self.x, 1160)
                    else:
                        self.x = clamp(40, self.x, 1160)
            case 'hero:monster':
                if self.invincible <= 0:
                    self.invincible = 1.5
                    self.hp -= other.power
                    print(self.hp)




    def weapon_draw(self, x, y):
        width, height = self.weapon_image.w * 1.3, self.weapon_image.h * 1.3
        if self.face_dir == 1:
            self.weapon_image.clip_composite_draw(0, 0, self.weapon_image.w, self.weapon_image.h, 0, 'h', self.x + width // 2 + x + 20, self.y + height // 2 + y + 5, width,height)
        else:
            self.weapon_image.clip_draw(0, 0, self.weapon_image.w, self.weapon_image.h, self.x + width // 2 + x,
                                        self.y + height // 2 + y + 5, width, height)
        self.hand.clip_draw(0, 0, self.hand.w, self.hand.h, self.x + 20 + x, self.y + 10 + y, 7, 7)

    def draw(self, x, y):
        self.cur_state.draw(self, x, y)
        self.weapon_draw(x, y)
        # self.body_draw(x, y)

    def attack(self):
        if self.weapon_type == 1:
            bullet = Bullet_object.Bullet(self.x, self.y, self.normal[0], self.normal[1], self.power)
            game_world.add_object(bullet, 1)
            if play_state.map.map_num == 1:
                game_world.add_collision_pairs(bullet, play_state.banshees, 'bullet:monster')
            elif play_state.map.map_num == 0:
                game_world.add_collision_pairs(bullet, play_state.biggrayskels, 'bullet:monster')
            elif play_state.map.map_num == 2:
                game_world.add_collision_pairs(bullet, play_state.chaindemons, 'bullet:monster')
            elif play_state.map.map_num == 3:
                game_world.add_collision_pairs(bullet, play_state.niflheim, 'bullet:boss')
                game_world.add_collision_pairs(bullet, play_state.ice_pillars, 'bullet:monster')


    def set_normal(self, x, y):
        d = distance(x - self.x, y - self.y)
        self.normal[0] = (x - self.x) / d
        self.normal[1] = (y - self.y) / d

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        if (event.type, event.button) in mouse_event_table:
            mouse_event = mouse_event_table[(event.type, event.button)]
            self.set_normal(event.x - Camera.camera.x, 600 - event.y - Camera.camera.y)
            self.add_event(mouse_event)
        if event.type == SDL_MOUSEMOTION:
            self.mouse_x = event.x

    def update(self):
        self.cur_state.do(self)
        # 피격시 무적 시간
        self.invincible -= game_framework.frame_time
        if self.hp <= 0:
            # to do: 게임 엔딩(게임 오버)
            pass
        self.y = min(680, self.y)
        # 중력
        self.y -= 10 * PIXEL_PER_METER * game_framework.frame_time
        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state[self.cur_state][event]
            self.cur_state.enter(self, event)
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

