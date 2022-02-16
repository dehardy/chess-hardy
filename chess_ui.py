import pygame, os
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
                self.cell_sub.fill((127, 127, 255))
            else:
                self.cell_sub.fill((255, 255, 255))
        else:
            if self.selected:
                self.cell_sub.fill((0, 0, 127))
            else:
                self.cell_sub.fill((0, 0, 0))

        if isinstance(self.piece, Pawn):
            self.get_subsurface().blit(pygame.transform.scale(pygame.image.load(os.path.join("sprites", "pawn_%s.png" %self.piece.get_color())), (100, 100)), (0, 0))
        elif isinstance(self.piece, Rook):
            self.get_subsurface().blit(pygame.transform.scale(pygame.image.load(os.path.join("sprites", "rook_%s.png" %self.piece.get_color())), (100, 100)), (0, 0))
        elif isinstance(self.piece, Bishop):
            self.get_subsurface().blit(pygame.transform.scale(pygame.image.load(os.path.join("sprites", "bishop_%s.png" %self.piece.get_color())), (100, 100)), (0, 0))
        elif isinstance(self.piece, Knight):
            self.get_subsurface().blit(pygame.transform.scale(pygame.image.load(os.path.join("sprites", "knight_%s.png" %self.piece.get_color())), (100, 100)), (0, 0))
        elif isinstance(self.piece, Queen):
            self.get_subsurface().blit(pygame.transform.scale(pygame.image.load(os.path.join("sprites", "queen_%s.png" %self.piece.get_color())), (100, 100)), (0, 0))
        elif isinstance(self.piece, King):
            self.get_subsurface().blit(pygame.transform.scale(pygame.image.load(os.path.join("sprites", "king_%s.png" %self.piece.get_color())), (100, 100)), (0, 0))

        
    def clear_selection(self):
        self.selected = False

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

    def get_selection(self):
        return self.selected



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
    cells_selected_group = pygame.sprite.Group()
    console = my_display.subsurface(pygame.Rect(800, 0, 400, 100))
    turn = "white"
    B = Board()


    checkmate = False

    black = False

    for row in range(8):
        for col in range(8):
            if black: sprite_cell = Cell("black", col * cell_width, row * cell_height, cell_width, cell_height)
            else: sprite_cell = Cell("white", col * cell_width, row * cell_height, cell_width, cell_height)

            black = not black
            cells_group.add(sprite_cell)
            cells_list[row][col] = sprite_cell
            sprite_cell.set_piece(B.get_grid()[row][col])
        black = not black #needed for correct colors

    cells_group.update()
    pygame.display.flip()

    pygame.event.set_allowed([pygame.MOUSEBUTTONDOWN])

    while not checkmate:
        event = pygame.event.wait()
        if update_image(console, cells_list, cells_group, cells_selected_group, B, turn, event.pos):

            turn = "black" if turn == "white" else "white"
        pygame.display.flip()

def update_image(console, cells, cells_group, cells_selected_group, gamestate, turn, mouse_pos = None):
    grid = gamestate.get_grid()
    opponent = "white" if turn == "black" else "black"
    letter_font = pygame.font.Font(pygame.font.get_default_font(), 75)
    selected_cell = None

    for row in range(8):
        for col in range(8):
            piece = grid[row][col]
            cell = cells[row][col]
            if mouse_pos != None and cell.get_rect().collidepoint(mouse_pos): #If mouse clicked on cell
                selected_piece = gamestate.get_piece_selected()

                if cell in cells_selected_group: #move piece if applicable

                    if selected_piece == (row, col): #Clicked cell with currently selected piece
                        for sprite in cells_selected_group.sprites():
                            cells_selected_group.remove(sprite)
                            sprite.toggle_selection()
                            sprite.update()

                    else: #Clicked cell which will move piece
                        cell.set_piece(gamestate.get_grid()[selected_piece[0]][selected_piece[1]]) #set current cell piece equal to piece that will be there
                        gamestate.move((row, col)) #move the piece in the backend
                        cells[selected_piece[0]][selected_piece[1]].set_piece(None) #clear the piece from the old cell
                        piece = grid[row][col]

                        for sprite in cells_selected_group.sprites():
                            cells_selected_group.remove(sprite)
                            sprite.toggle_selection()
                            sprite.update()

                        if gamestate.is_in_check(opponent):
                            if gamestate.is_checkmated(opponent):
                                console.blit(letter_font.render("CHECKMATE!!!", False, (0, 0, 0)), console.get_rect())
                            else:
                                console.blit(letter_font.render("Check!", False, (0, 0, 0)), console.get_rect())
                        else:
                            console.fill((127, 127, 127))
                        return True

                elif cell.get_piece() != None and cell.get_piece().get_color() == turn: #Clicked on a piece
                    if selected_piece != None: #Clicked new piece to select
                        for sprite in cells_selected_group.sprites(): #Deselect old
                            cells_selected_group.remove(sprite)
                            sprite.toggle_selection()
                            sprite.update()

                    cells_selected_group.add(cell)
                    cell.toggle_selection()
                    moves = gamestate.select_piece(row, col)
                    for move in moves:
                        cells_selected_group.add((cells[move[0]][move[1]]))
                        cells[move[0]][move[1]].toggle_selection()
                        cells[move[0]][move[1]].update()
            cell.update()

    return False
if __name__ == "__main__":
    main()

