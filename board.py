def clear_board():
    """Initialisiert ein leeres Spielbrett."""
    return [" " for _ in range(9)]

def draw_board(board):
    """Zeichnet die aktuelle Spielposition."""
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")

def check_if_valid(board, zug):
    """Überprüft, ob ein Zug möglich ist."""
    if 0 <= zug <= 8:
        return board[zug] == " "
    return False

def check_win_condition(board):
    """Prüft, ob ein Spieler gewonnen hat oder das Spiel unentschieden endet."""
    # Gewinnkombinationen (Reihen, Spalten, Diagonalen)
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # Reihen
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # Spalten
        (0, 4, 8), (2, 4, 6)             # Diagonalen
    ]

    for a, b, c in win_combinations:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a] # Gibt den Gewinner ('X' oder 'O') zurück
    
    if " " not in board:
        return "Tie" # Unentschieden
    
    return None # Spiel läuft noch