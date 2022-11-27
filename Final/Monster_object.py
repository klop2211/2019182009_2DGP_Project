
import play_state




class Monster:
    def set_dir(self):
        if self.x - play_state.hero.x > 15 or self.x - play_state.hero.x < -15:
            if self.x - play_state.hero.x > 0:
                self.dir = -1
            else:
                self.dir = 1
    pass



