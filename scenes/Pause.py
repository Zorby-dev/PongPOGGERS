from source import *
import wrapper
import utils

__name__ = "Pause"


class Pause(Scene):

    def __init__(self):
        super().__init__()
        self.objects.append(Label("GAME PAUSED", (pygame.display.get_window_size()[0] / 2, 60), 90,
                                  color=wrapper.SECONDARY_COLOR, shadow_color=wrapper.MAIN_COLOR, centered=True))

        resume = Button("RESUME", (pygame.display.get_window_size()[0] / 2, 200), centered=True)
        self.objects.append(resume)

        def on_resume_press(button):
            wrapper.main.current_scene = wrapper.main.secondary_scene
            wrapper.main.secondary_scene = None

        resume.on_left_up = on_resume_press

        restart = Button("RESTART", (pygame.display.get_window_size()[0] / 2, 270), centered=True)
        self.objects.append(restart)

        def on_restart_press(button):
            wrapper.main.current_scene = wrapper.main.scenes[wrapper.main.secondary_scene.__class__.__name__]()
            wrapper.main.secondary_scene = None

        restart.on_left_up = on_restart_press

        main_menu = Button("MAIN MENU", (pygame.display.get_window_size()[0] / 2, 270), centered=True)
        self.objects.append(main_menu)

        def on_main_menu_press(button):
            wrapper.main.current_scene = wrapper.main.scenes["MainMenu"]()
            wrapper.main.secondary_scene = None

        main_menu.on_left_up = on_main_menu_press

    def update(self):
        super().update()

    def event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_m:
                wrapper.main.current_scene = wrapper.main.scenes["MultiPlayer"]()
            elif event.key == pygame.K_s:
                wrapper.main.current_scene = wrapper.main.scenes["SinglePlayer"]()
        super().event(event)
