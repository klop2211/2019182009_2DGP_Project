import game_framework
import Camera
import Map_object
import UI_object
import Hero_object
import game_world
import Map_bb
from pico2d import *

map = None
minimap = None
hero = None
back_ground = None
wall_data = [[(0, 6, 1, 18), (29, 6, 30, 18)],
             [(0, 6, 1, 18), (29, 13, 30, 18), (29, 2, 30, 9)],
             [(0, 6, 1, 18), (29, 2, 30, 11), (29, 15, 30, 18)],
             [(0, 6, 1, 18), (29, 2, 30, 18)]]
block_data = [[(0, 0, 29, 2), (5, 5, 9, 5), (10, 8, 14, 8), (7, 12, 11, 12), (11, 16, 15, 16), (16, 13, 18, 13), (19, 11, 21, 11), (21, 8, 25, 8)],
              [(0, 0, 29, 2), (3, 10, 4, 10), (5, 13, 9, 13), (7, 9, 11, 9), (9, 16, 12, 16), (12, 5, 16, 5), (14, 11, 17, 11), (16, 8, 20, 8), (18, 14, 21, 14), (23, 11, 26, 11)],
              [(0, 0, 29, 2), (4, 5, 7, 5), (5, 8, 8, 8), (3, 11, 6, 11), (6, 14, 9, 14), (11, 16, 14, 16), (14, 12, 16, 12), (19, 16, 22, 16), (22, 13, 26, 13), (20, 10, 22, 10), (22, 7, 24, 7), (20, 4, 22, 4)],
              [(0, 0, 29, 2), (4, 7, 7, 7), (4, 11, 7, 11), (4, 15, 7, 15), (9, 5, 13, 5), (9, 9, 13, 9), (9, 13, 13, 13), (15, 7, 16, 7), (15, 11, 16, 11), (15, 15, 16, 15), (18, 5, 22, 5), (18, 9, 22, 9), (18, 13, 22, 13), (24, 7, 27, 7), (24, 11, 27, 11), (24, 15, 27, 15)]]
door_data = [[(0, 2, 1, 6), (29, 2, 30, 6)], [(0, 2, 1, 6), (29, 9, 30, 13)], [(0, 2, 1, 6), (29, 11, 30, 15)], [(0, 2, 1, 6)]]
walls = None
blocks = None
doors = None

def enter():
    global map, minimap, hero, back_ground, walls, doors, blocks
    back_ground = load_image('./Resource\ice_tile\BGLayer_0 #218364.png')
    map = Map_object.Map()
    minimap = UI_object.Minimap(map.map_num)
    hero = Hero_object.Hero()
    walls = [Map_bb.Wall(*l) for l in wall_data[map.map_num]]
    blocks = [Map_bb.Block(*l) for l in block_data[map.map_num]]
    doors = [Map_bb.Door(*l) for l in door_data[map.map_num]]
    game_world.add_objects(walls, 0)
    game_world.add_object(map, 0)
    game_world.add_object(minimap, 1)
    game_world.add_object(hero, 1)
    game_world.add_collision_pairs(hero, walls, 'hero:wall')
    game_world.add_collision_pairs(hero, blocks, 'hero:block')
    game_world.add_collision_pairs(hero, doors, 'hero:door')

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

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def update():
    # hero.update(camera.x)
    Camera.camera.update(hero)
    if hero.mouse_x > hero.x + Camera.camera.x:
        hero.face_dir = 1
    else:
        hero.face_dir = -1
    for object in game_world.all_object():
        object.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            a.handle_collision(b, group)
            b.handle_collision(a, group)

def draw():
    global map, camera, minimap
    clear_canvas()
    back_ground.clip_draw(0, 0, back_ground.w, back_ground.h, Camera.camera.x + 1200 // 2, Camera.camera.y + 800 // 2, 1200, 800)
    for object in game_world.all_object():
        object.draw(Camera.camera.x, Camera.camera.y)
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