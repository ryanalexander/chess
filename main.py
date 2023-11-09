import pygame

class GameBoard:
    call_for_render = True
    teams = []
    x = 8
    y = 8

    def get_piece_by_pos(self, x, y):
        for team in self.teams:
            for piece in team.piece:
                if piece.position[0] == y and piece.position[1] == x:
                    return piece

class Team:
    name = None
    color = None
    piece = []

    def __init__(self, name, color) -> None:
        self.name = name
        self.color = color

    def __str__(self) -> str:
        return self.name

class GamePiece:
    team = None
    type = None
    position = (0, 0)
    captured = False
    color = None

    def __init__(self, team, type):
        self.type = type
        self.team = team

    def get_valid_moves(self, gameBoard):
        paths = get_path_by_piece(self.type)
        valid_moves = []

        for path in paths:
            new_x = self.position[1] + path[1]
            new_y = self.position[0] + path[0]

            if 0 <= new_x < gameBoard.x and 0 <= new_y < gameBoard.y:
                target_piece = gameBoard.get_piece_by_pos(new_x, new_y)
                if target_piece is None or target_piece.team != self.team:
                    valid_moves.append((new_y, new_x))

        return valid_moves

    def get_relative_square(self, x, y):
        return (self.position[0] + y, self.position[1] + x)

    def __str__(self) -> str:
        return "Team=%s,Type=%s,Position=%s,Captured=%s,Color=%s" % (self.team,self.type,self.position,self.captured,self.color)

def get_path_by_piece(name):
    if name == "Pawn":
        return [(1, 0), (2, 0), (1, 1), (1, -1)]
    elif name == "Knight":
        return [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    elif name == "Bishop":
        return [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    elif name == "Rook":
        return [(1, 0), (0, 1), (-1, 0), (0, -1)]
    elif name == "Queen":
        return [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    elif name == "King":
        return [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    else:
        return []


def offset_by_piece(name, num):
    if name == "King":
        return (0, 0)
    if name == "Queen":
        return (0, -1)
    if name == "Bishop":
        if num == 0:
            return (0, 1)
        if num == 1:
            return (0, -2)
    if name == "Knight":
        if num == 0:
            return (0, 2)
        if num == 1:
            return (0, -3)
    if name == "Rook":
        if num == 0:
            return (0, 3)
        if num == 1:
            return (0, -4)
    if name == "Pawn":
        return (1, -4 + num)

def get_image_for_piece(piece):
    if piece is None:
        return None
    print (piece)
    return "./pieces/%s-%s.svg" % (piece.type.lower(), piece.team.name.lower()[0])

def main():
    gameBoard = GameBoard()

    selected_piece = None

    # Create teams
    whiteTeam = Team("White", (255, 255, 255))
    blackTeam = Team("Black", (0, 0, 0))

    # Add to board
    gameBoard.teams.append(whiteTeam)
    gameBoard.teams.append(blackTeam)
    
    # Create all pieces
    pieceDictionary = {"Queen": 1, "King": 1, "Bishop": 2, "Rook": 2, "Knight": 2, "Pawn": 8}

    # Add pieces to teams
    for team in gameBoard.teams:
        for pieceType in pieceDictionary:
            for i in range(pieceDictionary[pieceType]):
                piece = GamePiece(team, pieceType)
                pos = offset_by_piece(pieceType, i)
                if (team.name == "White"): # Offset to bottom of board
                    pos = (7 - pos[0], pos[1])

                pos = (pos[0], 4 + pos[1])
                piece.position = pos
                team.piece.append(piece)


    # Print all teams and their pieces
    for team in gameBoard.teams:
        for piece in team.piece:
            print("%s | %s | %s" % (team.name, piece.type, piece.position))

    pygame.init()
    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Hello, World!")

    def identify_piece_by_pos(pos):
        square_width = window.get_width() / gameBoard.x
        square_height = window.get_height() / gameBoard.y
        x = int(pos[0] // square_width)
        y = int(pos[1] // square_height)

        piece = gameBoard.get_piece_by_pos(x, y)
        return piece

    def handle_click(pos):
        selected_piece = identify_piece_by_pos(pos)
        if selected_piece != None:
            print("TODO: Movement")
            pass
        pass
    
    def render_board():
        gameBoard.call_for_render = False
        square_height = window.get_height() / gameBoard.y
        square_width = window.get_width() / gameBoard.x

        for x in range(gameBoard.x):
            for y in range(gameBoard.y):
                even = (x + y) % 2 == 0 
                color = (238,238,210) if even else (118,150,86)  # Use RGB tuples for colors
                x_position = x * square_width
                y_position = y * square_height
                pygame.draw.rect(window, color, (x_position, y_position, square_width, square_height))

                piece = gameBoard.get_piece_by_pos(x, y)
                if piece is not None:
                    surface = pygame.image.load(get_image_for_piece(piece))
                    window.blit(surface, (x * square_width, y * square_height))

        pygame.display.update()  # Update the display

    # Replace the input call with an event loop
    running = True
    while running:
        if gameBoard.call_for_render:
            render_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(pygame.mouse.get_pos())

    pygame.quit()

if __name__ == "__main__":
    main()