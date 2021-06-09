import pygame
import glob
import utils

print("started")
pygame.init()
pygame.font.init()
pygame.mixer.init()

hover_sound = pygame.mixer.Sound("assets/sounds/hover.mp3")
click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")
ping_sound = pygame.mixer.Sound("assets/sounds/ping.mp3")
goal_sound = pygame.mixer.Sound("assets/sounds/goal.wav")

SCREEN_SIZE = (1000, 600)

window = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Pong POGGERS")

scenes = {}
current_scene = None
secondary_scene = None

for file_name in glob.glob("./scenes/*.py"):
    scene = utils.import_class(file_name)
    scenes[scene.__name__] = scene
    try:
        if scene.__first_scene__:
            current_scene = scene()
    except AttributeError:
        pass
if current_scene is None:
    current_scene = tuple(scenes.values())[0]()

running = True
cycles = 0
bounces = 0
while running:

    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            current_scene.event(event)
    current_scene.update()

    current_scene.render(window)
    pygame.display.flip()
    cycles += 1

pygame.quit()
