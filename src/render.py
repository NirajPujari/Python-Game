# render.py
import pygame
import os
from constants import COLORS, ASSETS_DIR, WINDOW_SIZE, SPACING, N, TITLE, FPS

class Renderer:
    def __init__(self, game_logic):
        pygame.init()
        pygame.font.init()
        self.game = game_logic
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption(TITLE)
        logo_path = os.path.join(ASSETS_DIR, "logo.png")
        try:
            logo = pygame.image.load(logo_path)
            pygame.display.set_icon(logo)
        except Exception:
            # ignore if logo not present
            pass

        # fonts
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18)

        self.clock = pygame.time.Clock()

    def draw_board(self):
        self.screen.fill(COLORS['back'])
        board_margin = SPACING * 2
        cell_w = (WINDOW_SIZE - board_margin * 2) / N
        for i in range(N):
            for j in range(N):
                n = int(self.game.grid[i, j])
                rect_x = board_margin + j * cell_w + SPACING / 2
                rect_y = board_margin + i * cell_w + SPACING / 2
                rect_w = cell_w - SPACING
                rect_h = rect_w
                color = COLORS.get(n, COLORS[2048])
                pygame.draw.rect(self.screen, color, pygame.Rect(rect_x, rect_y, rect_w, rect_h), border_radius=8)
                if n != 0:
                    # dynamic font size based on digits
                    txt = str(n)
                    font_size = max(20, int(rect_w / (len(txt) * 0.6)))
                    tile_font = pygame.font.SysFont("Arial", font_size, bold=True)
                    text_surface = tile_font.render(txt, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2, rect_y + rect_h / 2))
                    self.screen.blit(text_surface, text_rect)

        # Score
        score_surf = self.small_font.render(f"Score: {self.game.score}", True, (0, 0, 0))
        self.screen.blit(score_surf, (10, 10))

    def draw_center_message(self, message, sub=None):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 200))
        self.screen.blit(overlay, (0, 0))
        text = self.big_font.render(message, True, (0, 0, 0))
        trect = text.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 20))
        self.screen.blit(text, trect)
        if sub:
            small = self.font.render(sub, True, (0, 0, 0))
            srect = small.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 + 30))
            self.screen.blit(small, srect)

    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
