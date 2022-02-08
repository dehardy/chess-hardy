#Chess API


class Board():

    def __init__(self):

        #Initialize 8*8 Matrix
        self.grid = [[None] * 8 for i in range(8)]

        #Put Pawns on Board
        for i in range(8):
            self.grid[i][1] = Pawn(1, i, "White")
            self.grid[i][6] = Pawn(6, i, "Black")

        #Put other pieces
        #White pieces
        self.grid[0][0] = Rook(0, 0, "White")
        self.grid[1][0] = Knight(0, 1, "White")
        self.grid[2][0] = Bishop(0, 2, "White")
        self.grid[3][0] = Queen(0, 3, "White")
        self.grid[4][0] = King(0, 4, "White")
        self.grid[5][0] = Bishop(0, 5, "White")
        self.grid[6][0] = Knight(0, 6, "White")
        self.grid[7][0] = Rook(0, 7, "White")

        #Black pieces
        self.grid[0][7] = Rook(7, 0, "Black")
        self.grid[1][7] = Knight(7, 1, "Black")
        self.grid[2][7] = Bishop(7, 2, "Black")
        self.grid[3][7] = Queen(7, 3, "Black")
        self.grid[4][7] = King(7, 4, "Black")
        self.grid[5][7] = Bishop(7, 5, "Black")    
        self.grid[6][7] = Knight(7, 6, "Black") 
        self.grid[7][7] = Rook(7, 7, "Black")

    def select_piece(self, row, col):
        P = self.grid[col][row]
        piece_moves = P.get_moves()
        valid_moves = []

        if not isinstance(P, Knight):
            for move in piece_moves:
                if not is_obstructed(row, col, move, P.get_color()):
                    valid_moves.append(move)
        else:
            for move in piece_moves:
                if not is_obstructed_knight:
                    valid_moves.append(move)

    #Detemine is a piece (other than knight) at position (row, col) can move to the cell designated by "move" 
    def is_obstructed(self, row, col, move, color):
        dest = self.grid[move[0]][move[1]]
        moveRow = move[1]
        moveCol = move[0]

        #If move cell contains a friendly piece, exit
        if dest != None and dest.get_color == color:
            return True

        if row == moveRow: #Same row
            if moveCol > col: 
                y1 = col + 1
                y2 = moveCol + 1
            else:
                y1 = moveCol
                y2 = col
            for y in range(y1, y2):
                curr = self.grid[y][row]
                if curr == None: pass #Empty Space
                elif curr.get_color == color: #Occupied by friendly piece
                    return True
                elif y != moveCol: #Cell contains enemy piece, but on path rather than at destination
                    return True
            return False

        elif col == moveCol: #Same column
            if moveRow > row:
                x1 = row + 1
                x2 = moveRow + 1
            else:
                x1 = moveRow
                x2 = row
            for x in range(x1, x2):
                curr = self.grid[col][x]
                if curr == None: pass #Empty space
                elif curr.get_color == color: #Occupied by friendly piece
                    return True
                elif x != moveRow: #Cell contains enemy piece, but on path rather than at destination
                    return True
            return False

        else: #Diagonal move
            if (moveRow < row and moveCol < col) or (moveRow > row and moveCol > col):
                pass
    
    def get_grid(self):
        return self.grid
        
#Parent for all pieces
class Piece():
    def __init__(self, row, col, color):
        self.color = color
        self.location = (row, col)

    def get_location(self):
        return self.location
    
    def get_color(self):
        return self.color

    def get_piece(self):
        return self.__class__

    def move(self, row, col):
        self.location = (col, row)


class Rook(Piece):

    def get_moves(self):
        moves = []
        rX = self.location[1]
        rY = self.location[0]
        for i in range(8):
            if i != rX:
                moves.append((rY, i))
            if i != rY:
                moves.append((i, rX))
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
    pass
class Queen(Piece):

    def get_moves(self):
        moves = []
        qX = self.location[1]
        qY = self.location[0]
        for o in range (-7, 8):
            if 0 >= qX + o and qX + o < 8 and 0 >= qY + o and qY + o < 8:
                moves.append(qY + o, qX + o)

        for i in range(8):
            if i != qX:
                moves.append(qY, i)
            if i != qY:
                moves.append(i, qX)
            
class Pawn(Piece):
    pass

class King(Piece):
    pass


