import random
import json
import os

DATA_FILE = "ki_memory.json"
q_table = {}
ALPHA = 0.5
GAMMA = 0.9
last_state = None
last_action = None

def get_state_key(board):
    return "".join(board)

def load_ai():
    global q_table
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                q_table = json.load(f)
        except:
            q_table = {}

def save_ai():
    with open(DATA_FILE, "w") as f:
        json.dump(q_table, f)

def make_ai_move(board):
    global last_state, last_action
    state = get_state_key(board)
    possible_moves = [i for i, x in enumerate(board) if x == " "]
    
    if not possible_moves:
        return None

    if state not in q_table:
        q_table[state] = [0.0] * 9

    # Epsilon-Greedy Strategie: Manchmal zufällig ziehen (Exploration), meistens den besten Zug (Exploitation)
    if random.random() < 0.1:
        action = random.choice(possible_moves)
    else:
        q_values = q_table[state]
        best_val = -float('inf')
        candidates = []
        for m in possible_moves:
            if q_values[m] > best_val:
                best_val = q_values[m]
                candidates = [m]
            elif q_values[m] == best_val:
                candidates.append(m)
        action = random.choice(candidates)

    last_state = state
    last_action = action
    return action

def update_q_table(state, action, reward, next_state_key, game_over):
    global q_table
    if state not in q_table:
        q_table[state] = [0.0] * 9

    old_q_value = q_table[state][action]
    
    future_optimal_value = 0
    if not game_over and next_state_key:
        if next_state_key not in q_table:
            q_table[next_state_key] = [0.0] * 9
        future_optimal_value = max(q_table[next_state_key])

    new_q_value = old_q_value + ALPHA * (reward + GAMMA * future_optimal_value - old_q_value)
    q_table[state][action] = new_q_value

def learn(reward, current_board, game_over):
    global last_state, last_action
    if last_state is None or last_action is None:
        return
    current_state_key = get_state_key(current_board)
    update_q_table(last_state, last_action, reward, current_state_key, game_over)
    if game_over:
        last_state = None
        last_action = None

def check_winner(board):
    """Hilfsfunktion: Prüft auf Gewinner (für das Training)."""
    lines = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a,b,c in lines:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    if " " not in board:
        return "Draw"
    return None

def train_self_play(episodes=10000):
    """Trainiert die KI durch Spiele gegen sich selbst (sehr effektiv)."""
    print(f"Starte Training mit {episodes} Spielen gegen sich selbst...")
    
    # Temporär Exploration erhöhen, damit sie viel ausprobiert
    temp_epsilon = 0.2
    
    for i in range(1, episodes + 1):
        board = [" "] * 9
        current_player = "X"
        history_x = None # (state, action)
        history_o = None # (state, action)
        
        while True:
            state = get_state_key(board)
            possible_moves = [idx for idx, x in enumerate(board) if x == " "]
            if not possible_moves: break
            
            # Zugwahl (vereinfacht für Training)
            if random.random() < temp_epsilon or state not in q_table:
                action = random.choice(possible_moves)
            else:
                # Greedy Wahl basierend auf Wissen
                q_vals = q_table[state]
                best_val = -float('inf')
                candidates = []
                for m in possible_moves:
                    if q_vals[m] > best_val:
                        best_val = q_vals[m]
                        candidates = [m]
                    elif q_vals[m] == best_val:
                        candidates.append(m)
                action = random.choice(candidates)
            
            board[action] = current_player
            
            # Lernen: Der Spieler, der NICHT dran ist, lernt aus dem Zug des anderen
            if current_player == "X":
                if history_o: # O lernt, dass sein letzter Zug zu diesem State führte
                    update_q_table(history_o[0], history_o[1], 0, state, False)
                history_x = (state, action)
                current_player = "O"
            else:
                if history_x: # X lernt
                    update_q_table(history_x[0], history_x[1], 0, state, False)
                history_o = (state, action)
                current_player = "X"
            
            winner = check_winner(board)
            if winner:
                reward_win = 1.0
                reward_loss = -1.0
                reward_draw = 0.5
                
                if winner == "Draw":
                    if history_x: update_q_table(history_x[0], history_x[1], reward_draw, None, True)
                    if history_o: update_q_table(history_o[0], history_o[1], reward_draw, None, True)
                elif winner == "X":
                    if history_x: update_q_table(history_x[0], history_x[1], reward_win, None, True)
                    if history_o: update_q_table(history_o[0], history_o[1], reward_loss, None, True)
                else: # O gewinnt
                    if history_o: update_q_table(history_o[0], history_o[1], reward_win, None, True)
                    if history_x: update_q_table(history_x[0], history_x[1], reward_loss, None, True)
                break
        
        # Fortschrittsanzeige alle 1000 Spiele
        if i % 1000 == 0:
            print(f"\rTraining läuft... {i}/{episodes} ({i/episodes*100:.1f}%)", end="")
            
    print("\nTraining abgeschlossen.")
    save_ai()
        