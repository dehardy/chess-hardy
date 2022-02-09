import pygame
from chess_api import *


#Sprite class for each individual cell on the chess board
class Cell(pygame.sprite.Sprite):

    def __init__(self, color, left, right, width, height, piece=None):

        pygame.sprite.Sprite.__init__(self)

        self.piece = piece
        self.cell_rect = pygame.Rect(left, right, width, height)
        self.cell_sub =  pygame.display.get_surface().subsurface(self.cell_rect)
        self.color = color
        self.selected = False
        self.update()

    def update(self):
        if self.color == "black":
            if self.selected:
                self.cell_sub.fill((27, 127, 255))
            else:
                self.cell_sub.fill((255, 255, 255))
        else:
            if self.selected:
                self.cell_sub.fill((0, 0, 127))
            else:
                self.cell_sub.fill((0, 0, 0))

    def get_subsurface(self):
        return self.cell_sub

    def get_rect(self):
        return self.cell_rect
            
    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.piece = piece

    def toggle_selection(self):
        self.selected = not self.selected



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
    cells_list = [[None] * 8 for i in range(8)]
    cells_group = pygame.sprite.Group()

    black = False

    for row in range(8):
        for col in range(8):
            if black: sprite_cell = Cell("black", col * cell_width, row * cell_height, cell_width, cell_height)
            else: sprite_cell = Cell("white", col * cell_width, row * cell_height, cell_width, cell_height)

            black = not black
            cells_group.add(sprite_cell)
            cells_list[col][row] = sprite_cell
        black = not black #needed for correct colors

    pygame.display.flip()
    B = Board()
    update_image(cells_list, cells_group, B)

    pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN])
    event = pygame.event.wait()
    print(event.pos)
    update_image(cells_list, cells_group, B, event.pos)

    event = pygame.event.wait()
    


def update_image(cells, cell_group, gamestate, mouse_pos = None):
    grid = gamestate.get_grid()
    letter_font = pygame.font.Font(pygame.font.get_default_font(), 75)
    selected_cell = None

    for row in range(8):
        for col in range(8):
            piece = grid[col][row]
            cell = cells[col][row]
            if mouse_pos != None and cell.get_rect().collidepoint(mouse_pos):
                cell.toggle_selection()
                moves = gamestate.select_piece(row, col)
                for move in moves:
                    cells[move[0]][move[1]].toggle_selection()
                    cells[move[0]][move[1]].update()
            cell.update()
            if isinstance(piece, Pawn):
                text = letter_font.render("P", True, ((255, 0, 0)))
                cell.set_piece(piece)
                cell.get_subsurface().blit(text, (0, 0))
            elif isinstance(piece, Rook):
                text = letter_font.render("R", True, ((255, 0, 0)))
                cell.set_piece(piece)
                cell.get_subsurface().blit(text, (0, 0))
            elif isinstance(piece, Bishop):
                text = letter_font.render("B", True, ((255, 0, 0)))
                cell.set_piece(piece)
                cell.get_subsurface().blit(text, (0, 0))            
            elif isinstance(piece, Knight):
                text = letter_font.render("Kn", True, ((255, 0, 0)))
                cell.set_piece(piece)
                cell.get_subsurface().blit(text, (0, 0))
            elif isinstance(piece, Queen):
                text = letter_font.render("Q", True, ((255, 0, 0)))
                cell.set_piece(piece)
                cell.get_subsurface().blit(text, (0, 0))
            elif isinstance(piece, King):
                text = letter_font.render("Ki", True, ((255, 0, 0)))
                cell.set_piece(piece)
                cell.get_subsurface().blit(text, (0, 0))

    pygame.display.flip()

if __name__ == "__main__":
    main()

