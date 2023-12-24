class Game():
    def __init__(self):
        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                      ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.whiteMove = True
        self.log = []
        
        self.inCheck = False

    def move(self, move):
        self.board[move.currX][move.currY] = "--"
        self.board[move.nextX][move.nextY] = move.startPiece

        self.log.append(move.chessNotation(self.board))
        self.whiteMove = not self.whiteMove

    def validMoves(self, r, c):
        moves = []
        player = self.board[r][c][0]
        piece = self.board[r][c][1]
        print(self.inCheck)

        if self.whiteMove and player == 'w':
            if piece == 'P':
                self.pawnMoves(r, c, moves)
            elif piece == 'R':
                self.rookMoves(r, c, moves)
            elif piece == 'N':
                self.knightMoves(r, c, moves)
            elif piece == 'B':
                self.bishopMoves(r, c, moves)
            elif piece == 'Q':
                self.queenMoves(r, c, moves)
            elif piece == 'K':
                self.kingMoves(r, c, moves)

        elif not self.whiteMove and player == 'b':
            if piece == 'P':
                self.pawnMoves(r, c, moves)
            elif piece == 'R':
                self.rookMoves(r, c, moves)
            elif piece == 'N':
                self.knightMoves(r, c, moves)
            elif piece == 'B':
                self.bishopMoves(r, c, moves)
            elif piece == 'Q':
                self.queenMoves(r, c, moves)
            elif piece == 'K':
                self.kingMoves(r, c, moves)

        return moves
    
    def Check(self):
        moves = []
        kingPos = (0, 4)

        if self.whiteMove:
            check = 'b'
            king = 'w'
        else:
            check = 'w'
            king = 'b'

        for row in range(8):
            for col in range(8):
                if check == self.board[row][col][0]:
                    piece = self.board[row][col][1]
                    if piece == 'P':
                        self.pawnMoves(row, col, moves)
                    elif piece == 'R':
                        self.rookMoves(row, col, moves)
                    elif piece == 'N':
                        self.knightMoves(row, col, moves)
                    elif piece == 'B':
                        self.bishopMoves(row, col, moves)
                    elif piece == 'Q':
                        self.queenMoves(row, col, moves)
                    elif piece == 'K':
                        self.kingMoves(row, col, moves)

                if self.board[row][col] == king + 'K':
                    kingPos = (row, col)

        if kingPos in moves:
            self.inCheck = True
            self.log[-1] += '+'

        return moves

    def pawnMoves(self, r, c, moves):
        player = self.board[r][c][0]

        side = -1
        startingPos = 6
        enemy = 'b'
        if player == 'w':
            side = -1
            startingPos = 6
            enemy = 'b'
        elif player == 'b':
            side = 1
            startingPos = 1
            enemy = 'w'

        if self.board[r + (1*side)][c] == '--':
            moves.append((r + (1*side),c))
            if r == startingPos and self.board[r + (2*side)][c] == '--':
                moves.append((r + (2*side),c))

        if c-1 > -1:
            if self.board[r + (1*side)][c-1] != '--' and self.board[r + (1*side)][c-1][0] == enemy:
                moves.append((r + (1*side),c-1))
        if c+1 < 8:
            if self.board[r + (1*side)][c+1] != '--' and self.board[r + (1*side)][c+1][0] == enemy:
                moves.append((r + (1*side),c+1))

    def rookMoves(self, r, c, moves):
        vertical = []
        horizontal = []
        player = self.board[r][c][0]

        enemy = 'b'
        if player == 'w':
            enemy = 'b'
        elif player == 'b':
            enemy = 'w'

        for row in range(8):
            if row != r:
                vertical.append((row, c))
            if row < r:
                if self.board[row][c] != '--':
                    vertical.clear()
                    if self.board[row][c][0] == enemy:
                        vertical.append((row, c))
            elif row > r:
                if self.board[row][c] != '--':
                    if self.board[row][c][0] != enemy:
                        vertical.remove((row, c))
                    break
                        
        for col in range(8):
            if col != c:
                horizontal.append((r, col))
            if col < c:
                if self.board[r][col] != '--':
                    horizontal.clear()
                    if self.board[r][col][0] == enemy:
                        horizontal.append((r, col))
            elif col > c:
                if self.board[r][col] != '--':
                    if self.board[r][col][0] != enemy:
                        horizontal.remove((r, col))
                    break
        
        for i in vertical + horizontal:
            moves.append(i)

    def knightMoves(self, r, c, moves):
        player = self.board[r][c][0]

        enemy = 'b'
        if player == 'w':
            enemy = 'b'
        elif player == 'b':
            enemy = 'w'

        if c-2 > -1:
            if r+1 < 8:
                if self.board[r+1][c-2] == '--' or self.board[r+1][c-2][0] == enemy:
                    moves.append((r+1, c-2))
            if r-1 > -1:
                if self.board[r-1][c-2] == '--' or self.board[r-1][c-2][0] == enemy:
                    moves.append((r-1, c-2))

        if c+2 < 8:
            if r+1 < 8:
                if self.board[r+1][c+2] == '--' or self.board[r+1][c+2][0] == enemy:
                    moves.append((r+1, c+2))
            if r-1 > -1:
                if self.board[r-1][c+2] == '--' or self.board[r-1][c+2][0] == enemy:
                    moves.append((r-1, c+2))
        
        if r-2 > -1:
            if c+1 < 8:
                if self.board[r-2][c+1] == '--' or self.board[r-2][c+1][0] == enemy:
                    moves.append((r-2, c+1))
            if c-1 > -1:
                if self.board[r-2][c-1] == '--' or self.board[r-2][c-1][0] == enemy:
                    moves.append((r-2, c-1))
        
        if r+2 < 8:
            if c+1 < 8:
                if self.board[r+2][c+1] == '--' or self.board[r+2][c+1][0] == enemy:
                    moves.append((r+2, c+1))
            if c-1 > -1:
                if self.board[r+2][c-1] == '--' or self.board[r+2][c-1][0] == enemy:
                    moves.append((r+2, c-1))
        
    def bishopMoves(self, r, c, moves):
        diagonal1 = []
        diagonal2 = []
        diagonal3 = []
        diagonal4 = []
        player = self.board[r][c][0]

        enemy = 'b'
        if player == 'w':
            enemy = 'b'
        elif player == 'b':
            enemy = 'w'

        for i in range(7, -1, -1):
            if r-i > -1 and c-i > -1 and r-i != r and c-i != c:
                diagonal1.append((r-i, c-i))
                if self.board[r-i][c-i] != '--':
                    if self.board[r-i][c-i][0] == enemy:
                        diagonal1.clear()
                        diagonal1.append((r-i, c-i))
                    else:
                        diagonal1.clear()

            if r-i > -1 and c+i < 8 and r-i != r and c+i != c:
                diagonal2.append((r-i, c+i))
                if self.board[r-i][c+i] != '--':
                    if self.board[r-i][c+i][0] == enemy:
                        diagonal2.clear()
                        diagonal2.append((r-i, c+i))
                    else:
                        diagonal2.clear()

            if r+i < 8 and c+i < 8 and r+i != r and c+i != c:
                diagonal3.append((r+i, c+i))
                if self.board[r+i][c+i] != '--':
                    if self.board[r+i][c+i][0] == enemy:
                        diagonal3.clear()
                        diagonal3.append((r+i, c+i))
                    else:
                        diagonal3.clear()

            if r+i < 8 and c-i > -1 and r+i != r and c-i != c:
                diagonal4.append((r+i, c-i))
                if self.board[r+i][c-i] != '--':
                    if self.board[r+i][c-i][0] == enemy:
                        diagonal4.clear()
                        diagonal4.append((r+i, c-i))
                    else:
                        diagonal4.clear()

        for i in diagonal1 + diagonal2 + diagonal3 + diagonal4:
            moves.append(i)

    def queenMoves(self, r, c, moves):
        diagonal1 = []
        diagonal2 = []
        diagonal3 = []
        diagonal4 = []
        vertical = []
        horizontal = []

        player = self.board[r][c][0]

        enemy = 'b'
        if player == 'w':
            enemy = 'b'
        elif player == 'b':
            enemy = 'w'

        for i in range(7, -1, -1):
            if r-i > -1 and c-i > -1 and r-i != r and c-i != c:
                diagonal1.append((r-i, c-i))
                if self.board[r-i][c-i] != '--':
                    if self.board[r-i][c-i][0] == enemy:
                        diagonal1.clear()
                        diagonal1.append((r-i, c-i))
                    else:
                        diagonal1.clear()

            if r-i > -1 and c+i < 8 and r-i != r and c+i != c:
                diagonal2.append((r-i, c+i))
                if self.board[r-i][c+i] != '--':
                    if self.board[r-i][c+i][0] == enemy:
                        diagonal2.clear()
                        diagonal2.append((r-i, c+i))
                    else:
                        diagonal2.clear()

            if r+i < 8 and c+i < 8 and r+i != r and c+i != c:
                diagonal3.append((r+i, c+i))
                if self.board[r+i][c+i] != '--':
                    if self.board[r+i][c+i][0] == enemy:
                        diagonal3.clear()
                        diagonal3.append((r+i, c+i))
                    else:
                        diagonal3.clear()

            if r+i < 8 and c-i > -1 and r+i != r and c-i != c:
                diagonal4.append((r+i, c-i))
                if self.board[r+i][c-i] != '--':
                    if self.board[r+i][c-i][0] == enemy:
                        diagonal4.clear()
                        diagonal4.append((r+i, c-i))
                    else:
                        diagonal4.clear()

        for i in diagonal1 + diagonal2 + diagonal3 + diagonal4:
            moves.append(i)

        for row in range(8):
            if row != r:
                vertical.append((row, c))
            if row < r:
                if self.board[row][c] != '--':
                    vertical.clear()
                    if self.board[row][c][0] == enemy:
                        vertical.append((row, c))
            elif row > r:
                if self.board[row][c] != '--':
                    if self.board[row][c][0] != enemy:
                        vertical.remove((row, c))
                    break
                        
        for col in range(8):
            if col != c:
                horizontal.append((r, col))
            if col < c:
                if self.board[r][col] != '--':
                    horizontal.clear()
                    if self.board[r][col][0] == enemy:
                        horizontal.append((r, col))
            elif col > c:
                if self.board[r][col] != '--':
                    if self.board[r][col][0] != enemy:
                        horizontal.remove((r, col))
                    break
        
        for i in vertical + horizontal:
            moves.append(i)

    def kingMoves(self, r, c, moves):
        player = self.board[r][c][0]

        enemy = 'b'
        if player == 'w':
            enemy = 'b'
        elif player == 'b':
            enemy = 'w'

        if r + 1 < 8:
            if c-1 > -1:
                if self.board[r+1][c-1] == '--' or self.board[r+1][c-1][0] == enemy:
                    moves.append((r+1, c-1))
            if c+1 < 8:
                if self.board[r+1][c+1] == '--' or self.board[r+1][c+1][0] == enemy:
                    moves.append((r+1, c+1))
            if self.board[r+1][c] == '--' or self.board[r+1][c][0] == enemy:
                moves.append((r+1, c))

        if c-1 > -1:
            if self.board[r][c-1] == '--' or self.board[r][c-1][0] == enemy:
                moves.append((r, c-1))
        if c+1 < 8:
            if self.board[r][c+1] == '--' or self.board[r][c+1][0] == enemy:
                moves.append((r, c+1))
        
        if r - 1 > -1:
            if c-1 > -1:
                if self.board[r-1][c-1] == '--' or self.board[r-1][c-1][0] == enemy:
                    moves.append((r-1, c-1))
            if c+1 < 8:
                if self.board[r-1][c+1] == '--' or self.board[r-1][c+1][0] == enemy:
                    moves.append((r, c+1))
            if self.board[r-1][c] == '--' or self.board[r-1][c][0] == enemy:
                moves.append((r-1, c))


class Move():
    def __init__(self, current, next, board):
        self.currX = current[0]
        self.currY = current[1]
        self.nextX = next[0]
        self.nextY = next[1]

        self.startPiece = board[self.currX][self.currY]
        self.endPiece = board[self.nextX][self.nextY]

    def chessNotation(self, board):
        colToFiles = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        rowToRanks = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}

        if board[self.nextX][self.nextY][1] == 'P':
            return colToFiles[self.nextY] + rowToRanks[self.nextX]
        else:
            return board[self.nextX][self.nextY][1] + colToFiles[self.nextY] + rowToRanks[self.nextX]