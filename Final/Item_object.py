from pico2d import *
import play_state


class Item:
    image = None

    def __init__(self, name, x, y, state='drop', power=0, defense=0, speed=0, attack_speed=0):
        if not Item.image:
            Item.image = {'sword': load_image('./Resource/Weapon/Sword.png'),
                          'saber': load_image('./Resource/Weapon/SaberCase.png'),
                          'colt': load_image('./Resource/Weapon/Colt.png'),
                          'shotgun': load_image('./Resource/Weapon/Shotgun.png')}

        self.name, self.power, self.defense, self.speed, self.attack_speed, self.state = \
            name, power, defense, speed, attack_speed, state
        self.x, self.y = x, y
        self.w, self.h = Item.image[name].w * 1.5, Item.image[name].h * 1.5
        self.dir = 1
        self.swing = 0

    def draw(self, x, y):
        if self.state == 'inven':
            return
        sx, sy = self.x + x, self.y + y
        if self.name == 'sword':
            width = Item.image[self.name].w // 2
            if self.swing == 0:
                if self.dir == 1:
                    Item.image[self.name].clip_composite_draw(width * self.swing, 0, width, Item.image[self.name].h, 0,
                                                              ' ',
                                                              sx + self.w // 2 - self.w, sy + self.h // 2 - self.h, self.w,
                                                              self.h)
                else:
                    Item.image[self.name].clip_composite_draw(width * self.swing, 0, width, Item.image[self.name].h, 0,
                                                              'h',
                                                              sx + self.w // 2, sy + self.h // 2 - self.h, self.w,
                                                              self.h)
            else:
                if self.dir == 1:
                    Item.image[self.name].clip_composite_draw(width * self.swing, 0, width, Item.image[self.name].h, 0,
                                                              ' ',
                                                              sx + self.w // 2 - self.w, sy + self.h // 2, self.w,
                                                              self.h)
                else:
                    Item.image[self.name].clip_composite_draw(width * self.swing, 0, width, Item.image[self.name].h, 0,
                                                              'h',
                                                              sx + self.w // 2, sy + self.h // 2, self.w,
                                                              self.h)
        elif self.name == 'saber':
            dir = 3.14 * 90 / 180
            if self.dir == 1:
                Item.image[self.name].clip_composite_draw(0, 0, Item.image[self.name].w,
                                                          Item.image[self.name].h, dir, 'h', sx,
                                                          sy, self.w, self.h)
            else:
                Item.image[self.name].clip_composite_draw(0, 0, Item.image[self.name].w,
                                                          Item.image[self.name].h, -dir, ' ', sx,
                                                          sy, self.w, self.h)
        else:
            if self.dir == 1:
                Item.image[self.name].clip_composite_draw(0, 0, Item.image[self.name].w,
                                                          Item.image[self.name].h, 0, ' ', sx + self.w // 2,
                                                          sy + self.h // 2, self.w, self.h)
            else:
                Item.image[self.name].clip_composite_draw(0, 0, Item.image[self.name].w,
                                                          Item.image[self.name].h, 0, 'h', sx + self.w // 2 - self.w,
                                                          sy + self.h // 2, self.w, self.h)


    def update(self):
        if self.state == 'equip':
            self.x, self.y, self.dir = play_state.hero.hand_x, play_state.hero.hand_y, play_state.hero.face_dir
            # if self.dir == 1:
            #     self.x += 10
            # else:
            #     self.x -= 10

    def get_bb(self):
        if self.state == 'drop':
            return self.x, self.y, self.x + self.w, self.y + self.h
        return 0,0,0,0

    def handle_collision(self, other, group):
        pass

