import game_utils
from source import *
import wrapper

__name__ = "SinglePlayer"


class SinglePlayer(GameScene):

    def __init__(self, player1_score=0, player2_score=0):
        super().__init__()
        self.player1 = Player((0, 0), 1)
        self.player1.pos = [50, int(pygame.display.get_window_size()[1] / 2 - self.player1.size[1] / 2)]
        self.objects.append(self.player1)
        self.player1_score = player1_score
        self.player2_score = player2_score

        self.player2 = Paddle((0, 0), 2)
        self.player2.pos = [pygame.display.get_window_size()[0] - 50 - self.player2.size[0],
                            int(pygame.display.get_window_size()[1] / 2 - self.player2.size[1] / 2)]
        self.objects.append(self.player2)
        self.player1_counter = Label(str(self.player1_score), (pygame.display.get_window_size()[0] / 2 - 50, 5), 60,
                                     color=wrapper.SECONDARY_COLOR, shadow_color=wrapper.MAIN_COLOR, centered=True)
        self.player2_counter = Label(str(self.player2_score), (pygame.display.get_window_size()[0] / 2 + 50, 5), 60,
                                     color=wrapper.SECONDARY_COLOR, shadow_color=wrapper.MAIN_COLOR, centered=True)
        self.objects.append(self.player1_counter)
        self.objects.append(self.player2_counter)

    def update(self):
        super().update()

        if self.ball.pos[0] <= 0:
            self.player2_score += 1
            wrapper.main.current_scene = SinglePlayer(self.player1_score, self.player2_score)
            next_scene = wrapper.main.current_scene
            next_scene.player1.direction = self.player1.direction
            next_scene.player2.direction = self.player2.direction
            wrapper.main.bounces = 0
            wrapper.main.goal_sound.play()
        elif self.ball.pos[0] + self.ball.size[0] >= pygame.display.get_window_size()[0]:
            self.player1_score += 1
            wrapper.main.current_scene = SinglePlayer(self.player1_score, self.player2_score)
            next_scene = wrapper.main.current_scene
            next_scene.player1.direction = self.player1.direction
            next_scene.player2.direction = self.player2.direction
            wrapper.main.bounces = 0
            wrapper.main.goal_sound.play()
        else:
            game_utils.handle_collisions(self.ball, self.player1, self.player2)
        offset = 10
        if not wrapper.main.cycles % 100:
            if self.player2.pos[1] + self.player2.size[1] + offset < self.ball.pos[1]:
                self.player2.direction = 1
            elif self.player2.pos[1] - offset > self.ball.pos[1] + self.ball.size[1]:
                self.player2.direction = -1
        self.player1_counter.text = self.player1_score
        self.player2_counter.text = self.player2_score
