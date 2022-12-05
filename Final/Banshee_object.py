import random
import time

from pico2d import *
import Monster_object
import game_framework
import game_world
import play_state
import Die_object
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


PIXEL_PER_METER = 40
RUN_SPEED_MPS = 5
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Banshee_Bullet:
    image = None

    def __init__(self, x = 800, y = 300, dx = 0, dy = 0):
        if Banshee_Bullet.image == None:
            Banshee_Bullet.image = load_image('./Resource/Banshee/BansheeBullet.png')
        self.x, self.y, self.dx, self.dy = x, y, dx, dy
        self.frame = 0
        self.frames = 4
        self.speed = 5
        self.power = 10

    def draw(self, x, y):
        frame_size = self.image.w // self.frames
        self.image.clip_composite_draw(frame_size * int(self.frame), 0, self.image.w // 4, self.image.h, 0, ' ', self.x + x + 15, self.y + y + 15, 30, 30)


    def get_bb(self):
        return self.x, self.y, self.x + 30, self.y + 30


    def update(self):
        self.x += self.dx * self.speed * PIXEL_PER_METER * game_framework.frame_time
        self.y += self.dy * self.speed * PIXEL_PER_METER * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frames
        if self.x < 20 or self.x > 1180:
            game_world.remove_object(self)
        if self.y < 60 or self.y > 720:
            game_world.remove_object(self)

    def handle_collision(self, other, group):
        pass


class Banshee(Monster_object.Monster):
    idle = None
    attack = None
    sound_attack = None

    def __init__(self, x, y, power, hp, defense = 2):
        self.x, self.y, self.power, self.hp, self.defense = x, y, power, hp, defense
        self.frames = {'idle': 6, 'attack': 6}
        self.face_dir = 1
        self.dir = 0
        self.frame = 0
        self.idletime = 0
        self.statetimer = 0
        self.attack_timer = 0
        self.cooltime = random.randint(3, 5)
        if Banshee.idle == None:
            Banshee.idle = load_image('./Resource/Banshee/BansheeIdle.png')
            Banshee.attack = load_image('./Resource/Banshee/BansheeAttack.png')
            Banshee.sound_attack = load_wav('./Resource/Audio/BansheeAttack_pre.wav')
            Banshee.sound_attack.set_volume(100)
        self.idle = Banshee.idle
        self.attack = Banshee.attack
        self.state = 'idle'
        self.build_behavior_tree()
        self.hp_back = load_image('./Resource/UI/hp_back.png')
        self.hp_bar = load_image('./Resource/UI/hp_bar.png')
        self.w, self.h = 40, 44

    def find_hero_attack(self):
        distance2 = (play_state.hero.x - self.x) ** 2 + (play_state.hero.y - self.y) ** 2
        if distance2 <= (PIXEL_PER_METER * 5) ** 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def check_cooldown(self):
        if self.attack_timer <= 0:
            self.frame = 0
            self.statetimer = self.frames['attack'] / (FRAMES_PER_ACTION * ACTION_PER_TIME)
            self.set_dir()
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def attack_hero(self):
        self.state = 'attack'
        self.statetimer -= game_framework.frame_time
        if self.frame > 3.0 and self.attack_timer <= 0:
            self.attack_timer = self.cooltime
            self.fire_bullet()
        if self.statetimer <= 0:
            print('attack end')
            self.state = 'idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        find_hero_node = LeafNode('Find Hero', self.find_hero_attack)
        check_cooldown_node = LeafNode('Check Cooldown', self.check_cooldown)
        attack_hero_node = LeafNode('Attack Hero', self.attack_hero)
        attack_node = SequenceNode('Attack')
        attack_node.add_children(check_cooldown_node, attack_hero_node)

        self.bt = BehaviorTree(attack_node)

    def get_bb(self):
        return self.x, self.y, self.x + 40, self.y + 44

    def fire_bullet(self):
        bullets =[]
        Banshee.sound_attack.play(1)
        bullets.append(Banshee_Bullet(self.x, self.y, -math.sqrt(0.5), -math.sqrt(0.5)))
        bullets.append(Banshee_Bullet(self.x, self.y, -1, 1))
        bullets.append(Banshee_Bullet(self.x, self.y, -1, 0))
        bullets.append(Banshee_Bullet(self.x, self.y, 1, -1))
        bullets.append(Banshee_Bullet(self.x, self.y, 1, 0))
        bullets.append(Banshee_Bullet(self.x, self.y, math.sqrt(0.5), math.sqrt(0.5)))
        bullets.append(Banshee_Bullet(self.x, self.y, 0, 1))
        bullets.append(Banshee_Bullet(self.x, self.y, 0, -1))
        game_world.add_objects(bullets, 1)
        game_world.add_collision_pairs(play_state.hero, bullets, 'hero:monster')


    def handle_collision(self, other, group):
        if group == 'hero:banshee':
            pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frames[
            self.state]
        self.attack_timer -= game_framework.frame_time
        self.bt.run()
        if self.hp <= 0:
            game_world.add_object(Die_object.Die(self.x, self.y, 40, 44), 1)
            game_world.remove_object(self)
            play_state.banshees.remove(self)

    def draw(self, x, y):
        self.draw_hp(x, y)
        if self.state == 'attack':
            frame_size = self.attack.w // self.frames['attack']
            if self.dir == 1:
                self.attack.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 20 + x,
                                      self.y + 22 + y, 40, 44)
            else:
                self.attack.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h',
                                                self.x + 20 + x,
                                                self.y + 22 + y, 40, 44)
        elif self.state == 'idle':
            frame_size = self.idle.w // self.frames['idle']
            if self.face_dir == 1:
                self.idle.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 20 + x,
                                    self.y + 22 + y, 40, 44)
            else:
                self.idle.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h',
                                              self.x + 20 + x,
                                              self.y + 22 + y, 40, 44)
        # self.cur_state.draw(self, x, y)
        # draw_rectangle(self.x + x, self.y + y, self.x + 67 + x, self.y + 96 + y)