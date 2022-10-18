from pico2d import *

class Minimap:
    def __init__(self):
        self.image = load_image('./Resource\\UI\\minimap_sheet.png')
        self.x = 650
        self.y = 500
        self.width = 120
        self.height = 80
        self.num = None

    def draw(self, map_num):
        self.image.clip_draw(30 * map_num, 0, self.image.w // 4, self.image.h,
                             self.x + self.width // 2, self.y + self.height // 2, self.width, self.height)

