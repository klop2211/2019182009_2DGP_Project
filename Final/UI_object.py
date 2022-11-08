from pico2d import *

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