import pygame
import colorsys

import utils
import wrapper
import random


class Scene:

    def __init__(self):
        self.objects = []

    def render(self, window):
        for object in self.objects:
            object.render(window)

    def update(self):
        wrapper.SECONDARY_COLOR.color = tuple(
            round(i * 255) for i in colorsys.hsv_to_rgb(wrapper.main.cycles / 4000, 1, 1))
        for object in self.objects:
            object.update()

    def event(self, event):
        for object in self.objects:
            object.event(event)


class Object:

    def __init__(self, pos, size):
        self.surf = pygame.Surface(size)
        self.pos = list(pos)
        self.size = size

    def render(self, window):
        window.blit(self.surf, self.pos)
        self.surf.fill((0, 0, 0))

    def update(self):
        pass

    def event(self, event):
        pass


class Label(Object):

    def __init__(self, text, pos, font_size=20, color=wrapper.MAIN_COLOR, shadow=True,
                 shadow_color=wrapper.SECONDARY_COLOR,
                 centered=False,
                 inverted=False, font="assets/fonts/Blockbit.ttf"):
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.shadow = shadow
        self.shadow_color = shadow_color
        self.centered = centered
        self.inverted = inverted
        super().__init__(pos, self.font.size(text))

    def render(self, window, x_offset=0, y_offset=0):
        utils.write_text(self.text, window, (self.pos[0] + x_offset, self.pos[1] + y_offset), self.font,
                         self.color.color, self.shadow, self.shadow_color.color,
                         self.centered, self.inverted)


def _none(*args, **kwargs):
    pass


class Button(Label):

    def __init__(self, text, pos, size=(int(pygame.display.get_window_size()[0] / 2), 50), centered=False, inverted=False):
        if centered:
            pos = (int(pos[0] - size[0] / 2), pos[1])
        super().__init__(text, pos, 30, wrapper.SECONDARY_COLOR, False, centered=True, inverted=inverted)
        self.size = size
        self.org_pos = pos
        self.org_size = size
        self.btn_centered = centered
        self.hovered = False
        self.left_pressed = False
        self.right_pressed = False
        self.on_enter = _none
        self.on_hover = _none
        self.on_exit = _none
        self.on_left_pressed = _none
        self.on_right_pressed = _none
        self.on_left_down = _none
        self.on_right_down = _none
        self.on_left_up = _none
        self.on_right_up = _none

    def update(self):
        self.pos = self.org_pos
        self.size = self.org_size
        mouse_pos = pygame.mouse.get_pos()
        if self.pos[0] <= mouse_pos[0] <= self.pos[0] + self.size[0] and self.pos[1] <= mouse_pos[1] <= self.pos[1] + \
                self.size[1]:
            if not self.hovered:
                self.on_enter(self)
                wrapper.main.hover_sound.play()
            self.on_hover(self)
            self.hovered = True
        elif self.hovered:
            self.hovered = False
            self.on_exit(self)

        if self.left_pressed:
            self.on_left_pressed(self)
        if self.right_pressed:
            self.on_right_pressed(self)

        if self.hovered:
            offset = 5
            self.pos = (self.org_pos[0] - offset, self.org_pos[1] - offset)
            self.size = (self.org_size[0] + offset * 2, self.org_size[1] + offset * 2)

    def left_down(self):
        if self.hovered:
            self.left_pressed = True
            self.on_left_down(self)

    def right_down(self):
        if self.hovered:
            self.right_pressed = True
            self.on_right_down(self)

    def left_up(self):
        if self.left_pressed:
            self.left_pressed = False
            self.on_left_up(self)
            wrapper.main.click_sound.play()

    def right_up(self):
        if self.right_pressed:
            self.right_pressed = False
            self.on_right_up(self)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_down()
            elif event.button == 3:
                self.right_down()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.left_up()
            elif event.button == 3:
                self.right_up()

    def render(self, window, x_offset=0, y_offset=0):
        offset = 5
        centered = self.btn_centered
        pygame.draw.rect(window, wrapper.SECONDARY_COLOR.color,
                         pygame.Rect(self.pos[0] + offset, self.pos[1] + offset, self.size[0], self.size[1]))
        pygame.draw.rect(window, wrapper.MAIN_COLOR.color,
                         pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
        super().render(window, int(self.size[0] / 2), int(self.size[1] / 2 - self.font.size(self.text)[1] / 2))


class Ball(Object):

    def __init__(self, pos):
        super().__init__(pos, (30, 30))
        self.booster_size = (14, 14)
        self.direction = random.choice([-1, 1])
        self.angle = random.randint(-3, 3) / 10
        self.speed = 0.2
        self.boost = False

    def update(self):
        boost = 3 if self.boost else 1
        self.speed = 0.2 + wrapper.main.bounces * 0.02 * boost
        self.pos[0] += self.direction * self.speed
        if self.pos[0] <= 0 or self.pos[0] >= pygame.display.get_window_size()[0] - self.size[0]:
            self.direction *= -1
        self.pos[0] = max(min(self.pos[0], pygame.display.get_window_size()[0] - self.size[0]), 0)
        self.pos[1] += self.angle * self.speed
        if self.pos[1] <= 0 or self.pos[1] >= pygame.display.get_window_size()[1] - self.size[1]:
            self.angle *= -1

    def render(self, window):
        color = wrapper.SECONDARY_COLOR
        if self.boost:
            x = bool(int(wrapper.main.cycles % 500 / 300))
            if x:
                color = utils.Color((0, 0, 0))
        pygame.draw.rect(self.surf, color.color, pygame.Rect((0, 0), self.size))
        super().render(window)


class Paddle(Object):

    def __init__(self, pos, id):
        super().__init__(pos, (15, 80))
        self.id = id
        self.direction = 1
        self.speed = 0.21

    def update(self):
        self.pos[1] += self.direction * self.speed
        self.pos[1] = max(min(self.pos[1], pygame.display.get_window_size()[1] - self.size[1]), 0)

    def render(self, window):
        pygame.draw.rect(self.surf, wrapper.MAIN_COLOR.color, pygame.Rect((0, 0), self.size))
        super().render(window)


class Player(Paddle):

    def __init__(self, pos, id, controls=None):
        super().__init__(pos, id)
        if controls is None:
            controls = {
                "up": pygame.K_w,
                "down": pygame.K_s
            }
        self.controls = controls

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.controls["up"]:
                self.direction = -1
            elif event.key == self.controls["down"]:
                self.direction = 1


class GameScene(Scene):

    def __init__(self):
        super().__init__()
        self.ball = Ball((0, 0))
        self.ball.pos = [int(pygame.display.get_window_size()[0] / 2 - self.ball.size[0] / 2),
                         int(pygame.display.get_window_size()[1] / 2 - self.ball.size[1] / 2)]
        self.objects.append(self.ball)

    def event(self, event):
        super().event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                wrapper.main.secondary_scene = self
                wrapper.main.current_scene = wrapper.main.scenes["Pause"]()

    def render(self, window):
        segments = 7
        gap = 30
        segment_width = 10
        height = pygame.display.get_window_size()[1]
        middle = pygame.display.get_window_size()[0] / 2
        segment_height = int((height - gap * (segments - 1)) / segments)
        for i in range(segments):
            pygame.draw.rect(window, wrapper.MAIN_COLOR.color,
                             pygame.Rect(middle - segment_width / 2, (i * (segment_height + gap)), segment_width,
                                         segment_height))
        super().render(window)
