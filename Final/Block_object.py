from pico2d import *

map_data = [[(0, 0, 30, 2, 'bottom', 3), (0, 1, 1, 2, 'bot_left_in', 1), (29, 1, 30, 2, 'bot_right_in', 2),
             (0, 18, 30, 20, 'top', 3), (0, 18, 1, 19, 'top_left_in', 3), (29, 18, 30, 19, 'top_right_in', 3),
             (0, 6, 1, 7, 'top_left_out', 1), (0, 6, 1, 18, 'left', 3),  (0, 2, 1, 6, 'left', 1),
             (29, 6, 30, 7, 'top_right_out', 2), (29, 6, 30, 18, 'right', 3),  (29, 2, 30, 6, 'right', 2)]]

class Block:
    # 상하좌우 벽
    top = load_image('./Resource\ice_tile\Ice_H_Type2_1.png')
    left = load_image('./Resource\ice_tile\Ice_H_Type2_3.png')
    right = load_image('./Resource\ice_tile\Ice_H_Type2_5.png')
    bottom = load_image('./Resource\ice_tile\Ice_H_Type2_7.png')
    under = load_image('./Resource\ice_tile\Ice_H_Type2_4.png')
    # 각종 코너 이미지
    bot_right_out = load_image('./Resource\ice_tile\Ice_H_Type2_0.png')
    bot_left_out = load_image('./Resource\ice_tile\Ice_H_Type2_2.png')
    top_right_out = load_image('./Resource\ice_tile\Ice_H_Type2_6.png')
    top_left_out = load_image('./Resource\ice_tile\Ice_H_Type2_8.png')
    top_left_in = load_image('./Resource\ice_tile\Ice_H_Type2_9.png')
    top_right_in = load_image('./Resource\ice_tile\Ice_H_Type2_10.png')
    bot_left_in = load_image('./Resource\ice_tile\Ice_H_Type2_11.png')
    bot_right_in = load_image('./Resource\ice_tile\Ice_H_Type2_12.png')
    # 발판 이미지
    block_left = load_image('./Resource\ice_tile\Ice_OnewayL.png')
    block_mid = load_image('./Resource\ice_tile\Ice_OnewayM.png')
    block_right = load_image('./Resource\ice_tile\Ice_OnewayR.png')
    img_dict = {'top': top, 'left': left, 'right': right, 'bottom': bottom, 'under': under,
                'bot_right_out': bot_right_out, 'bot_left_out': bot_left_out, 'top_right_out': top_right_out, 'top_left_out': top_left_out,
                'bot_right_in': bot_right_in, 'bot_left_in': bot_left_in, 'top_right_in': top_right_in, 'top_left_in': top_left_in,
                'block_left': block_left, 'block_right': block_right, 'block_mid': block_mid }

    def __init__(self, l, b, r, t, img_name, state):
        self.left, self.right, self.top, self.bottom = l, r, t, b
        self.img = Block.img_dict[img_name]
        # 3 항상 그림, 2 진행상황이 enter, lock일때 그림, 1 진행상황이 lock일때 그림
        self.state = state

    def draw(self, camera_x, camera_y):
        if self.state > 0: # 0 대신 현재상황 1: enter, 0:lock, 2: exit가 들어가면됨
            for x in range(self.left, self.right, 40):
                for y in range(self.bottom, self.top, 40):
                    self.img.clip_draw(0, 0, self.img.w, self.img.h, x - 20 + camera_x, y - 20 + camera_y, 40, 40)

    def update(self):
        pass

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top

