import curses

fire_chars = " .,:-=+*#%@"


def get_fire_color(value, block=False):
    if value < 8:
        return curses.color_pair(11 if block else 1)
    if value < 16:
        return curses.color_pair(12 if block else 2)
    if value < 24:
        return curses.color_pair(13 if block else 3)
    if value < 32:
        return curses.color_pair(14 if block else 4)
    return curses.color_pair(15 if block else 5)


def get_fire_char(value, max_intensity):
    if max_intensity <= 0:
        return fire_chars[0]

    index = int(value / max_intensity * (len(fire_chars) - 1))
    index = max(0, min(len(fire_chars) - 1, index))
    return fire_chars[index]


def render_ascii(stdscr, fire, previous_fire, height, width, max_intensity):

    for y in range(height):
        for x in range(width - 1):
            value = fire[y][x]

            if previous_fire is not None and previous_fire[y][x] == value:
                continue

            char = get_fire_char(value, max_intensity)
            stdscr.addstr(y, x, char)


def render_color(stdscr, fire, previous_fire, height, width, max_intensity):

    for y in range(height):
        for x in range(width - 1):
            value = fire[y][x]

            if previous_fire is not None and previous_fire[y][x] == value:
                continue

            char = get_fire_char(value, max_intensity)
            color = get_fire_color(value)

            stdscr.addstr(y, x, char, color)


def render_block(stdscr, fire, previous_fire, height, width, max_intensity):

    for y in range(height):
        for x in range(width - 1):
            value = fire[y][x]

            if previous_fire is not None and previous_fire[y][x] == value:
                continue

            if value == 0:
                stdscr.addstr(y, x, " ")
                continue

            color = get_fire_color(value, block=True)

            stdscr.addstr(y, x, " ", color)
