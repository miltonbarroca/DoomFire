import curses
import time

from fire import DEFAULT_FIRE_CONFIG, clamp, create_fire, normalize_fire_config, propagate_fire
from render import render_ascii, render_block, render_color

OPTION_FIELDS = [
    {
        "key": "source_intensity",
        "label": "Source intensity",
        "minimum": 1,
        "maximum": 100,
        "step": 1,
    },
    {
        "key": "max_decay",
        "label": "Max decay",
        "minimum": 0,
        "maximum": 20,
        "step": 1,
    },
    {
        "key": "frame_delay",
        "label": "Frame delay",
        "minimum": 0.01,
        "maximum": 0.20,
        "step": 0.01,
    },
]

MODE_ITEMS = [
    ("ascii", "ASCII mode"),
    ("color", "Color mode"),
    ("block", "Block mode"),
]


def init_colors():
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_BLACK, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_MAGENTA, -1)
    curses.init_pair(5, curses.COLOR_WHITE, -1)
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(13, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(14, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(15, curses.COLOR_WHITE, curses.COLOR_WHITE)


def format_option_value(key, value):
    if key == "frame_delay":
        return f"{value:.2f}s"
    return str(value)


def adjust_option(config, field, direction):
    key = field["key"]
    current_value = config[key]
    updated_value = current_value + (field["step"] * direction)

    if isinstance(field["step"], float):
        updated_value = round(updated_value, 2)

    config[key] = clamp(updated_value, field["minimum"], field["maximum"])

    if key == "source_intensity":
        config["max_decay"] = clamp(config["max_decay"], 0, config["source_intensity"])


def draw_main_menu(stdscr, selected_index, selected_mode):
    stdscr.clear()
    stdscr.addstr(2, 2, "DOOM FIRE")
    stdscr.addstr(4, 2, "Select mode")

    menu_items = [
        "ASCII mode",
        "Color mode",
        "Block mode",
        "Options",
        "Exit",
    ]

    for index, label in enumerate(menu_items):
        prefix = "> " if index == selected_index else "  "
        marker = " *" if index == selected_mode and index < len(MODE_ITEMS) else ""
        stdscr.addstr(6 + index, 2, f"{prefix}{label}{marker}")

    stdscr.addstr(13, 2, "Up/Down to navigate")
    stdscr.addstr(14, 2, "Enter on a mode to start")
    stdscr.addstr(15, 2, "* selected mode")
    stdscr.refresh()


def options_menu(stdscr, config):
    selected_index = 0

    while True:
        stdscr.clear()
        stdscr.addstr(2, 2, "OPTIONS")

        for index, field in enumerate(OPTION_FIELDS):
            key = field["key"]
            prefix = "> " if index == selected_index else "  "
            value = format_option_value(key, config[key])
            stdscr.addstr(4 + index, 2, f"{prefix}{field['label']}: {value}")

        stdscr.addstr(9, 2, "Left/Right to change")
        stdscr.addstr(10, 2, "Up/Down to navigate")
        stdscr.addstr(11, 2, "R to reset")
        stdscr.addstr(12, 2, "Enter or Esc to go back")
        stdscr.refresh()

        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected_index = (selected_index - 1) % len(OPTION_FIELDS)
        elif key in (curses.KEY_DOWN, ord("j")):
            selected_index = (selected_index + 1) % len(OPTION_FIELDS)
        elif key in (curses.KEY_LEFT, ord("h")):
            adjust_option(config, OPTION_FIELDS[selected_index], -1)
        elif key in (curses.KEY_RIGHT, ord("l")):
            adjust_option(config, OPTION_FIELDS[selected_index], 1)
        elif key in (ord("r"), ord("R")):
            config.clear()
            config.update(DEFAULT_FIRE_CONFIG)
        elif key in (27, 10, 13):
            return normalize_fire_config(config)


def menu(stdscr, config):
    selected_item = 0
    selected_mode = 0

    while True:
        draw_main_menu(stdscr, selected_item, selected_mode)
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected_item = (selected_item - 1) % 5
        elif key in (curses.KEY_DOWN, ord("j")):
            selected_item = (selected_item + 1) % 5
        elif key in (10, 13):
            if selected_item < len(MODE_ITEMS):
                return MODE_ITEMS[selected_item][0], normalize_fire_config(config)
            if selected_item == 3:
                config = options_menu(stdscr, config)
            if selected_item == 4:
                return "exit", normalize_fire_config(config)


def render_frame(stdscr, mode, fire, previous_fire, visible_height, width, config):
    max_intensity = config["source_intensity"]

    if mode == "ascii":
        render_ascii(stdscr, fire, previous_fire, visible_height, width, max_intensity)
    elif mode == "color":
        render_color(stdscr, fire, previous_fire, visible_height, width, max_intensity)
    elif mode == "block":
        render_block(stdscr, fire, previous_fire, visible_height, width, max_intensity)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    init_colors()

    config = DEFAULT_FIRE_CONFIG.copy()
    mode, config = menu(stdscr, config)

    if mode == "exit":
        return

    stdscr.nodelay(True)

    height, width = stdscr.getmaxyx()
    visible_height = max(1, height - 1)
    simulation_height = visible_height + 1
    stdscr.clear()

    fire = create_fire(simulation_height, width, config)
    previous_fire = None

    while True:
        propagate_fire(fire, simulation_height, width, config)
        render_frame(stdscr, mode, fire, previous_fire, visible_height, width, config)
        stdscr.refresh()
        previous_fire = [row[:] for row in fire]
        time.sleep(config["frame_delay"])


curses.wrapper(main)
