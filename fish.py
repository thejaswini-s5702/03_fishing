"""
Fish: swims horizontally at a fixed depth, wrapping around when it
exits the screen. Several fish types differ in speed, size, color and value.
"""

import pygame

FISH_TYPES = {
    "minnow": dict(speed=1.5, width=28, height=14, point_value=5,  color=(150, 210, 150)),
    "bass":   dict(speed=2.5, width=40, height=20, point_value=10, color=(80, 180, 220)),
    "golden": dict(speed=4.5, width=34, height=16, point_value=25, color=(240, 200, 60)),
}


class Fish:
    def __init__(self, x, y, speed, width=36, height=18, point_value=10,
                 color=(80, 180, 220), kind="bass"):
        self.x = float(x)
        self.y = y
        self.home_y = y          # remembered so a caught fish can respawn in its lane
        self.speed = speed
        self.width = width
        self.height = height
        self.point_value = point_value
        self.color = color
        self.kind = kind

    def update(self, screen_width):
        self.x += self.speed
        if self.speed > 0 and self.x > screen_width:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = screen_width

    def respawn(self, screen_width):
        """Put a caught fish back at the edge it swims in from."""
        self.y = self.home_y
        self.x = -self.width if self.speed > 0 else screen_width + self.width

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )


def create_fish(kind, x, y, direction=1):
    """Build a fish of the given type. direction is 1 (right) or -1 (left)."""
    props = FISH_TYPES[kind]
    return Fish(
        x=x, y=y,
        speed=props["speed"] * direction,
        width=props["width"], height=props["height"],
        point_value=props["point_value"], color=props["color"],
        kind=kind,
    )