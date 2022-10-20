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
        # 무기 이미지 dic로 바꿔서 문자열로 변경 예정
        self.weapon_image_L = load_image('./Resource/Weapon/Colt_L.png')
        self.weapon_image_R = load_image('./Resource/Weapon/Colt_R.png')
        self.equip_weapon = 'Colt'
        self.x = 400
        self.y = 300
        self.frame = 0
        self.frames = {'run': 8, 'idle': 5}
        self.status = {'speed': 10, 'jump': 30}
        # 오른쪽 : 1, 왼쪽 : -1
        self.dir = 1
        self.state = {'run': False, 'jump': 0, 'dash': 0, 'die': False}

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
        self.body_draw(x, y)
        self.weapon_draw(x, y)


    def update(self):
        sum = [0, 0]
        delay(0.05)
        # 중력
        sum[1] -= 12
        # 좌우 이동
        if self.state['run']:
            sum[0] += self.status['speed'] * self.dir
        # 점프
        if self.state['jump'] > 0:
            if self.state['jump'] > 2:
                sum[1] += 12 + self.status['jump'] + self.state['jump']
            self.state['jump'] -= 1
        # 대쉬
        if self.state['dash'] > 0:
            if self.state['dash'] > 2:
                sum[0] += self.status['speed'] * 2.4 * self.dir
            self.state['dash'] -= 1
        self.x += sum[0]
        self.y += sum[1]
        return sum

