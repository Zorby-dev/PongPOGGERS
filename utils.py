import importlib.util


class Color:

    def __init__(self, color):
        self.color = color


def import_file(file: str, name: str = "module"):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def import_class(file: str):
    file = import_file(file)
    return getattr(file, file.__name__)


def write_text(text, surface, pos, font, color=(0, 0, 0), shadow=True, shadow_color=(255, 255, 255), centered=False,
               inverted=False):
    text = str(text)
    font_size = font.size(text)[0]
    if inverted:
        pos = (pos[0] - font_size, pos[1])
    if centered:
        pos = (pos[0] - int(font_size / 2), pos[1])
    if shadow:
        shadow = font.render(text, False, shadow_color)
        offset = int(font.get_height() / 10)
        surface.blit(shadow, (pos[0] + offset, pos[1] + offset))
    text = font.render(text, False, color)
    surface.blit(text, pos)
