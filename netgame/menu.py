import ipaddress

import pygame


WINDOW_SIZE = (704, 576)
BACKGROUND = (0, 0, 0)
PANEL = (29, 36, 49)
PANEL_BORDER = (70, 84, 105)
BUTTON = (42, 42, 42)
BUTTON_HOVER = (72, 72, 72)
BUTTON_DANGER = BUTTON
BUTTON_DANGER_HOVER = BUTTON_HOVER
TEXT = (239, 244, 252)
MUTED_TEXT = (161, 175, 194)
ACCENT = (91, 192, 222)
ERROR = (239, 106, 106)


def _font(size, bold=False):
    return pygame.font.SysFont("segoeui", size, bold=bold)


def _draw_centered_text(surface, text, font, color, center):
    rendered = font.render(text, True, color)
    surface.blit(rendered, rendered.get_rect(center=center))


def _draw_button(surface, rect, label, mouse_pos, danger=False):
    hovered = rect.collidepoint(mouse_pos)
    if danger:
        color = BUTTON_DANGER_HOVER if hovered else BUTTON_DANGER
    else:
        color = BUTTON_HOVER if hovered else BUTTON
    pygame.draw.rect(surface, color, rect, border_radius=9)
    pygame.draw.rect(surface, PANEL_BORDER, rect, width=2, border_radius=9)
    _draw_centered_text(surface, label, _font(27, bold=True), TEXT, rect.center)


def _draw_background(surface):
    surface.fill(BACKGROUND)


def _validate_ipv4(value):
    try:
        return str(ipaddress.IPv4Address(value.strip()))
    except ipaddress.AddressValueError:
        return None


def _run_ip_screen(surface, clock, mode):
    host_mode = mode == "host"
    title = "Host Game" if host_mode else "Join Game"
    prompt = (
        "Enter IPv4 address."
        if host_mode
        else "Enter IPv4 address."
    )
    action_label = "Start Game" if host_mode else "Join Game"
    input_value = ""
    error_message = ""
    input_active = True

    back_button = pygame.Rect(40, 38, 112, 44)
    input_box = pygame.Rect(142, 235, 420, 58)
    action_button = pygame.Rect(202, 340, 300, 58)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    return "back", None
                if input_box.collidepoint(event.pos):
                    input_active = True
                if action_button.collidepoint(event.pos):
                    valid_ip = _validate_ipv4(input_value)
                    if valid_ip is not None:
                        return mode, valid_ip
                    error_message = "Enter a valid IPv4 address"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back", None
                if event.key == pygame.K_RETURN:
                    valid_ip = _validate_ipv4(input_value)
                    if valid_ip is not None:
                        return mode, valid_ip
                    error_message = "Enter a valid IPv4 address"
                elif event.key == pygame.K_BACKSPACE:
                    input_value = input_value[:-1]
                    error_message = ""
                elif input_active and event.unicode in "0123456789.":
                    if len(input_value) < 15:
                        input_value += event.unicode
                        error_message = ""

        _draw_background(surface)
        panel = pygame.Rect(76, 96, 552, 390)
        pygame.draw.rect(surface, PANEL, panel, border_radius=16)
        pygame.draw.rect(surface, PANEL_BORDER, panel, width=2, border_radius=16)

        _draw_centered_text(
            surface, title, _font(43, bold=True), TEXT, (WINDOW_SIZE[0] // 2, 142)
        )
        _draw_centered_text(
            surface, prompt, _font(21), MUTED_TEXT, (WINDOW_SIZE[0] // 2, 195)
        )

        input_color = ACCENT if input_active else PANEL_BORDER
        pygame.draw.rect(surface, (18, 23, 32), input_box, border_radius=8)
        pygame.draw.rect(surface, input_color, input_box, width=2, border_radius=8)
        shown_value = input_value
        if input_active and pygame.time.get_ticks() % 1000 < 500:
            shown_value += "|"
        rendered_input = _font(30).render(shown_value, True, TEXT)
        surface.blit(rendered_input, (input_box.x + 16, input_box.y + 11))

        if error_message:
            _draw_centered_text(
                surface,
                error_message,
                _font(18),
                ERROR,
                (WINDOW_SIZE[0] // 2, 315),
            )

        _draw_button(surface, action_button, action_label, mouse_pos)
        _draw_button(surface, back_button, "Back", mouse_pos)

        pygame.display.flip()
        clock.tick(60)


def run_menu():
    pygame.init()
    pygame.mixer.quit()
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Netgame")
    clock = pygame.time.Clock()

    singleplayer_button = pygame.Rect(202, 142, 300, 58)
    host_button = pygame.Rect(202, 220, 300, 58)
    join_button = pygame.Rect(202, 298, 300, 58)
    quit_button = pygame.Rect(202, 376, 300, 58)

    try:
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "quit", None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if singleplayer_button.collidepoint(event.pos):
                        return "host", "127.0.0.1"
                    elif host_button.collidepoint(event.pos):
                        result = _run_ip_screen(surface, clock, "host")
                        if result[0] != "back":
                            return result
                    elif join_button.collidepoint(event.pos):
                        result = _run_ip_screen(surface, clock, "join")
                        if result[0] != "back":
                            return result
                    elif quit_button.collidepoint(event.pos):
                        return "quit", None

            _draw_background(surface)
            _draw_button(surface, singleplayer_button, "Singleplayer", mouse_pos)
            _draw_button(surface, host_button, "Host Game", mouse_pos)
            _draw_button(surface, join_button, "Join Game", mouse_pos)
            _draw_button(surface, quit_button, "Quit", mouse_pos, danger=True)

            pygame.display.flip()
            clock.tick(60)
    finally:
        pygame.quit()


def show_error(message):
    pygame.init()
    pygame.mixer.quit()
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Netgame - Connection Error")
    clock = pygame.time.Clock()
    close_button = pygame.Rect(252, 390, 200, 54)

    lines = []
    remaining = str(message)
    while remaining:
        if len(remaining) <= 58:
            lines.append(remaining)
            break
        split_at = remaining.rfind(" ", 0, 58)
        if split_at <= 0:
            split_at = 58
        lines.append(remaining[:split_at])
        remaining = remaining[split_at:].lstrip()

    try:
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_RETURN,
                ):
                    return
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and close_button.collidepoint(event.pos)
                ):
                    return

            _draw_background(surface)
            panel = pygame.Rect(76, 112, 552, 352)
            pygame.draw.rect(surface, PANEL, panel, border_radius=16)
            pygame.draw.rect(surface, PANEL_BORDER, panel, width=2, border_radius=16)
            _draw_centered_text(
                surface,
                "Unable to Connect",
                _font(39, bold=True),
                ERROR,
                (WINDOW_SIZE[0] // 2, 170),
            )
            for index, line in enumerate(lines):
                _draw_centered_text(
                    surface,
                    line,
                    _font(21),
                    TEXT,
                    (WINDOW_SIZE[0] // 2, 240 + index * 30),
                )
            _draw_button(surface, close_button, "Close", mouse_pos)
            pygame.display.flip()
            clock.tick(60)
    finally:
        pygame.quit()
