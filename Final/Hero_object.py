from pico2d import *

import Item_object
import Swing_object
import play_state
import Bullet_object
import Camera
import game_world
import game_framework
import time
import dead_state
aD, dD, aU, dU, TIMER, SPACE, SHIFT, MOUSE_LD, KEY_1, KEY_2, KEY_3, KEY_4 = range(12)
key_event_table = {
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_a): aD,
    (SDL_KEYDOWN, SDLK_d): dD,
    (SDL_KEYUP, SDLK_a): aU,
    (SDL_KEYUP, SDLK_d): dU,
    (SDL_KEYDOWN, SDLK_1): KEY_1,
    (SDL_KEYDOWN, SDLK_2): KEY_2,
    (SDL_KEYDOWN, SDLK_3): KEY_3,
    (SDL_KEYDOWN, SDLK_4): KEY_4,
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
        if event == MOUSE_LD and self.attack_time <= 0:
            self.attack()
        if event == KEY_1:
            self.change_weapon(0)
        elif event == KEY_2 and len(self.item) >= 2:
            self.change_weapon(1)
        elif event == KEY_3 and len(self.item) >= 3:
            self.change_weapon(2)
        elif event == KEY_4 and len(self.item) >= 4:
            self.change_weapon(3)
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
        if event == MOUSE_LD and self.attack_time <= 0:
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
        if event == MOUSE_LD and self.attack_time <= 0:
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
        if event == MOUSE_LD and self.attack_time <= 0:
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
    IDLE: {aU: RUN, dU: RUN, aD: RUN, dD: RUN, TIMER: IDLE, SPACE: JUMP, SHIFT: DASH, MOUSE_LD: IDLE, KEY_1: IDLE, KEY_2: IDLE, KEY_3: IDLE, KEY_4: IDLE},
    RUN: {aU: IDLE, dU: IDLE, aD: IDLE, dD: IDLE, TIMER: RUN, SPACE: JUMP, SHIFT: DASH, MOUSE_LD: RUN, KEY_1: RUN, KEY_2: RUN, KEY_3: RUN, KEY_4: RUN},
    JUMP: {aU: JUMP, dU: JUMP, aD: JUMP, dD: JUMP, SPACE: JUMP, TIMER: IDLE, SHIFT: DASH, MOUSE_LD: JUMP, KEY_1: JUMP, KEY_2: JUMP, KEY_3: JUMP, KEY_4: JUMP},
    DASH: {aU: DASH, dU: DASH, aD: DASH, dD: DASH, SPACE: JUMP, TIMER: IDLE, SHIFT: DASH, MOUSE_LD: DASH, KEY_1: DASH, KEY_2: DASH, KEY_3: DASH, KEY_4: DASH},
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
    be_attack = None
    attack_colt = None
    attack_shotgun = None
    image = None

    def __init__(self):
        if not Hero.be_attack:
            Hero.be_attack = load_wav('./Resource/Audio/be_attacked.wav')
            Hero.attack_colt = load_wav('./Resource/Audio/Gun.wav')
            Hero.attack_shotgun = load_wav('./Resource/Audio/ShotgunVintage.wav')
            Hero.be_attack.set_volume(30)
            Hero.attack_colt.set_volume(50)
            Hero.attack_shotgun.set_volume(50)
            Hero.image = {'idle_left': load_image('./Resource/Char/CharIdle_L.png'), 'idle_right': load_image('./Resource/Char/CharIdle_R.png'),
                     'run_left': load_image('./Resource/Char/CharRun_L.png'), 'run_right': load_image('./Resource/Char/CharRun_R.png'),
                     'jump_right': load_image('./Resource/Char/CharJump_R.png'), 'jump_left': load_image('./Resource/Char/CharJump_L.png'),
                     'die': load_image('./Resource/Char/CharDie.png'), 'hand': load_image('./Resource/Char/CharHand0.png')}
        self.idle_left = Hero.image['idle_left']
        self.idle_right = Hero.image['idle_right']
        self.run_left = Hero.image['run_left']
        self.run_right = Hero.image['run_right']
        self.jump_right = Hero.image['jump_right']
        self.jump_left = Hero.image['jump_left']
        self.die = Hero.image['die']
        self.hand = Hero.image['hand']
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
        self.power = 15
        self.invincible = 0
        self.item = [Item_object.Item('sword', 0, 0, 'equip', 10, 0, 0, 0.2)]
        self.equip_weapon = 0
        self.attack_time = self.item[0].attack_speed
        self.hand_x, self.hand_y = self.x + 20, self.y + 10
        game_world.add_object(self.item[0], 2)
        self.opacify = 1
        self.w, self.h = 40, 40
        self.hp_back = load_image('./Resource/UI/hp_back.png')
        self.hp_bar = load_image('./Resource/UI/hp_bar.png')
        self.invincible_mode = False

    def draw_hp(self, x, y):
        sx, sy = self.x + x, self.y + y
        self.hp_back.draw(sx + self.w // 2, sy + self.h // 2 - 40)
        self.hp_bar.draw(sx + self.w // 2 + 1 - int(self.hp_bar.w // 2 * (100 - self.hp) / 100),
                         sy + self.h // 2 - 1 - 40, int(self.hp_bar.w * self.hp / 100),
                         self.hp_bar.h)


    def move(self):
        self.x += self.dir * self.status['speed'] * PIXEL_PER_METER * game_framework.frame_time

    def get_bb(self):
        return self.x, self.y, self.x + 40, self.y + 40

    def handle_collision(self, other, group):
        match group:
            case 'hero:wall':
                self.x = clamp(40, self.x, 1120)
            case 'hero:block':
                if self.cur_state != JUMP:
                    self.y = clamp(other.top * 40, self.y, 660)
                    self.fall = True
            case 'hero:door':
                if other.left < 20:
                    if play_state.map.state == 0 or play_state.map.state == 2:
                        if play_state.map.map_num > 0:
                            play_state.map.map_num -= 1
                            play_state.set_map()
                            self.x = 1120
                        else:
                            self.x = clamp(40, self.x, 1120)
                    else:
                        self.x = clamp(40, self.x, 1120)
                else:
                    if play_state.map.state == 2:
                        if play_state.map.map_num < 3:
                            play_state.map.map_num += 1
                            play_state.map.state = 0
                            play_state.set_map()
                            self.x = 80
                        else:
                            self.x = clamp(40, self.x, 1120)
                    else:
                        self.x = clamp(40, self.x, 1120)
            case 'hero:monster':
                if self.invincible <= 0:
                    self.invincible = 1.5
                    Hero.be_attack.play(1)
                    self.hp -= other.power
            case 'hero:item':
                self.item.append(other)
                game_world.remove_collision_object(other)
                play_state.items.remove(other)
                self.change_weapon(len(self.item) - 1)

    def change_weapon(self, index):
        self.item[self.equip_weapon].state = 'inven'
        self.equip_weapon = index
        self.item[self.equip_weapon].state = 'equip'


    # def weapon_draw(self, x, y):
    #     width, height = self.weapon_image.w * 1.3, self.weapon_image.h * 1.3
    #     if self.face_dir == 1:
    #         self.weapon_image.clip_composite_draw(0, 0, self.weapon_image.w, self.weapon_image.h, 0, 'h', self.x + width // 2 + x + 20, self.y + height // 2 + y + 5, width,height)
    #     else:
    #         self.weapon_image.clip_draw(0, 0, self.weapon_image.w, self.weapon_image.h, self.x + width // 2 + x,
    #                                     self.y + height // 2 + y + 5, width, height)
    #     self.hand.clip_draw(0, 0, self.hand.w, self.hand.h, self.x + 20 + x, self.y + 10 + y, 7, 7)

    def draw(self, x, y):
        if self.hp > 0:

            self.cur_state.draw(self, x, y)
            self.hand.clip_draw(0, 0, self.hand.w, self.hand.h, self.hand_x + x, self.hand_y + y, 7, 7)
            self.draw_hp(x, y)

        else:
            sx, sy = self.x + x, self.y + y
            self.die.draw(sx + 20, sy + 20, 40, 40)



        # self.weapon_draw(x, y)
        # self.body_draw(x, y)

    def attack(self):
        if self.item[self.equip_weapon].name == 'colt':
            Hero.attack_colt.play(1)
            effect = [Bullet_object.Bullet(self.x, self.y, self.normal[0], self.normal[1], self.power + self.item[self.equip_weapon].power)]
        if self.item[self.equip_weapon].name == 'sword':
            if self.item[self.equip_weapon].swing:
                self.item[self.equip_weapon].swing = 0
            else:
                self.item[self.equip_weapon].swing = 1
            effect = [Swing_object.Sword_Swing(self.hand_x, self.hand_y, math.atan2(self.normal[1], self.normal[0]), self.power + self.item[self.equip_weapon].power)]
        if self.item[self.equip_weapon].name == 'saber':
            effect = [Swing_object.Saber_Swing(self.hand_x, self.hand_y, math.atan2(self.normal[1], self.normal[0]), self.power + self.item[self.equip_weapon].power)]
        if self.item[self.equip_weapon].name == 'shotgun':
            Hero.attack_shotgun.play(1)
            effect = [Bullet_object.Bullet(self.x, self.y, self.normal[0], self.normal[1],
                                            self.power + self.item[self.equip_weapon].power), Bullet_object.Bullet(self.x, self.y, math.cos(math.atan2(self.normal[1], self.normal[0]) + 3.14 * 15 / 180), math.sin(math.atan2(self.normal[1], self.normal[0]) + 3.14 * 15 / 180),
                                          self.power + self.item[self.equip_weapon].power), Bullet_object.Bullet(self.x, self.y, math.cos(math.atan2(self.normal[1], self.normal[0]) + 3.14 * -15 / 180), math.sin(math.atan2(self.normal[1], self.normal[0]) + 3.14 * -15 / 180),
                                          self.power + self.item[self.equip_weapon].power)]
        game_world.add_objects(effect, 1)
        if play_state.map.map_num == 1:
            game_world.add_collision_pairs(effect, play_state.banshees, 'effect:monster')
        elif play_state.map.map_num == 0:
            game_world.add_collision_pairs(effect, play_state.biggrayskels, 'effect:monster')
        elif play_state.map.map_num == 2:
            game_world.add_collision_pairs(effect, play_state.chaindemons, 'effect:monster')
        elif play_state.map.map_num == 3:
            game_world.add_collision_pairs(effect, play_state.niflheim, 'effect:boss')
            game_world.add_collision_pairs(effect, play_state.ice_pillars, 'effect:monster')
        self.attack_time = self.item[self.equip_weapon].attack_speed


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
        self.attack_time -= game_framework.frame_time
        self.hand_x, self.hand_y = self.x + 20, self.y + 10
        if self.invincible_mode:
            self.invincible = 0.5
        # 피격시 무적 시간
        self.invincible -= game_framework.frame_time
        if self.invincible > 0:
            if self.opacify == 1:
                self.opacify = 0
                for a in Hero.image:
                    Hero.image[a].opacify(0)
            else:
                self.opacify = 1
                for a in Hero.image:
                    Hero.image[a].opacify(1)
        else:
            if self.opacify == 0:
                self.opacify = 1
                for a in Hero.image:
                    Hero.image[a].opacify(1)
        if self.hp <= 0:
            self.opacify = 1
            for a in Hero.image:
                Hero.image[a].opacify(1)
            game_framework.push_state(dead_state)
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

