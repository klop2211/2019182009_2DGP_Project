import game_framework
# import Camera
import Map_object
import UI_object
import Hero_object
import game_world
from pico2d import *

camera = None
map = None
minimap = None
hero = None
back_ground = None
wall_data = [[(0, 0, 30, 2), ()]]

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        self.x -= dx
        if self.x <= -400:
            self.x = -400
        elif self.x >= 0:
            self.x = 0
        self.y -= dy
        if self.y <= -200:
            self.y = -200
        elif self.y >= 0:
            self.y = 0

    def update(self, hero):
        dx, dy = hero.x + self.x + 20, hero.y + self.y + 20
        self.move(-(400 - dx), -(300 - dy))

    def draw(self):
        pass

def enter():
    global map, camera, minimap, hero, back_ground
    back_ground = load_image('./Resource\ice_tile\BGLayer_0 #218364.png')
    map = Map_object.Map()
    game_world.add_object(map, 0)
    camera = Camera()
    minimap = UI_object.Minimap(map.map_num)
    game_world.add_object(minimap, 1)
    hero = Hero_object.Hero()
    game_world.add_object(hero, 1)

# 두점을 선분이 양분 하는지
def is_divide_pt(x11,y11, x12,y12, x21,y21, x22,y22):
    f1 = (x12-x11)*(y21-y11) - (y12-y11)*(x21-x11)
    f2 = (x12-x11)*(y22-y11) - (y12-y11)*(x22-x11)
    if f1*f2 < 0:
        return True
    else:
        return False
# 두선분이 교차하는지
def is_cross_pt(x11, y11, x12,y12, x21,y21, x22,y22):
    b1 = is_divide_pt(x11, y11, x12, y12, x21, y21, x22, y22)
    b2 = is_divide_pt(x21, y21, x22, y22, x11, y11, x12, y12)
    if b1 and b2:
        return True
    return False

#  주인공이 발판이나 바닥위에있는지
def collision_hero_map(hero, map):
    # 발판의 top 선분 정보
    bottoms = [(i[0] * 40, (i[1] + 1) * 40, i[2] * 40 + 40) for i in map.block_info[map.map_num]]
    # 바닥
    bottoms.append((0, 1200, 80))
    for i in bottoms:
        if is_cross_pt(hero.x, hero.y + 15, hero.x + 40, hero.y - 10, i[0], i[2], i[1], i[2]):
            hero.y = i[2]
            return True
        if is_cross_pt(hero.x + 40, hero.y + 15, hero.x, hero.y - 10, i[0], i[2], i[1], i[2]):
            hero.y = i[2]
            return True
    return False

def update():
    # hero.update(camera.x)
    camera.update(hero)
    if hero.mouse_x > hero.x + camera.x:
        hero.face_dir = 1
    else:
        hero.face_dir = -1
    for object in game_world.all_object():
        object.update()
    collision_hero_map(hero, map)

def draw():
    global map, camera, minimap
    clear_canvas()
    back_ground.clip_draw(0, 0, back_ground.w, back_ground.h, camera.x + 1200 // 2, camera.y + 800 // 2, 1200, 800)
    for object in game_world.all_object():
        object.draw(camera.x, camera.y)
    # map.draw(camera.x, camera.y)
    # minimap.draw(map.map_num)
    # hero.draw(camera.x, camera.y)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            hero.handle_event(event)
    # events = get_events()
    # for event in events:
    #     if event.type == SDL_QUIT:
    #         game_framework.quit()
    #     elif event.type == SDL_KEYDOWN:
    #         match event.key:
    #             # 맵 이동을 위한 임시 문장
    #             case pico2d.SDLK_1:
    #                 map.map_num = 0
    #             case pico2d.SDLK_2:
    #                 map.map_num = 1
    #             case pico2d.SDLK_3:
    #                 map.map_num = 2
    #             case pico2d.SDLK_4:
    #                 map.map_num = 3
    #             # 주인공 좌우이동
    #             case pico2d.SDLK_a:
    #                 hero.dir = -1
    #                 hero.state['run'] = True
    #             case pico2d.SDLK_d:
    #                 hero.dir = 1
    #                 hero.state['run'] = True
    #             # 점프
    #             case pico2d.SDLK_SPACE:
    #                 if collision_hero_map():
    #                     hero.state['jump'] = 7
    #             case pico2d.SDLK_LSHIFT:
    #                 if hero.state['dash'] == 0:
    #                     hero.state['dash'] = 7
    #     elif event.type == SDL_KEYUP:
    #         hero.frame = 0
    #         match event.key:
    #             case pico2d.SDLK_a:
    #                 if hero.dir == -1:
    #                     hero.state['run'] = False
    #             case pico2d.SDLK_d:
    #                 if hero.dir == 1:
    #                     hero.state['run'] = False





def exit():
    pass

def pause():
    pass

def resume():
    pass



if __name__ == '__main__':
    open_canvas()
    game_framework.run(__name__)
    close_canvas()