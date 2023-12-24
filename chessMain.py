import pygame, sys
from pygame import mixer
import chessEngine as ce

woodBoard = pygame.image.load("boardWood.jpg")
blueBoard = pygame.image.load("boardblue.png")
boardType = blueBoard

logBg = pygame.image.load("log_bg.jpg")

pygame.font.init()
whitePieces = pygame.font.Font("whitePieces.ttf", 20)
blackPieces = pygame.font.Font("blackPieces.ttf", 20)
text = pygame.font.Font("text.ttf", 20)
def draw_text(text, win, font, text_col, x, y):
	img = font.render(text, True, text_col)
	win.blit(img, (x, y))

def draw_circle(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

pieceImgs = {}
def loadPieces():
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']
    for piece in pieces:
        pieceImgs[piece] = pygame.image.load(piece + ".png")


def drawPieces(win, board):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            
            if piece != '--':
                win.blit(pieceImgs[piece], (105*c, 105*r))

def main():
    pygame.init()
    mixer.init()    
    win = pygame.display.set_mode((1200, 840))
    gs = ce.Game()
    place_sound = pygame.mixer.Sound("placePiece.mp3")
    capture_sound = pygame.mixer.Sound("capturePiece.mp3")
   
    oppMoves = []
    validMoves = []
    tileClicked = ()
    playerClicks = []
    captured = False

    while True:
        loadPieces()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                col = mx // 105
                row = my // 105

                tileClicked = (row, col)
                playerClicks.append(tileClicked)
                captured = False

                if len(playerClicks) == 1:
                    validMoves = gs.validMoves(row, col)

                if len(playerClicks) == 2:
                    if gs.board[playerClicks[1][0]][playerClicks[1][1]] != '--':
                        captured = True
                    move = ce.Move(playerClicks[0], playerClicks[1], gs.board)
                    
                    if playerClicks[1] in validMoves:
                        oppMoves = []
                        gs.move(move)
                        validMoves = []
                        oppMoves = gs.Check()

                        if captured:
                            pygame.mixer.Sound.play(capture_sound)
                        else:
                            pygame.mixer.Sound.play(place_sound)
                    else:
                        tileClicked = ()
                        playerClicks = []
                        validMoves = []

                    tileClicked = ()
                    playerClicks = []
                    validMoves = []

        win.blit(logBg, (700,0))

        win.blit(boardType, (0,0))

        if len(playerClicks) > 0:
            pygame.draw.rect(win, (240,230,140), pygame.Rect(playerClicks[0][1]*105,playerClicks[0][0]*105, 105, 105))
            pygame.draw.rect(win, (189,183,107), pygame.Rect(playerClicks[0][1]*105,playerClicks[0][0]*105, 105, 105), 5)

        drawPieces(win, gs.board)

        for i in validMoves:
            draw_circle(win, pygame.Color(100,100,100, 128), (i[1]*105+52.5,i[0]*105+52.5), 15)

        if gs.whiteMove:
            player = "White's Move"
        else:
            player = "Black's Move"

        draw_text(player, win, text, (255,255,255), 900, 20)

        for i in range(1, len(gs.log)+1):
            if i % 2 == 0:
                x = 1050
                y = i*15 + 50
                font = whitePieces
            else:
                x = 925
                y = (i+1)*15 + 50
                font = blackPieces

                if i > 1:
                    move = i-1
                else:
                    move = i
                draw_text(str(move) + '.', win, text, (175,175,175), 875, y)

            if len(gs.log[i-1]) > 2:
                draw_text(gs.log[i-1][0], win, font, (230,230,230), x, y+2)
                draw_text(gs.log[i-1][1:], win, text, (230,230,230), x+20, y)
            else:
                draw_text(gs.log[i-1], win, text, (230,230,230), x, y)

        pygame.display.update()

main()