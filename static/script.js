let boardState = [" ", " ", " ", " ", " ", " ", " ", " ", " "];
let gameActive = true;

const boardElement = document.getElementById('board');
const statusElement = document.getElementById('status');

function initBoard() {
    boardElement.innerHTML = '';
    boardState.forEach((cell, index) => {
        const cellDiv = document.createElement('div');
        cellDiv.classList.add('cell');
        cellDiv.dataset.index = index;
        cellDiv.addEventListener('click', handleCellClick);
        
        if (cell !== " ") {
            cellDiv.classList.add(cell.toLowerCase());
            cellDiv.innerHTML = `<span>${cell}</span>`;
        }
        
        boardElement.appendChild(cellDiv);
    });
}

async function handleCellClick(e) {
    const index = e.target.dataset.index;

    if (boardState[index] !== " " || !gameActive) return;

    // Zustand für Backend sichern, bevor wir ihn lokal ändern
    const boardForBackend = [...boardState];

    // Optimistisches UI-Update (sofort anzeigen)
    updateBoardUI(index, "X");
    statusElement.innerText = "KI denkt nach...";
    gameActive = false; // Sperren bis Antwort kommt

    try {
        const response = await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ board: boardForBackend, move: index })
        });

        const data = await response.json();
        
        if (data.error) {
            alert(data.error);
            return;
        }

        boardState = data.board;
        initBoard(); // Board komplett neu zeichnen mit KI Antwort

        if (data.winner) {
            endGame(data.winner);
        } else {
            gameActive = true;
            statusElement.innerText = "Dein Zug (X)";
        }

    } catch (error) {
        console.error("Fehler:", error);
        statusElement.innerText = "Verbindungsfehler!";
    }
}

function updateBoardUI(index, player) {
    boardState[index] = player;
    const cell = boardElement.children[index];
    cell.classList.add(player.toLowerCase());
    cell.innerHTML = `<span>${player}</span>`;
}

function endGame(winner) {
    gameActive = false;
    if (winner === "Tie") {
        statusElement.innerText = "Unentschieden!";
        statusElement.style.color = "#fff";
    } else {
        statusElement.innerText = winner === "X" ? "Du hast gewonnen!" : "KI hat gewonnen!";
        statusElement.style.color = winner === "X" ? "var(--accent-color)" : "var(--loss-color)";
    }
}

async function resetGame() {
    const response = await fetch('/new_game', { method: 'POST' });
    const data = await response.json();
    boardState = data.board;
    gameActive = true;
    statusElement.innerText = "Dein Zug (X)";
    statusElement.style.color = "#666";
    initBoard();
}

// Start
initBoard();
