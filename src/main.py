import pygame
from pygame.locals import *
from gameLogic import GameLogic
from render import Renderer

KEY_TO_MOVE = {
    K_UP: 'u',
    K_DOWN: 'd',
    K_LEFT: 'l',
    K_RIGHT: 'r'
}

def main():
    game = GameLogic()
    renderer = Renderer(game)

    running = True
    show_game_over = False
    show_win = False
    animating = False

    while running:
        renderer.draw_board_tiles_static()

        renderer.update_and_draw_sprites()

        # HUD
        renderer.draw_score_and_hud()

        if game.has_won() and not renderer.sprites:
            show_win = True
            renderer.draw_center_message("You won!", "Press R to restart or Q to quit")
        if not game.can_move() and not renderer.sprites:
            show_game_over = True
            renderer.draw_center_message("Game Over", "Press R to restart or Q to quit")

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                if event.key in (K_q, K_ESCAPE):
                    running = False

                if event.key == K_r:
                    game.reset()
                    renderer.sprites = []
                    show_game_over = False
                    show_win = False

                if not renderer.sprites and not show_game_over and not show_win:
                    if event.key in KEY_TO_MOVE:
                        move = KEY_TO_MOVE[event.key]
                        moved, gained, movements = game.move_and_get_changes(move)
                        if moved:
                            renderer.create_sprites_from_movements(movements)
                        else:
                            pass

        if not hasattr(main, "_prior_sprites_count"):
            main._prior_sprites_count = 0
        if main._prior_sprites_count > 0 and len(renderer.sprites) == 0:
            # sprites just finished: spawn a new tile if any empty space
            if any(game.grid.flatten() == 0):
                game.new_number(k=1)
        main._prior_sprites_count = len(renderer.sprites)

        renderer.update()

    pygame.quit()

if __name__ == "__main__":
    main()
