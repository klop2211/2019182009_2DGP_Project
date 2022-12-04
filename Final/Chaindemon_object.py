from pico2d import *
import Monster_object
import game_framework
import game_world
import play_state
import Die_object
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random
PIXEL_PER_METER = 40
RUN_SPEED_MPS = 5
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Chaindemon_Bullet:
    image = None

    def __init__(self, x = 800, y = 300):
        if Chaindemon_Bullet.image == None:
            Chaindemon_Bullet.image = load_image('./Resource/Chaindemon/ChainDemonFX.png')
        self.x, self.y = x, y
        self.frame = 0
        self.frames = 7
        self.power = 10

    def draw(self, x, y):
        frame_size = self.image.w // self.frames
        self.image.clip_composite_draw(frame_size * int(self.frame), 0, self.image.w // self.frames, self.image.h, 0, ' ', self.x + x + 21, self.y + y + 20, 42, 40)


    def get_bb(self):
        return self.x - 21, self.y - 20, self.x + 21, self.y + 20


    def update(self):
        self.frame = (self.frame + 6 * ACTION_PER_TIME * game_framework.frame_time)
        if self.frame >= self.frames:
            game_world.remove_object(self)


    def handle_collision(self, other, group):
        pass


class Chaindemon(Monster_object.Monster):
    idle = None
    attack = None
    sound_attack = None
    def __init__(self, x, y, power, hp, defense):
        self.x, self.y, self.power, self.hp, self.defense = x, y, power, hp, defense
        self.frames = {'idle': 6, 'attack': 2}
        self.face_dir = 1
        self.dir = 0
        self.frame = 0
        self.idletime = 0
        self.statetimer = 0
        self.attack_timer = 0
        self.cooltime = random.randint(3, 5)
        if Chaindemon.idle == None:
            Chaindemon.idle = load_image('./Resource/Chaindemon/ChainDemon.png')
            Chaindemon.attack = load_image('./Resource/Chaindemon/ChainDemonAttack.png')
            Chaindemon.sound_attack = load_wav('./Resource/Audio/chaindemon_attack.wav')
            Chaindemon.sound_attack.set_volume(100)
        self.idle = Chaindemon.idle
        self.attack = Chaindemon.attack
        self.state = 'idle'
        self.build_behavior_tree()
        self.hp_back = load_image('./Resource/UI/hp_back.png')
        self.hp_bar = load_image('./Resource/UI/hp_bar.png')
        self.w, self.h = 96, 78

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
            self.fire_bullet()
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def attack_hero(self):
        self.state = 'attack'
        self.statetimer -= game_framework.frame_time

        if self.statetimer <= 0:
            self.fire_bullet2()
            self.state = 'idle'
            self.attack_timer = self.cooltime
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING



    def find_hero_move(self):
        distance2 = (play_state.hero.x - self.x) ** 2 + (play_state.hero.y - self.y) ** 2
        if distance2 <= (PIXEL_PER_METER * 10) ** 2:
            self.dir = math.atan2(play_state.hero.y - self.y, play_state.hero.x - self.x)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_hero(self):
        self.state = 'idle'
        self.x += 10 * math.cos(self.dir) * game_framework.frame_time
        self.y += 10 * math.sin(self.dir) * game_framework.frame_time
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        find_hero_node = LeafNode('Find Hero', self.find_hero_attack)
        check_cooldown_node = LeafNode('Check Cooldown', self.check_cooldown)
        attack_hero_node = LeafNode('Attack Hero', self.attack_hero)
        attack_node = SequenceNode('Attack')
        attack_node.add_children(find_hero_node, check_cooldown_node, attack_hero_node)

        find_hero_move_node = LeafNode('Find Hero Move', self.find_hero_move)
        move_hero_node = LeafNode('Move Hero', self.move_hero)
        move_node = SequenceNode('Move')
        move_node.add_children(find_hero_move_node, move_hero_node)

        offence_node = SelectorNode('Offence')
        offence_node.add_children(attack_node, move_node)

        self.bt = BehaviorTree(offence_node)

    def get_bb(self):
        return self.x, self.y, self.x + 96, self.y + 78

    def fire_bullet(self):
        bullets = []
        Chaindemon.sound_attack.play(1)
        bullets.append(Chaindemon_Bullet(self.x - 48 - 40, self.y - 39 - 40))
        bullets.append(Chaindemon_Bullet(self.x, self.y - 39 - 40))
        bullets.append(Chaindemon_Bullet(self.x - 48 - 40, self.y))
        bullets.append(Chaindemon_Bullet(self.x + 48 + 40, self.y + 39 + 40))
        bullets.append(Chaindemon_Bullet(self.x, self.y + 39 + 40))
        bullets.append(Chaindemon_Bullet(self.x + 48 + 40, self.y))
        bullets.append(Chaindemon_Bullet(self.x - 48 - 40, self.y + 39 + 40))
        bullets.append(Chaindemon_Bullet(self.x + 48 + 40, self.y - 39 - 40))
        game_world.add_objects(bullets, 1)
        game_world.add_collision_pairs(play_state.hero, bullets, 'hero:monster')

    def fire_bullet2(self):
        bullets = []
        Chaindemon.sound_attack.play(1)
        bullets.append(Chaindemon_Bullet(self.x - 48 - 80, self.y - 39 - 80))
        bullets.append(Chaindemon_Bullet(self.x, self.y - 39 - 80))
        bullets.append(Chaindemon_Bullet(self.x - 48 - 80, self.y))
        bullets.append(Chaindemon_Bullet(self.x + 48 + 80, self.y + 39 + 80))
        bullets.append(Chaindemon_Bullet(self.x, self.y + 39 + 80))
        bullets.append(Chaindemon_Bullet(self.x + 48 + 80, self.y))
        bullets.append(Chaindemon_Bullet(self.x - 48 - 80, self.y + 39 + 80))
        bullets.append(Chaindemon_Bullet(self.x + 48 + 80, self.y - 39 - 80))
        game_world.add_objects(bullets, 1)
        game_world.add_collision_pairs(play_state.hero, bullets, 'hero:monster')

    def handle_collision(self, other, group):
        if group == 'hero:chaindemon':
            pass

    def update(self):
        self.frame = (self.frame + self.frames[self.state] * ACTION_PER_TIME * game_framework.frame_time) % self.frames[
            self.state]
        self.attack_timer -= game_framework.frame_time
        self.bt.run()
        if self.hp <= 0:
            game_world.add_object(Die_object.Die(self.x, self.y, 96, 78), 1)
            game_world.remove_object(self)
            play_state.chaindemons.remove(self)

    def draw(self, x, y):
        self.draw_hp(x, y)
        if self.state == 'attack':
            frame_size = self.attack.w // self.frames['attack']
            if self.dir == 1:
                self.attack.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 48 + x, self.y + 39 + y, 96, 78)
            else:
                self.attack.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h',
                                                self.x + 48 + x, self.y + 39 + y, 96, 78)
        elif self.state == 'idle' or self.state == 'move':
            frame_size = self.idle.w // self.frames['idle']
            if self.face_dir == 1:
                self.idle.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 48 + x, self.y + 39 + y, 96, 78)
            else:
                self.idle.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h',
                                              self.x + 48 + x, self.y + 39 + y, 96, 78)