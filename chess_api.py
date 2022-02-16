#Chess API
import pygame, copy

class Board():

    def __init__(self):

        #Initialize 8*8 Matrix
        self.grid = [[None] * 8 for i in range(8)]

        self.piece_selected = None
        self.check = False

        #Put Pawns on Board
        for i in range(8):
            self.grid[1][i] = Pawn(1, i, "black")
            self.grid[6][i] = Pawn(6, i, "white")

        #Put other pieces
        #white pieces
        self.grid[7][0] = Rook(7, 0, "white")
        self.grid[7][1] = Knight(7, 1, "white")
        self.grid[7][2] = Bishop(7, 2, "white")
        self.grid[7][3] = Queen(7, 3, "white")
        self.grid[7][4] = King(7, 4, "white")
        self.grid[7][5] = Bishop(7, 5, "white")
        self.grid[7][6] = Knight(7, 6, "white")
        self.grid[7][7] = Rook(7, 7, "white")

        #black pieces
        self.grid[0][0] = Rook(0, 0, "black")
        self.grid[0][1] = Knight(0, 1, "black")
        self.grid[0][2] = Bishop(0, 2, "black")
        self.grid[0][3] = Queen(0, 3, "black")
        self.grid[0][4] = King(0, 4, "black")
        self.grid[0][5] = Bishop(0, 5, "black")    
        self.grid[0][6] = Knight(0, 6, "black") 
        self.grid[0][7] = Rook(0, 7, "black")

        #Identify Kings
        self.white_king = self.grid[7][4]
        self.black_king = self.grid[0][4]

    #When a player selects a piece to preview moves. Calculates moves and the validity of them
    def select_piece(self, row, col):
        P = self.grid[row][col]
        piece_moves = P.get_moves()
        valid_moves = []

        #Knights have unique movement, so they are handled separately
        if isinstance(P, Knight):
            for move in piece_moves:
                if not self.is_obstructed_knight(row, col, move, P.get_color()):
                    valid_moves.append(move)

        #Pawns also move uniquely since they capture and move normally in different ways
        elif isinstance(P, Pawn):
            for move in piece_moves:
                if not self.is_obstructed_pawn(row, col, move, P.get_color()):
                    valid_moves.append(move)

        #Every other piece behaves similarly
        else:
            for move in piece_moves:
                if not self.is_obstructed(row, col, move, P.get_color()):
                    valid_moves.append(move)


        self.piece_selected = (row, col)
        return valid_moves

    def deselect_piece(self):
        self.piece_selected = None

    #Detemine if a piece (other than knight or pawn) at position (row, col) can move to the cell designated by "move" 
    def is_obstructed(self, row, col, move, color):
        if move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0: return True #Move off board

        dest = self.grid[move[0]][move[1]]
        moveRow = move[0]
        moveCol = move[1]

        #If move cell contains a friendly piece, exit
        if dest != None and dest.get_color == color:
            return True

        if row == moveRow: #Same row
            if moveCol > col: #starting at col and iterating to moveCol; do not check col
                x1 = col + 1
                x2 = moveCol + 1
            else:
                x1 = moveCol
                x2 = col
            for curr_col in range(x1, x2):
                curr = self.grid[row][curr_col]
                if curr == None: pass #Empty Space
                elif curr.get_color() == color: #Occupied by friendly piece
                    return True
                elif curr_col != moveCol: #Cell contains enemy piece, but on path rather than at destination
                    return True
            return False

        elif col == moveCol: #Same column
            if moveRow > row:
                y1 = row + 1
                y2 = moveRow + 1
            else:
                y1 = moveRow
                y2 = row
            for curr_row in range(y1, y2):
                curr = self.grid[curr_row][col]
                if curr == None: pass #Empty space
                elif curr.get_color() == color: #Occupied by friendly piece
                    return True
                elif curr_row != moveRow: #Cell contains enemy piece, but on path rather than at destination
                    return True
            return False

        else: #Diagonal move
            row_offset = 1 if moveRow > row else -1 #Direction to move vertically
            col_offset = 1 if moveCol > col else -1 #Direction to move horizontally
            begin_row = row + row_offset
            begin_col = col + col_offset

            while (begin_row, begin_col) != (moveRow, moveCol):
                curr = self.grid[begin_row][begin_col]
                if curr != None: return True
                begin_row += row_offset
                begin_col += col_offset

            curr = self.grid[moveRow][moveCol]
            #curr being empty or holding an enemy piece will result in a false
            return (curr != None and curr.get_color() == color) 
    

    def is_obstructed_pawn(self, row, col, move, color):
        if move[0] > 7 or move[1] > 7 or move[0] < 0 or move[1] < 0: return True #Move off board

        dest = self.grid[move[0]][move[1]]
        direction = -1 if color == "white" else 1
        if dest != None and dest.get_color() == color:
            return True

        elif move[1] == col: #forward move
            if row + direction == move[0]: #One space
                return dest != None
            else: #Two spaces
                return dest != None or self.grid[row + direction][move[1]] != None

        elif dest == None: #Sideways move, no piece present
            return True
        
        elif dest.get_color() != color: #Sideways move, enemy piece
            return False

        else:
            return True

    #Check if a knight may move to a position        
    def is_obstructed_knight(self, row, col, move, color):
        if move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7: return True
        if self.grid[move[0]][move[1]] == None: return False
        if self.grid[move[0]][move[1]].get_color() == color: return True
        return False
        
    #Moves the currently selected piece. This will place the selected piece into the space designated by move
    #The old piece if it exists (which should be an enemy piece) is overrided and deleted (or captured)
    def move(self, move):
        piece = self.grid[self.piece_selected[0]][self.piece_selected[1]]
        piece.move(move[0], move[1])
        self.grid[move[0]][move[1]] = piece
        self.grid[self.piece_selected[0]][self.piece_selected[1]] = None
        self.piece_selected = None
        if isinstance(piece, King):
            if piece.get_color() == "white":
                self.white_king = piece
            else:
                self.black_king = piece

    #Checks if color is in check. If true, then checks for checkmate
    def is_in_check(self, color):
        king = self.white_king if color == "white" else self.black_king
        (king_row, king_col) = king.get_location()
        print(king.get_location())
        for row in range (8):
            for col in range(8):
                if self.grid[row][col] != None and self.grid[row][col].get_color() != color:
                    piece = self.grid[row][col]
                    moves = piece.get_moves()
                    if (king_row, king_col) in moves:
                        if isinstance(piece, Pawn):
                            self.check = not self.is_obstructed_pawn(row, col, (king_row, king_col), piece.get_color())
                            if self.check: return self.check
                        elif isinstance(piece, Knight):
                            self.check = not self.is_obstructed_knight(row, col, (king_row, king_col), piece.get_golor())
                            if self.check: return self.check
                        else:
                            self.check = not self.is_obstructed(row, col, (king_row, king_col), piece.get_color())
                            if self.check: return self.check

        return self.check

    def is_checkmated(self, color):
        king = self.white_king if color == "white" else self.black_king
        (king_row, king_col) = king.get_location()
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece != None and piece.get_color() == color:
                    moves = self.select_piece(row, col)
                    for move in moves: #Check if possible to get out of check with current piece
                        curr_state = copy.deepcopy(self.grid)
                        self.move(move)
                        if not self.is_in_check(color): #Found a move that gets out of check
                            self.grid = curr_state #Restore original grid
                            print("not checkmated thanks to")
                            print(piece, move)
                            if isinstance(piece, King):
                                print("restoring king")
                                if color == "white":
                                    self.white_king = self.grid[king_row][king_col]
                                else:
                                    self.black_king = self.grid[king_row][king_col]                          
                            self.check = True
                            return False
                        else:
                            self.grid = curr_state
                            if isinstance(piece, King):
                                print("restoring king")
                                if color == "white":
                                    self.white_king = self.grid[king_row][king_col]
                                else:
                                    self.black_king = self.grid[king_row][king_col]

                            self.piece_selected = (row, col)
        self.checkmated = True
        return True
                        
    #Returns the grid holding the piece locations
    def get_grid(self):
        return self.grid

    #Returns the location of the current piece that is selected to be moved
    def get_piece_selected(self):
        return self.piece_selected

#Parent for all pieces
class Piece():
    def __init__(self, row, col, color):
        self.color = color
        self.location = (row, col)
        self.moved = False

    def get_location(self):
        return self.location
    
    def get_color(self):
        return self.color

    def get_piece(self):
        return self.__class__

    def move(self, row, col):
        self.location = (row, col)
        self.moved = True


class Rook(Piece):

    def get_moves(self):
        moves = []
        col = self.location[1]
        row = self.location[0]
        for i in range(8):
            if i != col:
                moves.append((i, row))
            if i != row:
                moves.append((col, i))
        return moves

        
class Bishop(Piece):

    def get_moves(self):
        moves = []
        bX = self.location[1]
        bY = self.location[0]
        for o in range(-7, 8):
            if o == 0: pass
            if 0 <= bX + o and bX + o < 8 and 0 <= bY + o and bY + o < 8:
                moves.append((bY + o, bX + o))
            if 0 <= bX + o and bX + o < 8 and 0 <= bY - o and bY - o < 8:
                moves.append((bY - o, bX + o))
        return moves

class Knight(Piece):
    
    def get_moves(self):
        moves = []
        kX = self.location[1]
        kY = self.location[0]

        for i in [-1, 1]:
            moves.append((kY + 2, kX + i))
            moves.append((kY - 2, kX + i))
            moves.append((kY + i, kX + 2))
            moves.append((kY + i, kX - 2))
        
        return moves

class Queen(Piece):

    def get_moves(self):
        moves = []
        qX = self.location[1]
        qY = self.location[0]
        for o in range (-7, 8):
            if o != 0 and 0 <= qX + o and qX + o < 8 and 0 <= qY + o and qY + o < 8:
                moves.append((qY + o, qX + o))
            if o != 0 and 0 <= qX + o and qX + o < 8 and 0 <= qY - o and qY - o < 8:
                moves.append((qY - o, qX + o))

        for i in range(8):
            if i != qX:
                moves.append((qY, i))
            if i != qY:
                moves.append((i, qX))
        
        return moves

class Pawn(Piece):
    def get_moves(self):
        moves = []
        qX = self.location[1]
        qY = self.location[0]

        if self.color == "white":
            moves.append((qY - 1, qX))
            moves.append((qY - 1, qX + 1))
            moves.append((qY - 1, qX - 1))
            if not self.moved:
                moves.append((qY - 2, qX))
        else:
            moves.append((qY + 1, qX))
            moves.append((qY + 1, qX + 1))
            moves.append((qY + 1, qX - 1))
            if not self.moved:
                moves.append((qY + 2, qX))
        
        return moves

class King(Piece):
    def get_moves(self):
        moves = []
        kX = self.location[1]
        kY = self.location[0]

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x != 0 or y != 0: #if the position change isn't 0,0
                    moves.append((kY + y, kX + x))
        return moves


