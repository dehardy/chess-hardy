import pygame
from chess_api import *

def main():
    pygame.init()
    my_display = pygame.display.set_mode()
    my_display.fill((127, 127, 127))
    pygame.event.set_blocked(None)
    pygame.event.clear()
    width = my_display.get_width()
    height = my_display.get_height()
    cell_width = 100
    cell_height = 100
    cells = [[None] * 8 for i in range(8)]
    black = False

    for row in range(8):
        for col in range(8):
            cell = my_display.subsurface((row * cell_width, col * cell_height, cell_width, cell_height))
            if not black:
                cell.fill((255, 255, 255))
            else:
                cell.fill((0, 0, 0))
            black = not black
            cells[row][col] = cell
        black = not black #needed for correct colors

    pygame.display.flip()
    B = Board()
    update_image(cells, B)

    pygame.event.set_allowed([pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
    event = pygame.event.wait()
    print(event)

def update_image(cells, gamestate):
    grid = gamestate.get_grid()
    letter_font = pygame.font.Font(pygame.font.get_default_font(), 75)
    for x in range(8):
        for y in range(8):
            piece = grid[x][y]
            if isinstance(piece, Pawn):
                text = letter_font.render("P", True, ((255, 0, 0)))
                cells[x][y].blit(text, (0, 0))
            elif isinstance(piece, Rook):
                text = letter_font.render("R", True, ((255, 0, 0)))
                cells[x][y].blit(text, (0, 0))
            elif isinstance(piece, Bishop):
                text = letter_font.render("B", True, ((255, 0, 0)))
                cells[x][y].blit(text, (0, 0))            
            elif isinstance(piece, Knight):
                text = letter_font.render("Kn", True, ((255, 0, 0)))
                cells[x][y].blit(text, (0, 0))
            elif isinstance(piece, Queen):
                text = letter_font.render("Q", True, ((255, 0, 0)))
                cells[x][y].blit(text, (0, 0))
            elif isinstance(piece, King):
                text = letter_font.render("Ki", True, ((255, 0, 0)))
                cells[x][y].blit(text, (0, 0))
                
    pygame.display.flip()
if __name__ == "__main__":
    main()