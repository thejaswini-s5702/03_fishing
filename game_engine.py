"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic, including player-controlled casting and the round timer.
"""

from game.hook import Hook, IDLE
from game.fish import create_fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y

ROUND_SECONDS = 30


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a fresh round: new hook, new fish, score 0, timer 30s."""
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            create_fish("minnow", x=100, y=160, direction=1),
            create_fish("bass",   x=400, y=230, direction=-1),
            create_fish("golden", x=250, y=300, direction=1),
            create_fish("minnow", x=550, y=370, direction=-1),
            create_fish("bass",   x=50,  y=420, direction=1),
        ]
        self.hooked_fish = None
        self.score = 0
        self.time_left = float(ROUND_SECONDS)
        self.game_over = False

    def handle_cast(self):
        """Called when the player presses the cast key."""
        if not self.game_over:
            self.hook.start_cast()   # Hook ignores this unless it is idle

    def restart(self):
        if self.game_over:
            self.reset()

    def update(self, dt):
        """dt = seconds since the last frame."""
        if self.game_over:
            return

        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish.respawn(WIDTH)      # keep the pond stocked
                self.fish_list.append(self.hooked_fish)
                self.hooked_fish = None
        else:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def draw(self, surface, font):
        from game import renderer
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Time: {int(self.time_left) + (1 if self.time_left % 1 else 0)}",
                           (WIDTH - 130, 10))
        if self.game_over:
            renderer.draw_banner(surface, font, f"Time's up!  Final score: {self.score}")
            renderer.draw_text(surface, font, "Press R to play again",
                               (WIDTH // 2 - 130, HEIGHT // 2 + 30))
        else:
            renderer.draw_text(surface, font, "SPACE: cast", (10, HEIGHT - 30))