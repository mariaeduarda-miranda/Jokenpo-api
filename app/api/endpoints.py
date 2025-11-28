from fastapi import APIRouter, HTTPException, status
import random
import sqlite3
from typing import List

# Importa os Schemas (Modelos de Dados)
from app.models.schemas import (
    Player, PlayerOut, JokenpoMove, GameResult,
    HistoryEntry, ScoreboardEntry
)

# Importa as Funções Core
from app.core.database import get_db_connection
from app.core.logic import determine_winner

# Cria um Roteador para agrupar todos os endpoints de Jokenpô
router = APIRouter(
    prefix="",  # Pode ser vazio ou '/v1' se você quiser prefixar
    tags=["Jokenpô"]
)


# --------------------------------------------------------------------------------
# 1. POST /players
# --------------------------------------------------------------------------------

@router.post("/players", response_model=PlayerOut, summary="Cria um novo jogador")
def create_player(player: Player):
    """Cria um novo jogador. Retorna 400 se o nome for vazio ou já existir."""

    name = player.name.strip()
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O nome do jogador não pode ser vazio."
        )

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
        player_id = cursor.lastrowid
        conn.commit()

        return PlayerOut(player_id=player_id, name=name)

    except sqlite3.IntegrityError:
        # 400 - Nome duplicado (violação UNIQUE)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O nome '{name}' já está em uso. Escolha outro nome."
        )
    finally:
        conn.close()


# --------------------------------------------------------------------------------
# 2. POST /jokenpo/play
# --------------------------------------------------------------------------------

@router.post("/jokenpo/play", response_model=GameResult, summary="Cria uma nova jogada de Jokenpô")
def play_jokenpo(game_move: JokenpoMove):
    """
    Realiza uma jogada de Jokenpô. Retorna 404 se o jogador não existir e 400 se a jogada for inválida.
    """
    player_id = game_move.player_id
    player_move = str(game_move.move).strip().upper()
    valid_moves = ["PEDRA", "PAPEL", "TESOURA"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Validação da Jogada (400 - Bad Request)
    if player_move not in valid_moves:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Movimento '{player_move}' é inválido. Escolha: PEDRA, PAPEL ou TESOURA."
        )

    # 2. Validação do Jogador (404 - Not Found)
    cursor.execute("SELECT name FROM players WHERE id = ?", (player_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogador com ID {player_id} não encontrado."
        )

    # 3. Processamento
    cpu_move = random.choice(valid_moves)
    result_data = determine_winner(player_move, cpu_move)
    result = result_data["result"]
    message = result_data["message"]

    # 4. Inserção no Histórico (tabela games)
    try:
        cursor.execute(
            "INSERT INTO games (player_id, player_move, cpu_move, result) VALUES (?, ?, ?, ?)",
            (player_id, player_move, cpu_move, result)
        )
        conn.commit()
    finally:
        conn.close()

    return GameResult(
        player_id=player_id,
        player_move=player_move,
        cpu_move=cpu_move,
        result=result,
        message=message
    )


# --------------------------------------------------------------------------------
# 3. GET /jokenpo/history/{player_id}
# --------------------------------------------------------------------------------

@router.get("/jokenpo/history/{player_id}", response_model=List[HistoryEntry],
            summary="Lista o histórico de jogadas do jogador")
def get_player_history(player_id: int):
    """Retorna o histórico de jogadas. Retorna 404 se o jogador não existir."""

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Validação do Jogador (404 - Not Found)
    cursor.execute("SELECT id FROM players WHERE id = ?", (player_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogador com ID {player_id} não encontrado."
        )

    # 2. Busca e retorno
    cursor.execute(
        "SELECT player_move, cpu_move, result FROM games WHERE player_id = ? ORDER BY timestamp DESC",
        (player_id,)
    )

    history_rows = cursor.fetchall()
    conn.close()

    history = [
        HistoryEntry(
            player_move=row['player_move'],
            cpu_move=row['cpu_move'],
            result=row['result']
        )
        for row in history_rows
    ]
    return history


# --------------------------------------------------------------------------------
# 4. GET /jokenpo/scoreboard
# --------------------------------------------------------------------------------

@router.get("/jokenpo/scoreboard", response_model=List[ScoreboardEntry],
            summary="Mostra o placar resumido de todos os jogadores")
def get_scoreboard():
    """Retorna o placar consolidado de todos os jogadores, calculado dinamicamente pelo SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta SQL que calcula as somas de WIN, LOSE e DRAW para cada jogador
    cursor.execute("""
        SELECT
            p.id,
            p.name,
            SUM(CASE WHEN g.result = 'WIN' THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN g.result = 'LOSE' THEN 1 ELSE 0 END) as losses,
            SUM(CASE WHEN g.result = 'DRAW' THEN 1 ELSE 0 END) as draws
        FROM players p
        LEFT JOIN games g ON p.id = g.player_id
        GROUP BY p.id, p.name
        ORDER BY wins DESC, losses ASC
    """)

    scoreboard_rows = cursor.fetchall()
    conn.close()

    scoreboard_list = [
        ScoreboardEntry(
            name=row['name'],
            player_id=row['id'],
            wins=row['wins'] if row['wins'] is not None else 0,
            losses=row['losses'] if row['losses'] is not None else 0,
            draws=row['draws'] if row['draws'] is not None else 0,
        )
        for row in scoreboard_rows
    ]

    return scoreboard_list