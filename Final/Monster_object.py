
import play_state


class Monster:
    def set_dir(self):
        if self.x - play_state.hero.x > 15 or self.x - play_state.hero.x < -15:
            if self.x - play_state.hero.x > 0:
                self.dir = -1
            else:
                self.dir = 1

    def draw_hp(self, x, y):
        sx, sy = self.x + x, self.y + y
        self.hp_back.draw(sx + self.w // 2, sy + self.h // 2 - 40)
        self.hp_bar.draw(sx + self.w // 2 + 1 - int(self.hp_bar.w // 2 * (100 - self.hp) / 100),
                         sy + self.h // 2 - 1 - 40, int(self.hp_bar.w * self.hp / 100),
                         self.hp_bar.h)



