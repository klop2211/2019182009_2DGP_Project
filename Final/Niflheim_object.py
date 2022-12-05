import random

from pico2d import *
import Monster_object
import game_world
import play_state
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import game_framework
import math
import clear_state

PIXEL_PER_METER = 40
RUN_SPEED_MPS = 5
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


def normalize(x, y):
    dis = math.sqrt(x ** 2 + y ** 2)
    return x / dis, y / dis


def rotate(x, y, rad):
    return x * math.cos(rad) - y * math.sin(rad), x * math.sin(rad) + y * math.cos(rad)


class Ice_Crystal:
    image = {}
    enter_sound = None

    def __init__(self, x, y, power, delay):
        if not Ice_Crystal.image:
            Ice_Crystal.image['idle'] = load_image('./Resource/Niflheim/crystal/IceCrystalIdle.png')
            Ice_Crystal.image['enter'] = load_image('./Resource/Niflheim/crystal/IceCrystalEnter.png')
            Ice_Crystal.image['destroy'] = load_image('./Resource/Niflheim/crystal/IceCrystalDestroy.png')
            Ice_Crystal.enter_sound = load_wav('./Resource/Audio/ice_crystal_attack.wav')
            Ice_Crystal.enter_sound.set_volume(32)
        self.delay = delay
        self.w, self.h, = 93, 108
        self.x, self.y, self.power = x, y, power
        self.dy = -1
        self.state = 'enter'
        self.frames = {'enter': 16, 'idle': 1, 'destroy': 5}
        self.frame = 0

    def update(self):
        if self.delay <= 0:
            if self.state == 'enter':
                self.frame = (self.frame + self.frames[self.state] * ACTION_PER_TIME * game_framework.frame_time)
                if self.frame >= self.frames['enter']:
                    Ice_Crystal.enter_sound.play(1)
                    self.frame = 0
                    self.state = 'idle'
            elif self.state == 'idle':
                self.y += self.dy * 20 * PIXEL_PER_METER * game_framework.frame_time
            else:
                self.frame = (self.frame + self.frames[self.state] * 3 * game_framework.frame_time)
                if self.frame >= self.frames['destroy']:
                    game_world.remove_object(self)
            if self.y < 80:
                self.state = 'destroy'
        else:
            self.delay -= game_framework.frame_time

    def get_bb(self):
        return self.x, self.y, self.x + self.w, self.y + self.h

    def handle_collision(self, other, group):
        if self.state == 'idle':
            self.state = 'destroy'

    def draw(self, c_x, c_y):
        sx, sy = self.x + c_x, self.y + c_y
        frame_size = Ice_Crystal.image[self.state].w // self.frames[self.state]
        Ice_Crystal.image[self.state].clip_draw(frame_size * int(self.frame), 0, frame_size,
                                                        Ice_Crystal.image[self.state].h,
                                                        sx + self.w // 2, sy + self.h // 2, self.w, self.h)


class Ice_Spear:
    image = {}
    enter_sound = None

    def __init__(self, x, y, power, delay):
        if not Ice_Spear.image:
            Ice_Spear.image['idle'] = load_image('./Resource/Niflheim/spear/IceSpearIdle.png')
            Ice_Spear.image['enter'] = load_image('./Resource/Niflheim/spear/IceSpearEnter.png')
            Ice_Spear.enter_sound = load_wav('./Resource/Audio/ice_spear_attack.wav')
            Ice_Spear.enter_sound.set_volume(128)
        self.delay = delay
        self.w, self.h, = 50, 222
        self.x, self.y, self.power = x, y, power
        self.dx, self.dy = normalize(play_state.hero.x - x, play_state.hero.y - y)
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
                    Ice_Spear.enter_sound.play(1)
                    self.dx, self.dy = normalize(play_state.hero.x - self.x, play_state.hero.y - self.y)
                    self.dir = math.atan2(self.dy, self.dx)
                    self.frame = 0
                    self.state = 'idle'
            else:
                self.x += self.dx * 20 * PIXEL_PER_METER * game_framework.frame_time
                self.y += self.dy * 20 * PIXEL_PER_METER * game_framework.frame_time
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
    enter_sound = None

    def __init__(self, dx, dy, dir, hp):
        if not Ice_Pillar.image:
            Ice_Pillar.image['idle'] = load_image('./Resource/Niflheim/pillar/IcePillarIdle.png')
            Ice_Pillar.image['destroy'] = load_image('./Resource/Niflheim/pillar/IcePillarDestroyFX.png')
            Ice_Pillar.image['enter'] = load_image('./Resource/Niflheim/pillar/IcePillarEnter.png')
            Ice_Pillar.enter_sound = load_wav('./Resource/Audio/ice_pillar_spawn.wav')
            Ice_Pillar.enter_sound.set_volume(25)

        self.w, self.h, = 112, 44
        self.x, self.y, self.dir, self.hp = play_state.niflheim.x + dx, play_state.niflheim.y + dy, dir, hp
        print(hp)
        self.dx, self.dy = dx, dy
        self.state = 'enter'
        self.frames = {'enter': 20, 'destroy': 3, 'idle': 1}
        self.frame = 0
        self.defense = 0
        self.hp_back = load_image('./Resource/UI/hp_back.png')
        self.hp_bar = load_image('./Resource/UI/hp_bar.png')
        Ice_Pillar.enter_sound.play(1)

    def update(self):
        self.x, self.y = play_state.niflheim.x + self.dx, play_state.niflheim.y + self.dy
        if self.state == 'enter':
            self.frame = (self.frame + self.frames[self.state] * ACTION_PER_TIME * game_framework.frame_time)
            if self.frame >= self.frames['enter']:
                self.frame = 0
                self.state = 'idle'
        if self.state == 'destroy':
            self.frame = (self.frame + self.frames[self.state] * 3 * game_framework.frame_time)
            if self.frame >= self.frames['destroy']:
                game_world.remove_object(self)
                play_state.ice_pillars.remove(self)
        if self.hp <= 0 and self.state != 'destroy':
            self.state = 'destroy'

    def draw(self, c_x, c_y):
        sx, sy = self.x + c_x, self.y + c_y
        frame_size = Ice_Pillar.image[self.state].w // self.frames[self.state]

        if self.dir == 0:
            self.hp_back.draw(sx + self.w // 2, sy + self.h // 2 - 40)
            self.hp_bar.draw(sx + self.w // 2 + 1 - int(self.hp_bar.w // 2 * (100 - self.hp) / 100), sy + self.h // 2 - 1 - 40, int(self.hp_bar.w * self.hp / 100),
                             self.hp_bar.h)
            Ice_Pillar.image[self.state].clip_draw(frame_size * int(self.frame), 0, frame_size, Ice_Pillar.image[self.state].h, sx + self.w // 2, sy + self.h // 2, self.w, self.h)
        else:
            self.hp_back.draw(sx + self.w // 2, sy + self.h // 2 - 80)
            self.hp_bar.draw(sx + self.w // 2 + 1 - int(self.hp_bar.w // 2 * (100 - self.hp) / 100), sy + self.h // 2 - 1 - 80, int(self.hp_bar.w * self.hp / 100),
                             self.hp_bar.h)
            Ice_Pillar.image[self.state].clip_composite_draw(frame_size * int(self.frame), 0, frame_size, Ice_Pillar.image[self.state].h, 1.57, '', sx + self.w // 2, sy + self.h // 2, self.w, self.h)

    def handle_collision(self, other, group):
        pass

    def get_bb(self):
        # 가로 모양
        if self.dir == 0:
            return self.x, self.y, self.x + 112, self.y + 44
        else:
            return self.x, self.y, self.x + 44, self.y + 112


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
        self.dx, self.dy = 0, 0
        self.state = 'enter'
        self.invincible = 1
        self.cooltime = {'pillar': 0, 'spear': 3, 'crystal': 5}
        self.delay = 0
        self.build_behavior_tree()
        self.hp_back = load_image('./Resource/UI/hp_back.png')
        self.hp_bar = load_image('./Resource/UI/hp_bar.png')

    def update(self):
        self.x += self.dx * 20 * PIXEL_PER_METER * game_framework.frame_time
        self.y += self.dy * 20 * PIXEL_PER_METER * game_framework.frame_time
        self.delay -= game_framework.frame_time
        self.invincible -= game_framework.frame_time
        self.frame = (self.frame + self.frames[self.state] * ACTION_PER_TIME * game_framework.frame_time)
        if self.state == 'idle':
            self.frame %= self.frames[self.state]
            if self.delay <= 0:
                for k in self.cooltime:
                    self.cooltime[k] -= game_framework.frame_time
                self.bt.run()
        if self.state == 'enter' and self.frame >= self.frames['enter']:
            self.frame = 0
            self.state = 'idle'
        if self.state == 'die' and self.frame >= self.frames['die']:
            game_framework.push_state(clear_state)
        if self.hp <= 0 and self.state != 'die':
            self.state = 'die'

    def draw(self, x, y):
        sx, sy = self.x + x, self.y + y
        frame_size = Niflheim.image[self.state].w // self.frames[self.state]
        self.draw_hp(x, y)
        if self.dir == 1:
            Niflheim.image[self.state].clip_draw(frame_size * int(self.frame), 0, frame_size, Niflheim.image[self.state].h, sx + self.w // 2, sy + self.h // 2, self.w, self.h)
        else:
            Niflheim.image[self.state].clip_composite_draw(frame_size * int(self.frame), 0, frame_size,
                                                 Niflheim.image[self.state].h, 0, 'h', sx + self.w // 2, sy + self.h // 2,
                                                 self.w, self.h)

    def get_bb(self):
        if play_state.ice_pillars:
            return 0, 0, 0, 0
        return self.x - self.w // 2, self.y - self.h // 2, self.x + self.w // 2, self.y + self.h // 2

    def handle_collision(self, other, group):
        pass

    def check_cooldown_pillar(self):
        if self.cooltime['pillar'] <= 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def move_center(self):
        if clamp(590, self.x, 610) == self.x and clamp(430, self.y, 450) == self.y:
            self.dx, self.dy = 0, 0
            return BehaviorTree.SUCCESS
        self.dx, self.dy = normalize(600 - self.x, 440 - self.y)
        return BehaviorTree.RUNNING

    def spawn_pillar(self):
        for o in play_state.ice_pillars:
            game_world.remove_object(o)
        play_state.ice_pillars.clear()
        self.cooltime['pillar'] = 10
        play_state.ice_pillars.append(Ice_Pillar(- self.w - 20 - 40, 0, 90, 100))
        play_state.ice_pillars.append(Ice_Pillar(self.w - 20 + 40, 0, 90, 100))
        play_state.ice_pillars.append(Ice_Pillar(- 20, - self.h - 40, 0, 100))
        play_state.ice_pillars.append(Ice_Pillar(- 20, + self.h + 40, 0, 100))
        game_world.add_objects(play_state.ice_pillars, 1)
        self.delay = 2
        return BehaviorTree.SUCCESS

    def check_cooldown_spear(self):
        if self.cooltime['spear'] <= 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def spawn_spear(self):
        spears = []
        self.cooltime['spear'] = 7
        match random.randint(0, 2):
            case 0:
                spears.append(Ice_Spear(7 * 40, 13 * 40, self.power, 0))
                spears.append(Ice_Spear(11 * 40, 13 * 40, self.power, 0.5))
                spears.append(Ice_Spear(15 * 40, 13 * 40, self.power, 1))
                spears.append(Ice_Spear(19 * 40, 13 * 40, self.power, 1.5))
                spears.append(Ice_Spear(23 * 40, 13 * 40, self.power, 2))
            case 1:
                spears.append(Ice_Spear(7 * 40, 13 * 40, self.power, 0))
                spears.append(Ice_Spear(11 * 40, 13 * 40, self.power, 0.2))
                spears.append(Ice_Spear(15 * 40, 13 * 40, self.power, 0.4))
                spears.append(Ice_Spear(19 * 40, 13 * 40, self.power, 0.6))
                spears.append(Ice_Spear(23 * 40, 13 * 40, self.power, 0.8))
            case 2:
                spears.append(Ice_Spear(7 * 40, 13 * 40, self.power, 0))
                spears.append(Ice_Spear(11 * 40, 13 * 40, self.power, 0))
                spears.append(Ice_Spear(15 * 40, 13 * 40, self.power, 0))
                spears.append(Ice_Spear(19 * 40, 13 * 40, self.power, 0))
                spears.append(Ice_Spear(23 * 40, 13 * 40, self.power, 0))

        game_world.add_objects(spears, 1)
        game_world.add_collision_pairs(play_state.hero, spears, 'hero:monster')
        self.delay = 2
        return BehaviorTree.SUCCESS

    def check_cooldown_crystal(self):
        if self.cooltime['crystal'] <= 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def move_left(self):
        self.dx, self.dy = normalize(4 * 40 - self.x, 15 * 40 - self.y)
        self.dir = -1
        if clamp(4 * 40 - 10, self.x, 4 * 40 + 10) == self.x and clamp(15 * 40 - 10, self.y, 15 * 40 + 10) == self.y:
            self.dx, self.dy = 0, 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def spawn_crystal(self):
        crystals = []
        self.cooltime['crystal'] = 7
        match random.randint(0, 2):
            case 0:
                for i in range(1, 26, 3):
                    if i % 2:
                        crystals.append(Ice_Crystal(i * 40, 16 * 40, self.power, 0))
                    else:
                        crystals.append(Ice_Crystal(i * 40, 16 * 40, self.power, 1))
            case 1:
                for i in range(1, 26, 3):
                    crystals.append(Ice_Crystal(i * 40, 16 * 40, self.power, i // 3 / 3))
            case 2:
                for i in range(1, 26, 3):
                    if i > 15:
                        crystals.append(Ice_Crystal(i * 40, 16 * 40, self.power, 1))
                    else:
                        crystals.append(Ice_Crystal(i * 40, 16 * 40, self.power, 0))



        game_world.add_objects(crystals, 1)
        game_world.add_collision_pairs(play_state.hero, crystals, 'hero:monster')
        self.delay = 2
        return BehaviorTree.SUCCESS

    def move_right(self):
        self.dx, self.dy = normalize(26 * 40 - self.x, 15 * 40 - self.y)
        self.dir = 1
        if clamp(26 * 40 - 10, self.x, 26 * 40 + 10) == self.x and clamp(15 * 40 - 10, self.y, 15 * 40 + 10) == self.y:
            self.dx, self.dy = 0, 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def move_random(self):
        if self.dx != 0:
            if self.dir == 1:
                return self.move_right()
            else:
                return self.move_left()
        if random.randint(0, 1):
            return self.move_right()
        else:
            return self.move_left()

    def build_behavior_tree(self):
        check_cooldown_pillar_node = LeafNode('Check_Cooldown_Pillar', self.check_cooldown_pillar)
        move_center_node = LeafNode('Move_Center', self.move_center)
        spawn_pillar_node = LeafNode('Spawn_Pillar', self.spawn_pillar)
        pillar_node = SequenceNode('Pillar')
        pillar_node.add_children(check_cooldown_pillar_node, move_center_node, spawn_pillar_node)

        check_cooldown_spear_node = LeafNode('Check_Cooldown_Spear', self.check_cooldown_spear)
        spawn_spear_node = LeafNode('Spawn_Spear', self.spawn_spear)
        move_random_node = LeafNode('Move_Random', self.move_random)
        spear_node = SequenceNode('Spear')
        spear_node.add_children(check_cooldown_spear_node, move_random_node, spawn_spear_node)

        check_cooldown_crystal_node = LeafNode('Check_Cooldown_Crystal', self.check_cooldown_crystal)
        spawn_crystal_node = LeafNode('Spawn_Crystal', self.spawn_crystal)
        crystal_node = SequenceNode('Crystal')
        crystal_node.add_children(check_cooldown_crystal_node, move_random_node, spawn_crystal_node)

        root_node = SelectorNode('Root')
        root_node.add_children(pillar_node, spear_node, crystal_node)
        self.bt = BehaviorTree(root_node)

    # to do: 인공지능 완성하기