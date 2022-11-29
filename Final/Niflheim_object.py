from pico2d import *
import Monster_object
import game_world
import play_state
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import game_framework
import math

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


def normalize(x, y):
    dis = math.sqrt(x ** 2 + y ** 2)
    return x / dis, y / dis


def rotate(x, y, rad):
    return x * math.cos(rad) - y * math.sin(rad), x * math.sin(rad) + y * math.cos(rad)


class Ice_Spear:
    image = {}

    def __init__(self, x, y, dx, dy, power, delay):
        if not Ice_Spear.image:
            Ice_Spear.image['idle'] = load_image('./Resource/Niflheim/spear/IceSpearIdle.png')
            Ice_Spear.image['enter'] = load_image('./Resource/Niflheim/spear/IceSpearEnter.png')
        self.delay = delay
        self.w, self.h, = 50, 222
        self.x, self.y, self.power = x, y, power
        self.dx, self.dy = normalize(dx - x, dy - y)
        print(self.dx, self.dy)
        self.dir = math.atan2(self.dy, self.dx)

        self.state = 'enter'
        self.frames = {'enter': 12, 'idle': 1}
        self.frame = 0

    def update(self):
        self.delay -= game_framework.frame_time
        if self.delay <= 0:
            if self.state == 'enter':
                self.frame = (self.frame + self.frames[self.state] * ACTION_PER_TIME * game_framework.frame_time)
                if self.frame >= self.frames['enter']:
                    self.frame = 0
                    self.state = 'idle'
            else:
                self.x += self.dx
                self.y += self.dy
            if self.x < -100 or self.x > 1300 or self.y < -100 or self.y > 900:
                game_world.remove_object(self)


    def get_bb(self):
        center_x = self.x + self.w // 2
        center_y = self.y + self.h // 2
        points_x = []
        points_y = []
        lb = [self.x - center_x, self.y - center_y]
        points_x.append(rotate(lb[0], lb[1], self.dir)[0])
        points_y.append(rotate(lb[0], lb[1], self.dir)[1])
        lt = [self.x - center_x, self.y + self.h - center_y]
        points_x.append(rotate(lt[0], lt[1], self.dir)[0])
        points_y.append(rotate(lt[0], lt[1], self.dir)[1])
        rb = [self.x + self.w - center_x, self.y - center_y]
        points_x.append(rotate(rb[0], rb[1], self.dir)[0])
        points_y.append(rotate(rb[0], rb[1], self.dir)[1])
        rt = [self.x + self.w - center_x, self.y + self.h - center_y]
        points_x.append(rotate(rt[0], rt[1], self.dir)[0])
        points_y.append(rotate(rt[0], rt[1], self.dir)[1])
        return min(points_x) + center_x, min(points_y) + center_y,  max(points_x) + center_x, max(points_y) + center_y

    def handle_collision(self, other, group):
        pass

    def draw(self, c_x, c_y):
        sx, sy = self.x + c_x, self.y + c_y
        frame_size = Ice_Spear.image[self.state].w // self.frames[self.state]
        Ice_Spear.image[self.state].clip_composite_draw(frame_size * int(self.frame), 0, frame_size, Ice_Spear.image[self.state].h, self.dir - 1.57, '', sx + self.w // 2, sy + self.h // 2, self.w, self.h)


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
        self.defense = 0

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
            Ice_Pillar.image[self.state].clip_draw(frame_size * int(self.frame), 0, frame_size, Ice_Pillar.image[self.state].h, sx + self.w // 2, sy + self.h // 2, self.w, self.h)
        else:
            Ice_Pillar.image[self.state].clip_composite_draw(frame_size * int(self.frame), 0, frame_size, Ice_Pillar.image[self.state].h, 1.57, '', sx + self.w // 2, sy + self.h // 2, self.w, self.h)

    def handle_collision(self, other, group):
        pass

    def get_bb(self):
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
        self.build_behavior_tree()

    def update(self):
        for k, v in self.cooltime.items():
            self.cooltime[k] -= game_framework.frame_time
        self.frame = (self.frame + self.frames[self.state] * ACTION_PER_TIME * game_framework.frame_time)
        if self.state == 'idle':
            self.frame %= self.frames[self.state]
            self.bt.run()
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
            Niflheim.image[self.state].clip_draw(frame_size * int(self.frame), 0, frame_size, Niflheim.image[self.state].h, sx + self.w // 2, sy + self.h // 2, self.w, self.h)
        else:
            Niflheim.image[self.state].clip_composite_draw(frame_size * int(self.frame), 0, frame_size,
                                                 Niflheim.image[self.state].h, 0, 'h', sx + self.w // 2, sy + self.h // 2,
                                                 self.w, self.h)

    def get_bb(self):
        return self.x - self.w // 2, self.y - self.h // 2, self.x + self.w // 2, self.y + self.h // 2

    def handle_collision(self, other, group):
        pass

    def check_cooldown_pillar(self):
        if self.cooltime['pillar'] <= 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def move_center(self):
        self.x, self.y = 600, 440
        return BehaviorTree.SUCCESS

    def spawn_pillar(self):
        for o in play_state.ice_pillars:
            game_world.remove_object(o)
        play_state.ice_pillars.clear()
        self.cooltime['pillar'] = 10
        play_state.ice_pillars.append(Ice_Pillar(self.x - self.w - 20, self.y, 90, 100))
        play_state.ice_pillars.append(Ice_Pillar(self.x + self.w - 20, self.y, 90, 100))
        play_state.ice_pillars.append(Ice_Pillar(self.x - 20, self.y - self.h, 0, 100))
        play_state.ice_pillars.append(Ice_Pillar(self.x - 20, self.y + self.h, 0, 100))
        game_world.add_objects(play_state.ice_pillars, 1)
        return BehaviorTree.SUCCESS

    def check_cooldown_spear(self):
        if self.cooltime['spear'] <= 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def spawn_spear(self):
        spears = []
        hx, hy = play_state.hero.x, play_state.hero.y
        self.cooltime['spear'] = 7
        spears.append(Ice_Spear(7 * 40, 13 * 40, hx, hy, self.power, 0))
        spears.append(Ice_Spear(11 * 40, 13 * 40, hx, hy, self.power, 0.5))
        spears.append(Ice_Spear(15 * 40, 13 * 40, hx, hy, self.power, 1))
        spears.append(Ice_Spear(19 * 40, 13 * 40, hx, hy, self.power, 1.5))
        spears.append(Ice_Spear(23 * 40, 13 * 40, hx, hy, self.power, 2))
        game_world.add_objects(spears, 1)
        game_world.add_collision_pairs(play_state.hero, spears, 'hero:monster')
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        check_cooldown_pillar_node = LeafNode('Check_Cooldown_Pillar', self.check_cooldown_pillar)
        move_center_node = LeafNode('Move_Center', self.move_center)
        spawn_pillar_node = LeafNode('Spawn_Pillar', self.spawn_pillar)
        pillar_node = SequenceNode('Pillar')
        pillar_node.add_children(check_cooldown_pillar_node, move_center_node, spawn_pillar_node)

        check_cooldown_spear_node = LeafNode('Check_Cooldown_Pillar', self.check_cooldown_spear)
        spawn_spear_node = LeafNode('Spawn_Pillar', self.spawn_spear)
        spear_node = SequenceNode('Pillar')
        spear_node.add_children(check_cooldown_spear_node, move_center_node, spawn_spear_node)

        root_node = SelectorNode('Root')
        root_node.add_children(pillar_node, spear_node)
        self.bt = BehaviorTree(root_node)

    # to do: 인공지능 완성하기