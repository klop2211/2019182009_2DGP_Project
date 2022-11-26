from pico2d import *

import game_framework
import play_state

class Minimap:
    def __init__(self, num = 0):
        self.image = load_image('./Resource\\UI\\minimap_sheet.png')
        self.x = 650
        self.y = 500
        self.width = 120
        self.height = 80
        self.num = num

    def draw(self,x,y):
        self.image.clip_draw(30 * self.num, 0, self.image.w // 4, self.image.h,
                             self.x + self.width // 2, self.y + self.height // 2, self.width, self.height)

    def update(self):
        pass


class Startbutton:
    def __init__(self):
        self.off = load_image('./Resource\\UI\\PlayOff_kor.png')
        self.on = load_image('./Resource\\UI\\PlayOn_kor.png')
        self.state = 'off'

    def draw(self):
        if self.state == 'off':
            self.off.clip_draw(0, 0, self.off.w, self.off.h, 400, 200 - 18, 108, 36)
        else:
            self.on.clip_draw(0, 0, self.off.w, self.off.h, 400, 200 - 18, 108, 36)

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            if event.x < 454 and event.x > 346 and 600 - event.y < 218 and 600 - event.y > 172:
                self.state = 'on'
            else:
                self.state = 'off'
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.x < 454 and event.x > 346 and 600 - event.y < 218 and 600 - event.y > 172:
                game_framework.change_state(play_state)


class Exitbutton:
    def __init__(self):
        self.off = load_image('./Resource\\UI\\ExitOff_kor.png')
        self.on = load_image('./Resource\\UI\\ExitOn_kor.png')
        self.state = 'off'

    def draw(self):
        if self.state == 'off':
            self.off.clip_draw(0, 0, self.off.w, self.off.h, 400, 150 - 18, 63, 36)
        else:
            self.on.clip_draw(0, 0, self.off.w, self.off.h, 400, 150 - 18, 63, 36)

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_MOUSEMOTION:
            if event.x < 431 and event.x > 369 and 600 - event.y < 158 and 600 - event.y > 122:
                self.state = 'on'
            else:
                self.state = 'off'
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.x < 431 and event.x > 369 and 600 - event.y < 158 and 600 - event.y > 122:
                game_framework.quit()
