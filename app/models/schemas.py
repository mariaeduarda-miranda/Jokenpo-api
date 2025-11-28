from pydantic import BaseModel
from typing import List, Dict

class Player(BaseModel):
    """Modelo para criação de um novo jogador (input)."""
    name: str

class PlayerOut(Player):
    """Modelo para o jogador retornado após a criação (output)."""
    player_id: int

class JokenpoMove(BaseModel):
    """Modelo para uma nova jogada (input)."""
    player_id: int
    move: str # Deve ser 'PEDRA', 'PAPEL', ou 'TESOURA'

class GameResult(BaseModel):
    """Modelo para o resultado de uma única jogada (output)."""
    player_id: int
    player_move: str
    cpu_move: str
    result: str # 'WIN', 'LOSE', 'DRAW'
    message: str

class HistoryEntry(BaseModel):
    """Modelo para um item do histórico de jogadas (output)."""
    player_move: str
    cpu_move: str
    result: str

class ScoreboardEntry(BaseModel):
    """Modelo para uma linha do placar (output)."""
    name: str
    player_id: int
    wins: int
    losses: int
    draws: int