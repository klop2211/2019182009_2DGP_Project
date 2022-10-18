import game_framework
import Camera
import Map_object
import UI_object
import Hero_object
from pico2d import *

camera = None
map = None
minimap = None
hero = None

def enter():
    global map, camera, minimap, hero
    map = Map_object.Map()
    camera = Camera.Camera()
    minimap = UI_object.Minimap()
    hero = Hero_object.Hero()

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

def collision_hero_map():
    # 발판의 top 선분 정보
    bottoms = [(i[0] * 40, (i[1] + 1) * 40, i[2] * 40 + 40) for i in map.block_info[map.map_num]]
    # 바닥
    bottoms.append((0, 1200, 80))
    for i in bottoms:
        if is_cross_pt(hero.x, hero.y + 40, hero.x + 40, hero.y - 5, i[0], i[2], i[1], i[2]):
            hero.y = i[2]
            return
        if is_cross_pt(hero.x + 40, hero.y + 40, hero.x, hero.y - 5, i[0], i[2], i[1], i[2]):
            hero.y = i[2]
            return

def update():
    hero.update()
    collision_hero_map()
    pass

def draw():
    global map, camera, minimap
    clear_canvas()
    map.draw(camera.x, camera.y)
    minimap.draw(map.map_num)
    hero.draw(camera.x, camera.y)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                # 카메라 이동을 위한 임시 문장
                case pico2d.SDLK_UP:
                    camera.move(0, 50)
                case pico2d.SDLK_DOWN:
                    camera.move(0, -50)
                case pico2d.SDLK_LEFT:
                    camera.move(-50, 0)
                case pico2d.SDLK_RIGHT:
                    camera.move(50, 0)
                # 맵 이동을 위한 임시 문장
                case pico2d.SDLK_1:
                    map.map_num = 0
                case pico2d.SDLK_2:
                    map.map_num = 1
                case pico2d.SDLK_3:
                    map.map_num = 2
                case pico2d.SDLK_4:
                    map.map_num = 3
                # 주인공 좌우이동
                case pico2d.SDLK_a:
                    hero.dir = -1
                    hero.state['run'] = True
                case pico2d.SDLK_d:
                    hero.dir = 1
                    hero.state['run'] = True
        elif event.type == SDL_KEYUP:
            hero.frame = 0
            match event.key:
                case pico2d.SDLK_a:
                    if hero.dir == -1:
                        hero.state['run'] = False
                case pico2d.SDLK_d:
                    if hero.dir == 1:
                        hero.state['run'] = False





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