from pico2d import *


class Map:
    def __init__(self):
        self.width = 1200
        self.height = 800
        # 상하좌우 기본 이미지 및 내부 이미지
        self.top = load_image('./Resource\ice_tile\Ice_H_Type2_1.png')
        self.left = load_image('./Resource\ice_tile\Ice_H_Type2_3.png')
        self.under = load_image('./Resource\ice_tile\Ice_H_Type2_4.png')
        self.right = load_image('./Resource\ice_tile\Ice_H_Type2_5.png')
        self.bottom = load_image('./Resource\ice_tile\Ice_H_Type2_7.png')
        # 각종 코너 이미지
        self.top_left = load_image('./Resource\ice_tile\Ice_H_Type2_0.png')
        self.bot_left = load_image('./Resource\ice_tile\Ice_H_Type2_6.png')
        self.bot_right = load_image('./Resource\ice_tile\Ice_H_Type2_8.png')
        self.top_left_corner = load_image('./Resource\ice_tile\Ice_H_Type2_9.png')
        self.top_right_corner = load_image('./Resource\ice_tile\Ice_H_Type2_10.png')
        self.bot_left_corner = load_image('./Resource\ice_tile\Ice_H_Type2_11.png')
        self.bot_right_corner = load_image('./Resource\ice_tile\Ice_H_Type2_12.png')
        self.back_ground = load_image('./Resource\ice_tile\BGLayer_0 #218364.png')
        # 발판 이미지
        self.block_left = load_image('./Resource\ice_tile\Ice_OnewayL.png')
        self.block_mid = load_image('./Resource\ice_tile\Ice_OnewayM.png')
        self.block_right = load_image('./Resource\ice_tile\Ice_OnewayR.png')
        # 0 : enter, 1 : lock, 2 : clear
        self.state = 0
        self.map_num = 3
        # 블럭의 위치를 x1, x2, y 순으로 가진 리스트, map_num를 통해 맵을 변경 1/40으로 축소 되있음
        self.block_info = [((5, 9, 4), (10, 14, 7), (7, 11, 11), (11, 15, 15), (16, 18, 12), (19, 21, 10), (21, 25, 7)),
                           ((3, 4, 9), (5, 9, 12), (7, 11, 8), (9, 12, 15), (12, 16, 4), (14, 17, 10), (16, 20, 7), (18, 21, 13), (23, 26, 10)),
                           ((4, 7, 4), (5, 8, 7), (3, 6, 10), (6, 9, 13), (11, 14, 15), (14, 16, 11), (19, 22, 15), (22, 26, 12), (20, 22, 9), (22, 24, 6), (20, 22, 3)),
                           ((4, 7, 6), (4, 7, 10), (4, 7, 14), (9, 13, 4), (9, 13, 8), (9, 13, 12), (15, 16, 6), (15, 16, 10), (15, 16, 14), (18, 22, 4), (18, 22, 8), (18, 22, 12), (24, 27, 6), (24, 27, 10), (24, 27, 14))]

    def draw(self, x, y):
        self.back_ground.clip_draw(0, 0, self.back_ground.w, self.back_ground.h,
                                   x + self.width // 2, y + self.height // 2, self.width, self.height)
        # 왼쪽, 오른쪽 벽
        for dy in range(0, self.height, 40):
            # 왼쪽
            if self.state == 0 or self.state == 2:
                if dy >= 280:
                    self.right.clip_draw(0, 0, self.right.w, self.right.h, x + 20, y + 20 + dy, 40, 40)
                if dy == 240:
                    self.bot_right.clip_draw(0, 0, self.bot_right.w, self.bot_right.h, x + 20, y + 20 + dy, 40, 40)
            elif self.state == 1:
                self.right.clip_draw(0, 0, self.right.w, self.right.h, x + 20, y + 20 + dy, 40, 40)
            # 오른쪽
            if self.state == 0 or self.state == 1:
                self.left.clip_draw(0, 0, self.left.w, self.left.h, x + 20 + self.width - 40, y + 20 + dy, 40, 40)
            elif self.state == 2:
                match self.map_num:
                    case 0:
                        if dy > 6 * 40:
                            self.left.clip_draw(0, 0, self.left.w, self.left.h, x + 20 + self.width - 40, y + 20 + dy,
                                                40, 40)
                        if dy == 6 * 40:
                            self.bot_left.clip_draw(0, 0, self.bot_left.w, self.bot_left.h, x + 20 + self.width - 40, y + 20 + dy,
                                                40, 40)
                    case 1:
                        if dy < 8 * 40:
                            self.left.clip_draw(0, 0, self.left.w, self.left.h, x + 20 + self.width - 40, y + 20 + dy,
                                                40, 40)
                        if dy == 8 * 40:
                            self.top_left.clip_draw(0, 0, self.top_left.w, self.top_left.h, x + 20 + self.width - 40, y + 20 + dy,
                                                40, 40)
                        if dy > 13 * 40:
                            self.left.clip_draw(0, 0, self.left.w, self.left.h, x + 20 + self.width - 40, y + 20 + dy,
                                                40, 40)
                        if dy == 13 * 40:
                            self.bot_left.clip_draw(0, 0, self.bot_left.w, self.bot_left.h, x + 20 + self.width - 40, y + 20 + dy,
                                                40, 40)
                    case 2:
                        if dy < 10 * 40:
                            self.left.clip_draw(0, 0, self.left.w, self.left.h, x + 20 + self.width - 40, y + 20 + dy,
                                                40, 40)
                        if dy == 10 * 40:
                            self.top_left.clip_draw(0, 0, self.top_left.w, self.top_left.h, x + 20 + self.width - 40,
                                                    y + 20 + dy, 40, 40)
                        if dy > 15 * 40:
                            self.left.clip_draw(0, 0, self.left.w, self.left.h, x + 20 + self.width - 40, y + 20 + dy,
                                                40, 40)
                        if dy == 15 * 40:
                            self.bot_left.clip_draw(0, 0, self.bot_left.w, self.bot_left.h, x + 20 + self.width - 40,
                                                    y + 20 + dy, 40, 40)
        # 위, 아래 벽
        for dx in range(0, self.width, 40):
            # 아래
            self.top.clip_draw(0, 0, self.top.w, self.top.h, x + 20 + dx, y + 60, 40, 40)
            self.under.clip_draw(0, 0, self.under.w, self.under.h, x + 20 + dx, y + 20, 40, 40)
            if dx == self.width - 40:
                self.bot_right_corner.clip_draw(0, 0, self.bot_right_corner.w, self.bot_right_corner.h, x + 20 + dx, y + 60, 40, 40)
            if self.state == 1:
                if dx == 0:
                    self.bot_left_corner.clip_draw(0, 0, self.bot_left_corner.w, self.bot_left_corner.h, x + 20 + dx,
                                               y + 60, 40, 40)
            if self.state == 2:
                match self.map_num:
                    case 0:
                        if dx == 29 * 40:
                            self.top.clip_draw(0, 0, self.top.w, self.top.h, x + 20 + dx, y + 60, 40, 40)
            # 위
            self.bottom.clip_draw(0, 0, self.bottom.w, self.bottom.h, x + 20 + dx, y + 20 + self.height - 80, 40, 40)
            self.under.clip_draw(0, 0, self.under.w, self.under.h, x + 20 + dx, y + 20 + self.height - 40, 40, 40)
            if dx == 0:
                self.top_left_corner.clip_draw(0, 0, self.top_left_corner.w, self.top_left_corner.h, x + 20 + dx, y + 20 + self.height - 80, 40, 40)
            if dx == self.width - 40:
                self.top_right_corner.clip_draw(0, 0, self.top_right_corner.w, self.top_right_corner.h, x + 20 + dx, y + 20 + self.height - 80, 40, 40)
        # 맵 별로 블럭 그리기
        for num in self.block_info[self.map_num]:
            for i in range(num[0], num[1] + 1):
                if i == num[0]:
                    self.block_left.clip_draw(0, 0, self.block_left.w, self.block_left.h, x + i * 40 + 20,
                                             y + num[2] * 40 + 20, 40, 40)
                elif i == num[1]:
                    self.block_right.clip_draw(0, 0, self.block_right.w, self.block_right.h, x + i * 40 + 20,
                                              y + num[2] * 40 + 20, 40, 40)
                else:
                    self.block_mid.clip_draw(0, 0, self.block_mid.w, self.block_mid.h, x + i * 40 + 20, y + num[2] * 40 + 20, 40, 40)





