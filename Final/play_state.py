import time

import Banshee
import chaindemon
import game_framework
import Camera
import Map_object
import UI_object
import Hero_object
import game_world
import Map_bb
import Monster_object
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
walls = []
blocks = []
doors = []
check_col = None
biggrayskuls = []
banshees = []
chaindemons = []
spawn_timer = None


def set_map():
    global map, walls, doors, blocks, check_col, minimap, biggrayskuls, spawn_timer
    minimap.num = map.map_num
    for o in walls:
        game_world.remove_collision_object(o)
    for o in blocks:
        game_world.remove_collision_object(o)
    for o in doors:
        game_world.remove_collision_object(o)
    walls = [Map_bb.Wall(*l) for l in wall_data[map.map_num]]
    blocks = [Map_bb.Block(*l) for l in block_data[map.map_num]]
    doors = [Map_bb.Door(*l) for l in door_data[map.map_num]]
    game_world.add_collision_pairs(hero, walls, 'hero:wall')
    game_world.add_collision_pairs(hero, blocks, 'hero:block')
    game_world.add_collision_pairs(hero, doors, 'hero:door')
    spawn_timer = time.time()
    for o in biggrayskuls:
        game_world.remove_object(o)
    for o in banshees:
        game_world.remove_object(o)


def enter():
    global map, minimap, hero, back_ground, walls, doors, blocks, biggrayskuls, banshees
    check_col = True
    back_ground = load_image('./Resource\ice_tile\BGLayer_0 #218364.png')
    map = Map_object.Map()
    minimap = UI_object.Minimap(map.map_num)
    hero = Hero_object.Hero()
    biggrayskuls.append(Monster_object.Biggrayskul(16 * 40, 2 * 40, 10))
    biggrayskuls.append(Monster_object.Biggrayskul(7 * 40, 5 * 40, 10))
    biggrayskuls.append(Monster_object.Biggrayskul(24 * 40, 8 * 40, 10))
    biggrayskuls.append(Monster_object.Biggrayskul(17 * 40, 13 * 40, 10))
    biggrayskuls.append(Monster_object.Biggrayskul(10 * 40, 12 * 40, 10))
    banshees.append(Banshee.Banshee(6 * 40, 2 * 40, 10))
    banshees.append(Banshee.Banshee(4 * 40, 10 * 40, 10))
    banshees.append(Banshee.Banshee(10 * 40, 16 * 40, 10))
    banshees.append(Banshee.Banshee(14 * 40, 5 * 40, 10))
    banshees.append(Banshee.Banshee(14 * 40, 11 * 40, 10))
    banshees.append(Banshee.Banshee(19 * 40, 14 * 40, 10))
    banshees.append(Banshee.Banshee(20 * 40, 8 * 40, 10))
    chaindemons.append(chaindemon.Chaindemon(20 * 40, 4 * 40, 10))
    chaindemons.append(chaindemon.Chaindemon(25 * 40, 9 * 40, 10))
    chaindemons.append(chaindemon.Chaindemon(20 * 40, 16 * 40, 10))
    chaindemons.append(chaindemon.Chaindemon(14 * 40, 8 * 40, 10))
    chaindemons.append(chaindemon.Chaindemon(8 * 40, 15 * 40, 10))
    chaindemons.append(chaindemon.Chaindemon(4 * 40, 11 * 40, 10))
    set_map()
    # walls = [Map_bb.Wall(*l) for l in wall_data[map.map_num]]
    # blocks = [Map_bb.Block(*l) for l in block_data[map.map_num]]
    # doors = [Map_bb.Door(*l) for l in door_data[map.map_num]]
    game_world.add_objects(walls, 0)
    game_world.add_object(map, 0)
    game_world.add_object(hero, 1)
    game_world.add_object(minimap, 1)
    # game_world.add_collision_pairs(hero, walls, 'hero:wall')
    # game_world.add_collision_pairs(hero, blocks, 'hero:block')
    # game_world.add_collision_pairs(hero, doors, 'hero:door')


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def monster_spawn():
    if map.map_num == 0 and map.state < 3:
        game_world.add_objects(biggrayskuls, 1)
        game_world.add_collision_pairs(hero, biggrayskuls, 'hero:monster')
        game_world.add_collision_pairs(biggrayskuls, blocks, 'biggrayskel:block')
    if map.map_num == 1 and map.state < 3:
        game_world.add_objects(banshees, 1)
        game_world.add_collision_pairs(hero, banshees, 'hero:monster')
    if map.map_num == 2 and map.state < 3:
        game_world.add_objects(chaindemons, 1)
        game_world.add_collision_pairs(hero, chaindemons, 'hero:monster')

def update():
    # hero.update(camera.x)
    Camera.camera.update(hero)
    if time.time() - spawn_timer > 2 and map.state == 0:
        monster_spawn()
        map.state = 2
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