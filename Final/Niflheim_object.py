from pico2d import *
import Monster_object
import game_world
import play_state
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import game_framework

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Ice_Pillar:
    image = {}
    # w: 112, h: 44

    def __init__(self, x, y, dir, hp):
        if not Ice_Pillar.image:
            Ice_Pillar.image['idle'] = load_image('./Resource/Niflheim/pillar/IcePillarIdle.png')
            Ice_Pillar.image['destroy'] = load_image('./Resource/Niflheim/pillar/IcePillarDestroyFX.png')
            Ice_Pillar.image['enter'] = load_image('./Resource/Niflheim/pillar/IcePillarEnter.png')

        self.w, self.h, = 112, 44
        self.x, self.y, self.dir, self.hp = x, y, dir, hp
        self.state = 'enter'
        self.frames = {'enter': 20, 'destroy': 3, 'idle': 1}
        self.frame = 0

    def update(self):
        if self.state != 'idle':
            self.frame = (self.frame + self.frames[self.state] * ACTION_PER_TIME * game_framework.frame_time)
        if self.state == 'enter' and self.frame >= self.frames['enter']:
            self.frame = 0
            self.state = 'idle'
        if self.state == 'destroy' and self.frame >= self.frames['destroy']:
            game_world.remove_object(self)
            play_state.ice_pillars.remove(self)
        if self.hp <= 0 and self.state != 'destroy':
            self.state = 'destroy'

    def draw(self, c_x, c_y):
        sx, sy = self.x + c_x, self.y + c_y
        frame_size = Ice_Pillar.image[self.state].w // self.frames[self.state]
        if self.dir == 0:
            Ice_Pillar.image[self.state].clip_draw(frame_size * int(self.frame), 0, frame_size, Ice_Pillar.image[self.state].h, sx - self.w // 2, sy - self.h // 2, self.w, self.h)
        else:
            Ice_Pillar.image[self.state].clip_composite_draw(frame_size * int(self.frame), 0, frame_size, Ice_Pillar.image[self.state].h, 90, ' ', sx - self.w // 2, sy - self.h // 2, self.w, self.h)

    def handle_collision(self, other, group):
        pass

    def get__bb(self):
        # 가로 모양
        if self.dir == 0:
            return self.x - 56, self.y - 22, self.x + 56, self.y + 22
        else:
            return self.x - 22, self.y - 56, self.x + 22, self.y + 56


class Niflheim(Monster_object.Monster):
    image = dict()

    def __init__(self, x, y, power, hp, defense):
        self.w, self.h = 80, 64
        self.x, self.y, self.power, self.hp, self.defense = x, y, power, hp, defense
        if 'idle' not in Niflheim.image:
            print('니플헤임 생성')
            Niflheim.image['idle'] = load_image('./Resource/Niflheim/Sprite/NiflheimIdle.png')
            Niflheim.image['enter'] = load_image('./Resource/Niflheim/Sprite/NiflheimEnter.png')
            Niflheim.image['die'] = load_image('./Resource/Niflheim/Sprite/NiflheimDie.png')
            Niflheim.image['attack'] = load_image('./Resource/Niflheim/Sprite/NiflheimAttack.png')
        self.frames = {'idle': 6, 'attack': 11, 'die': 30, 'enter': 16}
        self.frame = 0
        self.dir = 1
        self.state = 'enter'
        self.invincible = 0
        self.cooltime = {'pillar': 0, 'spear': 5, 'crystal': 5}
        # self.build_behavior_tree()

    def update(self):
        for t in self.cooltime.values():
            t -= game_framework.frame_time
        self.frame = (self.frame + self.frames[self.state] * ACTION_PER_TIME * game_framework.frame_time)
        if self.state == 'idle':
            self.frame %= self.frames[self.state]
        if self.state == 'enter' and self.frame >= self.frames['enter']:
            self.frame = 0
            self.state = 'idle'
        if self.state == 'die' and self.frame >= self.frames['die']:
            pass
            # to do: 게임 엔딩(클리어)
        if self.hp <= 0 and self.state != 'die':
            self.state = 'die'

    def draw(self, x, y):
        sx, sy = self.x + x, self.y + y
        frame_size = Niflheim.image[self.state].w // self.frames[self.state]
        if self.dir == 1:
            Niflheim.image[self.state].clip_draw(frame_size * int(self.frame), 0, frame_size, Niflheim.image[self.state].h, sx - self.w // 2, sy - self.h // 2, self.w, self.h)
        else:
            Niflheim.image[self.state].clip_composite_draw(frame_size * int(self.frame), 0, frame_size,
                                                 Niflheim.image[self.state].h, 0, 'h', sx - self.w // 2, sy - self.h // 2,
                                                 self.w, self.h)

    def get_bb(self):
        return self.x - self.w // 2, self.y - self.h // 2, self.x + self.w // 2, self.y + self.h // 2

    def handle_collision(self, other, group):
        pass

    def check_cooldown_pillar(self):
        if self.cooltime['pillar'] <= 0:
            return BehaviorTree.SUCCESS

    def move_center(self):
        pass

    def spawn_pillar(self):
        for o in play_state.ice_pillars:
            game_world.remove_object(o)
        play_state.ice_pillars.clear()
        self.cooltime['pillar'] = 15
        play_state.ice_pillars.append(Ice_Pillar(self.x - self.w, self.y, 90, 100))

    # to do: 인공지능 완성하기