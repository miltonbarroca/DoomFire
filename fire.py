import random

DEFAULT_FIRE_CONFIG = {
    "source_intensity": 36,
    "max_decay": 4,
    "frame_delay": 0.05,
}


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def normalize_fire_config(config=None):
    normalized = DEFAULT_FIRE_CONFIG.copy()

    if config is not None:
        normalized.update(config)

    normalized["source_intensity"] = clamp(normalized["source_intensity"], 1, 100)
    normalized["max_decay"] = clamp(normalized["max_decay"], 0, normalized["source_intensity"])
    normalized["frame_delay"] = clamp(normalized["frame_delay"], 0.01, 0.20)

    return normalized


def create_fire(height, width, config=None):
    fire = [[0 for _ in range(width)] for _ in range(height)]
    source_intensity = normalize_fire_config(config)["source_intensity"]

    for x in range(width):
        fire[height - 1][x] = source_intensity

    return fire


def propagate_fire(fire, height, width, config=None):
    settings = normalize_fire_config(config)
    source_intensity = settings["source_intensity"]
    max_decay = settings["max_decay"]
    previous_fire = [row[:] for row in fire]

    for y in range(height - 1):
        for x in range(width):
            decay = random.randint(0, max_decay)
            below = previous_fire[y + 1][x]
            new_value = below - decay

            if new_value < 0:
                new_value = 0

            fire[y][x] = new_value

    for x in range(width):
        fire[height - 1][x] = source_intensity
