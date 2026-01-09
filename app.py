from flask import Flask, render_template, request, jsonify
import KI
import board as board_logic # Wir nutzen deine board.py Logik, nennen sie aber board_logic um Verwirrung zu vermeiden

app = Flask(__name__)

# KI initial laden
KI.load_ai()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    # Setzt globale KI-Variablen zurück, falls nötig
    KI.last_state = None
    KI.last_action = None
    return jsonify({"message": "New Game Started", "board": [" "] * 9})

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    game_board = data['board']
    player_move = int(data['move'])

    # 1. Spielerzug prüfen und ausführen
    if not board_logic.check_if_valid(game_board, player_move):
        return jsonify({"error": "Invalid move"}), 400
    
    game_board[player_move] = "X"
    
    # Check ob Spieler gewonnen hat
    winner = board_logic.check_win_condition(game_board)
    if winner:
        if winner == "X": KI.learn(-1.0, game_board, True)
        elif winner == "Tie": KI.learn(0.5, game_board, True)
        KI.save_ai()
        return jsonify({"board": game_board, "winner": winner})

    # 2. KI ist dran
    # KI lernt aus dem Zustand NACH dem Spielerzug (dass sie noch lebt)
    KI.learn(0, game_board, False)
    
    ai_move = KI.make_ai_move(game_board)
    
    if ai_move is not None:
        game_board[ai_move] = "O"
    
    # Check ob KI gewonnen hat
    winner = board_logic.check_win_condition(game_board)
    if winner:
        if winner == "O": KI.learn(1.0, game_board, True)
        elif winner == "Tie": KI.learn(0.5, game_board, True)
        KI.save_ai()
    
    return jsonify({"board": game_board, "winner": winner})

if __name__ == '__main__':
    # Debug mode erlaubt automatisches Neuladen bei Code-Änderungen
    app.run(debug=True, port=5000)