import pygame
import os
from constants import COLORS, ASSETS_DIR, WINDOW_SIZE, SPACING, N, TITLE, FPS

# animation config
ANIM_FRAMES = 12
MERGE_POP_FRAMES = 10

def ease_out_quad(t):
    return 1 - (1 - t) * (1 - t)

class TileSprite:
    def __init__(self, value, start_px, end_px, merged=False):
        self.value = value
        self.start = start_px
        self.end = end_px
        self.merged = merged
        self.frame = 0
        self.pop_frame = 0
        self.done = False

    def update(self):
        if self.frame < ANIM_FRAMES:
            self.frame += 1
        elif self.merged and self.pop_frame < MERGE_POP_FRAMES:
            self.pop_frame += 1
        else:
            self.done = True

    def is_animating(self):
        return not self.done

    def current_pos(self):
        if self.frame >= ANIM_FRAMES:
            return self.end
        t = ease_out_quad(self.frame / ANIM_FRAMES)
        x = self.start[0] + (self.end[0] - self.start[0]) * t
        y = self.start[1] + (self.end[1] - self.start[1]) * t
        return (x, y)

    def current_scale(self):
        if self.frame < ANIM_FRAMES:
            return 1.0
        if self.merged:
            half = MERGE_POP_FRAMES // 2
            if self.pop_frame <= half:
                return 1.0 + 0.25 * (self.pop_frame / half)
            else:
                return 1.0 + 0.25 * (1 - (self.pop_frame - half) / max(1, MERGE_POP_FRAMES - half))
        return 1.0

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
            pass

        # fonts
        self.base_tile_font = "Arial"
        self.small_font = pygame.font.SysFont(self.base_tile_font, 16)
        self.score_font = pygame.font.SysFont(self.base_tile_font, 20, bold=True)
        self.big_font = pygame.font.SysFont(self.base_tile_font, 36, bold=True)

        self.clock = pygame.time.Clock()
        self.sprites = []

    def cell_center_px(self, r, c):
        board_margin = SPACING * 3
        cell_w = (WINDOW_SIZE - board_margin * 2) / N
        rect_x = board_margin + c * cell_w + SPACING / 2
        rect_y = board_margin + r * cell_w + SPACING / 2
        rect_w = cell_w - SPACING
        rect_h = rect_w
        cx = rect_x + rect_w / 2
        cy = rect_y + rect_h / 2
        size = rect_w, rect_h
        return (cx, cy), size

    def draw_board_tiles_static(self):
        self.screen.fill(COLORS['back'])
        board_margin = SPACING * 3
        cell_w = (WINDOW_SIZE - board_margin * 2) / N
        for i in range(N):
            for j in range(N):
                rect_x = board_margin + j * cell_w + SPACING / 2
                rect_y = board_margin + i * cell_w + SPACING / 2
                rect_w = cell_w - SPACING
                rect_h = rect_w
                pygame.draw.rect(self.screen, COLORS[0], pygame.Rect(rect_x, rect_y, rect_w, rect_h), border_radius=8)

        animated_ends = { (int(s.end[2]), int(s.end[3])) for s in self.sprites if not s.is_animating() }
        animated_starts = set()
        for s in self.sprites:
            pass
        
        for i in range(N):
            for j in range(N):
                n = int(self.game.grid[i, j])
                if n == 0:
                    continue
                if any((s.end_grid == (i,j) and s.is_animating()) for s in self.sprites):
                    continue
                # draw static tile
                (cx, cy), (rw, rh) = self.cell_center_px(i, j)
                rect_x = cx - rw/2
                rect_y = cy - rh/2
                color = COLORS.get(n, COLORS[2048])
                pygame.draw.rect(self.screen, color, pygame.Rect(rect_x, rect_y, rw, rh), border_radius=8)
                # smaller dynamic font
                txt = str(n)
                font_size = max(16, int(rw / (len(txt) * 0.85)))
                tile_font = pygame.font.SysFont(self.base_tile_font, font_size, bold=True)
                text_surface = tile_font.render(txt, True, (0,0,0))
                text_rect = text_surface.get_rect(center=(cx, cy))
                self.screen.blit(text_surface, text_rect)

    def create_sprites_from_movements(self, movements):
        sprites = []
        for mv in movements:
            end_r, end_c = mv['end']
            end_center, size = self.cell_center_px(end_r, end_c)
            start_centers = []
            for (sr, sc) in mv['starts']:
                scenter, _ = self.cell_center_px(sr, sc)
                start_centers.append(scenter)
            if not start_centers:
                start_centers = [end_center]
            avg_x = sum(p[0] for p in start_centers) / len(start_centers)
            avg_y = sum(p[1] for p in start_centers) / len(start_centers)
            sprite = TileSprite(mv['value'], (avg_x, avg_y), (end_center[0], end_center[1]), merged=mv['merged'])
            sprite.start_grid = mv['starts'][0] if mv['starts'] else None
            sprite.end_grid = (end_r, end_c)
            sprites.append(sprite)
        self.sprites = sprites

    def update_and_draw_sprites(self):
        # draw sprites on top of board
        for s in self.sprites:
            pos = s.current_pos()
            scale = s.current_scale()
            # size
            _, (rw, rh) = self.cell_center_px(0,0)
            w = rw * scale
            h = rh * scale
            rect = pygame.Rect(0,0,w,h)
            rect.center = (pos[0], pos[1])
            color = COLORS.get(s.value, COLORS[2048])
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            # number
            txt = str(s.value)
            font_size = max(14, int(w / (len(txt) * 0.95)))
            tile_font = pygame.font.SysFont(self.base_tile_font, font_size, bold=True)
            text_surface = tile_font.render(txt, True, (0,0,0))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
            s.update()
        # remove done sprites
        self.sprites = [s for s in self.sprites if not s.done]

    def draw_score_and_hud(self):
        score_surf = self.score_font.render(f"Score: {self.game.score}", True, (0, 0, 0))
        self.screen.blit(score_surf, (10, 10))
        hint = self.small_font.render("R: Restart   Q/Esc: Quit", True, (0,0,0))
        self.screen.blit(hint, (10, WINDOW_SIZE - 28))

    def draw_center_message(self, message, sub=None):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 220))
        self.screen.blit(overlay, (0, 0))
        text = self.big_font.render(message, True, (0, 0, 0))
        trect = text.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 20))
        self.screen.blit(text, trect)
        if sub:
            small = self.score_font.render(sub, True, (0, 0, 0))
            srect = small.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2 + 30))
            self.screen.blit(small, srect)

    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
