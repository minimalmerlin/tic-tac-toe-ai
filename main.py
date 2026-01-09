import board
import KI

def main():
    game_board = board.clear_board()
    player_symbol = "X"
    ai_symbol = "O"
    current_turn = "Player" # Der Spieler beginnt

    print("Willkommen zu Tic-Tac-Toe!")
    KI.load_ai() # KI-Gedächtnis laden
    
    print("1. Spielen")
    print("2. KI Trainieren (100.000 Spiele)")
    if input("Auswahl: ") == "2":
        KI.train_self_play(100000)
        return

    board.draw_board(game_board)

    while True:
        if current_turn == "Player":
            try:
                zug_input = input("Dein Zug (1-9): ")
                zug = int(zug_input) - 1 # Umrechnung auf 0-basierten Index
                
                if board.check_if_valid(game_board, zug):
                    game_board[zug] = player_symbol
                    current_turn = "KI"
                else:
                    print("Ungültiger Zug. Feld belegt oder außerhalb des Bereichs.")
                    continue
            except ValueError:
                print("Bitte eine Zahl eingeben.")
                continue
        else:
            print("KI zieht...")
            # Die KI lernt aus dem Zustand NACH dem Spielerzug (dass sie noch lebt/nicht verloren hat)
            KI.learn(0, game_board, False)
            zug = KI.make_ai_move(game_board)
            if zug is not None:
                game_board[zug] = ai_symbol
                current_turn = "Player"
        
        board.draw_board(game_board)
        
        status = board.check_win_condition(game_board)
        if status:
            if status == "Tie":
                print("Unentschieden!")
                KI.learn(0.5, game_board, True) # Kleine Belohnung für Unentschieden
            elif status == player_symbol:
                print("Du hast gewonnen!")
                KI.learn(-1.0, game_board, True) # Bestrafung für Niederlage
            elif status == ai_symbol:
                print("Die KI hat gewonnen!")
                KI.learn(1.0, game_board, True) # Große Belohnung für Sieg
            KI.save_ai() # Wissen speichern
            break

if __name__ == "__main__":
    main()