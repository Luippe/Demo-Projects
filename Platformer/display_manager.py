import pygame


LOGICAL_SIZE = (1920, 1080)
LETTERBOX_COLOR = (0, 0, 0)

_display_surface = None
_logical_surface = None
_scaled_surface = None
_viewport = pygame.Rect((0, 0), LOGICAL_SIZE)


def _calculate_viewport(display_size):
    display_width, display_height = display_size
    logical_width, logical_height = LOGICAL_SIZE
    scale = min(display_width / logical_width, display_height / logical_height)
    width = max(1, round(logical_width * scale))
    height = max(1, round(logical_height * scale))
    return pygame.Rect(
        (display_width - width) // 2,
        (display_height - height) // 2,
        width,
        height,
    )


def initialize():
    global _display_surface, _logical_surface, _scaled_surface, _viewport
    if _display_surface is None:
        pygame.init()
        _display_surface = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF
        )
        _logical_surface = pygame.Surface(LOGICAL_SIZE).convert()
        _viewport = _calculate_viewport(_display_surface.get_size())
        if _viewport.size != LOGICAL_SIZE:
            _scaled_surface = pygame.Surface(_viewport.size).convert()
    return _logical_surface


def present(surface=None):
    if _display_surface is None:
        initialize()
    source = _logical_surface if surface is None else surface
    if _viewport.size != _display_surface.get_size():
        _display_surface.fill(LETTERBOX_COLOR)
    if source.get_size() == _viewport.size:
        scaled_surface = source
    else:
        pygame.transform.scale(source, _viewport.size, _scaled_surface)
        scaled_surface = _scaled_surface
    _display_surface.blit(scaled_surface, _viewport.topleft)
    pygame.display.flip()


def to_logical_position(position):
    if not _viewport.collidepoint(position):
        return LOGICAL_SIZE
    logical_width, logical_height = LOGICAL_SIZE
    x = (position[0] - _viewport.x) * logical_width // _viewport.width
    y = (position[1] - _viewport.y) * logical_height // _viewport.height
    return int(x), int(y)


def get_mouse_pos():
    return to_logical_position(pygame.mouse.get_pos())
