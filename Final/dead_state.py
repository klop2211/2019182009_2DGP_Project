import time

import Camera
import game_framework
import game_world

from pico2d import *

import play_state
import logo_state

end_image = None
bgm = None
end_time = None


def enter():
    global end_image, bgm, end_time
    end_image = load_image('./Resource/UI/ExplorationFailure.korean.png')
    bgm = load_music('./Resource/Audio/dead.mp3')
    bgm.set_volume(32)
    bgm.play(1)
    end_time = 13


def update():
    global end_time
    end_time -= game_framework.frame_time

    if end_time <= 0:
        game_framework.change_state(logo_state)


def draw():
    global end_image
    clear_canvas()
    play_state.draw_world()
    play_state.hero.draw(Camera.camera.x, Camera.camera.y)
    end_image.draw(400, 300, 800, 90)
    update_canvas()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()





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