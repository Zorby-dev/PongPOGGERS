from source import *
import wrapper
import utils

__name__ = "MainMenu"


class MainMenu(Scene):
    __first_scene__ = True

    def __init__(self):
        super().__init__()
        self.objects.append(Label("PONG", (pygame.display.get_window_size()[0] / 2, 50), 25, centered=True))
        self.objects.append(Label("POGGERS", (pygame.display.get_window_size()[0] / 2, 60), 90,
                                  color=wrapper.SECONDARY_COLOR, shadow_color=wrapper.MAIN_COLOR, centered=True))

        classic = Button("CLASSIC", (pygame.display.get_window_size()[0] / 2, 200), centered=True)
        self.objects.append(classic)

        def on_classic_press(button):
            wrapper.main.current_scene = wrapper.main.scenes["SinglePlayer"]()

        classic.on_left_up = on_classic_press

        versus = Button("VERSUS", (pygame.display.get_window_size()[0] / 2, 270), centered=True)
        self.objects.append(versus)

        def on_versus_press(button):
            wrapper.main.current_scene = wrapper.main.scenes["MultiPlayer"]()

        versus.on_left_up = on_versus_press

        self.objects.append(Button("CAMPAIGN", (pygame.display.get_window_size()[0] / 2, 340), centered=True))
        self.objects.append(Button("RANKED", (pygame.display.get_window_size()[0] / 2, 410), centered=True))

    def update(self):
        super().update()

    def event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_m:
                wrapper.main.current_scene = wrapper.main.scenes["MultiPlayer"]()
            elif event.key == pygame.K_s:
                wrapper.main.current_scene = wrapper.main.scenes["SinglePlayer"]()
        super().event(event)
