
import game_framework
import game_world
import UI_object

from pico2d import *

back_ground = None
startbutton = None
exitbutton = None
main_logo = None
back_cloud = None
cloud_x = 0
bgm = None

def enter():
    global back_ground, startbutton, exitbutton, main_logo, back_cloud, bgm
    back_ground = load_image('./Resource/UI/BGLayer_0.png')
    main_logo = load_image('./Resource/UI/MainLogo.png')
    back_cloud = load_image('./Resource/UI/BackCloud.png')
    startbutton = UI_object.Startbutton()
    exitbutton = UI_object.Exitbutton()
    game_world.add_object(startbutton, 1)
    game_world.add_object(exitbutton, 1)
    bgm = load_music('./Resource/Audio/0.Town.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()


def update():
    global cloud_x
    cloud_x = (cloud_x + 10 * game_framework.frame_time) % 374


def draw():
    global back_ground
    clear_canvas()
    back_ground.clip_draw(0, 0, back_ground.w, back_ground.h, 400, 600 // 2, 800, 600)
    back_cloud.clip_draw(int(cloud_x), 0, 240, back_cloud.h, 400, 600 // 2, 800, 600)
    main_logo.clip_draw(0, 0, main_logo.w, main_logo.h, 400, 400, 312, 150)
    for object in game_world.all_object():
        object.draw()
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
            startbutton.handle_event(event)
            exitbutton.handle_event(event)





def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass



if __name__ == '__main__':
    open_canvas()
    game_framework.run(__name__)
    close_canvas()