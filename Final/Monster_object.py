from pico2d import *
import game_framework
import play_state
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


PIXEL_PER_METER = 40
RUN_SPEED_MPS = 5
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Monster:
    def set_dir(self):
        if self.x - play_state.hero.x > 15 or self.x - play_state.hero.x < -15:
            if self.x - play_state.hero.x > 0:
                self.dir = -1
            else:
                self.dir = 1
    pass



class Biggrayskul(Monster):
    idle = None
    attack = None
    move = None
    skill = None

    def __init__(self, x, y, power):
        self.x, self.y, self.power = x, y, power
        self.frames = {'idle': 8, 'attack': 13, 'move': 6, 'skill': 13}
        self.face_dir = 1
        self.dir = 0
        self.frame = 0
        if Biggrayskul.idle == None:
            Biggrayskul.idle = load_image('./Resource/BigGrayIceSkel/BigGrayIceSkelIdle.png')
            Biggrayskul.attack = load_image('./Resource/BigGrayIceSkel/BigGrayIceSkelAttack.png')
            Biggrayskul.move = load_image('./Resource/BigGrayIceSkel/BigGrayIceSkelMove.png')
            Biggrayskul.skill = load_image('./Resource/BigGrayIceSkel/BigGrayIceSkelSkill.png')
        self.idle = Biggrayskul.idle
        self.attack = Biggrayskul.attack
        self.move = Biggrayskul.move
        self.skill = Biggrayskul.skill
        self.state = 'idle'
        self.cooltime = {'attack': 13 / (FRAMES_PER_ACTION * ACTION_PER_TIME), 'skill': 13 / (FRAMES_PER_ACTION * ACTION_PER_TIME)}
        self.timer = self.cooltime['attack']
        self.build_behavior_tree()
        # self.cur_state = IDLE
        # self.cur_state.enter(self, None)

    def find_hero_move(self):
        distance2 = (play_state.hero.x - self.x) ** 2 + (play_state.hero.y - self.y) ** 2
        if distance2 <= (PIXEL_PER_METER * 6) ** 2:
            self.set_dir()
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_hero(self):
        self.state = 'move'
        self.x += self.dir * 5 * PIXEL_PER_METER * game_framework.frame_time
        return BehaviorTree.SUCCESS


    def find_hero_attack(self):
        distance2 = (play_state.hero.x - self.x) ** 2 + (play_state.hero.y - self.y) ** 2
        if distance2 <= (PIXEL_PER_METER * 2) ** 2:
            self.frame = 0
            self.set_dir()
            self.timer = self.cooltime['attack']
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def attack_hero(self):
        self.state = 'attack'
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            print('attack end')
            self.state = 'idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def find_hero_skill(self):
        distance2 = (play_state.hero.x - self.x) ** 2 + (play_state.hero.y - self.y) ** 2
        if distance2 <= (PIXEL_PER_METER * 8) ** 2:
            self.frame = 0
            self.set_dir()
            self.timer = self.cooltime['skill']
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def skill_hero(self):
        self.state = 'skill'
        self.timer -= game_framework.frame_time
        if int(self.frame) == 7:
            self.x, self.y = play_state.hero.x, play_state.hero.y
        if self.timer <= 0:
            print('attack end')
            self.state = 'idle'
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def build_behavior_tree(self):
        find_hero_attack_node = LeafNode('Find Hero Attack', self.find_hero_attack)
        attack_hero_node = LeafNode('Attack Hero', self.attack_hero)
        attack_node = SequenceNode('Attack')
        attack_node.add_children(find_hero_attack_node, attack_hero_node)

        find_hero_move_node = LeafNode('Find Hero Move', self.find_hero_move)
        move_hero_node = LeafNode('Move Hero', self.move_hero)
        move_node = SequenceNode('Move')
        move_node.add_children(find_hero_move_node, move_hero_node)

        find_hero_skill_node = LeafNode('Find Hero Skill', self.find_hero_skill)
        skill_hero_node = LeafNode('Skill Hero', self.skill_hero)
        skill_node = SequenceNode('Skill')
        skill_node.add_children(find_hero_skill_node, skill_hero_node)

        offence_node = SelectorNode('Offence')
        offence_node.add_children(attack_node, move_node, skill_node)
        self.bt = BehaviorTree(offence_node)
        # fill here
        pass

    def get_bb(self):
        if self.state == 'attack':
            return self.x - (2 * PIXEL_PER_METER), self.y - 48, self.x + (2 * PIXEL_PER_METER), self.y + (2 * PIXEL_PER_METER)
        return self.x - 67, self.y - 48, self.x + 67, self.y + 48


    # def set_dir(self):
    #     if self.x - play_state.hero.x > 15 or self.x - play_state.hero.x < -15:
    #         if self.x - play_state.hero.x > 0:
    #             self.dir = -1
    #         else:
    #             self.dir = 1


    def handle_collision(self, other, group):
        pass
        # if group == 'hero:biggrayskel':
        #     if self.cur_state == IDLE:
        #         locate = other.x, other.y
        #         self.cur_state.exit(self, None)
        #         self.cur_state = SKILL
        #         self.cur_state.enter(self, locate)
        #     if self.cur_state == MOVE:
        #         self.cur_state.exit(self, None)
        #         self.cur_state = ATTACK
        #         self.cur_state.enter(self, None)
        if group == 'biggrayskel:block':
            self.y = clamp(other.top * 40, self.y, 660)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.frames[self.state]
        self.bt.run()
        # self.cur_state.do(self)
        self.y -= 10 * PIXEL_PER_METER * game_framework.frame_time

    def draw(self, x, y):
        if self.state == 'idle':
            frame_size = self.idle.w // self.frames['idle']
            if self.face_dir == 1:
                self.idle.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 67 + x,
                                    self.y + 48 + y, 134, 96)
            else:
                self.idle.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h',
                                              self.x + 67 + x,
                                              self.y + 48 + y, 134, 96)
        elif self.state == 'attack':
            frame_size = self.attack.w // self.frames['attack']
            if self.dir == 1:
                self.attack.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 67 + x,
                                      self.y + 48 + y, 134, 96)
            else:
                self.attack.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h',
                                                self.x + x,
                                                self.y + 48 + y, 134, 96)
        elif self.state == 'move':
            frame_size = self.move.w // self.frames['move']
            if self.dir == 1:
                self.move.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 67 + x,
                                    self.y + 48 + y, 134, 96)
            else:
                self.move.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h',
                                              self.x + x,
                                              self.y + 48 + y, 134, 96)
        elif self.state == 'skill':
            frame_size = self.skill.w // self.frames['skill']
            if self.face_dir == 1:
                self.skill.clip_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, self.x + 67 + x,
                                     self.y + 48 + y, 134, 96)
            else:
                self.skill.clip_composite_draw(frame_size * int(self.frame), 0, frame_size, self.idle.h, 0, 'h',
                                               self.x + 67 + x,
                                               self.y + 48 + y, 134, 96)
        # self.cur_state.draw(self, x, y)


