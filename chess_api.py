#Chess API
import pygame

class Board():

    def __init__(self):

        #Initialize 8*8 Matrix
        self.grid = [[None] * 8 for i in range(8)]

        self.piece_selected = None

        #Put Pawns on Board
        for i in range(8):
            self.grid[1][i] = Pawn(1, i, "black")
            self.grid[6][i] = Pawn(6, i, "white")

        #Put other pieces
        #white pieces
        self.grid[7][0] = Rook(7, 0, "white")
        self.grid[7][1] = Knight(7, 1, "white")
        self.grid[7][2] = Bishop(7, 2, "white")
        self.grid[7][3] = Queen(4, 3, "white")
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

    def select_piece(self, row, col):
        P = self.grid[row][col]
        piece_moves = P.get_moves()
        valid_moves = []


        if isinstance(P, Knight):
            for move in piece_moves:
                if not self.is_obstructed_knight():
                    valid_moves.append(move)

        elif isinstance(P, Pawn):
            for move in piece_moves:
                if not self.is_obstructed_pawn(row, col, move, P.get_color()):
                    valid_moves.append(move)

        else:
            for move in piece_moves:
                if not self.is_obstructed(row, col, move, P.get_color()):
                    valid_moves.append(move)

        self.piece_selected = (row, col)
        return valid_moves

    #Detemine is a piece (other than knight or pawn) at position (row, col) can move to the cell designated by "move" 
    def is_obstructed(self, row, col, move, color):
        if move[0] > 7 or move[1] > 7: return True #Move off board

        dest = self.grid[move[0]][move[1]]
        moveRow = move[0]
        moveCol = move[1]

        #If move cell contains a friendly piece, exit
        if dest != None and dest.get_color == color:
            return True

        if row == moveRow: #Same row
            if moveCol > col: 
                x1 = col + 1
                x2 = moveCol + 1
            else:
                x1 = moveCol
                x2 = col
            for curr_col in range(x1, x2):
                curr = self.grid[curr_col][row]
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
                curr = self.grid[col][curr_row]
                if curr == None: pass #Empty space
                elif curr.get_color() == color: #Occupied by friendly piece
                    return True
                elif curr_row != moveRow: #Cell contains enemy piece, but on path rather than at destination
                    return True
            return False

        else: #Diagonal move
            if (moveRow < row and moveCol < col) or (moveRow > row and moveCol > col):
                pass
    
    def is_obstructed_pawn(self, row, col, move, color):
        if move[0] > 7 or move[1] > 7: return True #Move off board

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
        
    def move(self, move):
        piece = self.grid[self.piece_selected[0]][self.piece_selected[1]]
        piece.move(move[0], move[1])
        self.grid[move[0]][move[1]] = piece
        self.grid[self.piece_selected[0]][self.piece_selected[1]] = None
        self.piece_selectd = None

    def get_grid(self):
        return self.grid

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
            if 0 >= bX + o and bX + o < 8 and 0 >= bY + o and bY + o < 8:
                moves.append((bY + o, bX + o))
        return moves

class Knight(Piece):
    
    def get_moves(self):
        pass

class Queen(Piece):

    def get_moves(self):
        moves = []
        qX = self.location[1]
        qY = self.location[0]
        for o in range (-7, 8):
            if 0 >= qX + o and qX + o < 8 and 0 >= qY + o and qY + o < 8:
                moves.append((qY + o, qX + o))

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
    pass


