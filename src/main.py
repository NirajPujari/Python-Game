# main.py
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
    render = Renderer(game)

    running = True
    show_game_over = False
    show_win = False

    while running:
        render.draw_board()

        if game.has_won():
            show_win = True
            render.draw_center_message("You won!", "Press R to restart or Q to quit")

        if not game.can_move():
            show_game_over = True
            render.draw_center_message("Game Over", "Press R to restart or Q to quit")

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                if event.key in (K_q, K_ESCAPE):
                    running = False

                if event.key == K_r:
                    game.reset()
                    show_game_over = False
                    show_win = False

                # Only accept moves if game not over or won
                if not show_game_over and not show_win:
                    if event.key in KEY_TO_MOVE:
                        move = KEY_TO_MOVE[event.key]
                        # translate 'u','d','l','r' used in logic to same as gamespace:
                        move_map = {'u': 'u', 'd': 'd', 'l': 'l', 'r': 'r'}
                        moved = game.make_move(move_map[move])
                        if moved:
                            game.new_number(k=1)

        render.update()

    pygame.quit()

if __name__ == "__main__":
    main()
