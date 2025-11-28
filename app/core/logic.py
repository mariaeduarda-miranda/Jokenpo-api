from typing import Dict


def determine_winner(player_move: str, cpu_move: str) -> Dict[str, str]:
    """
    Determina o resultado de uma rodada de Jokenpô.
    Retorna um dicionário com 'result' (WIN, LOSE, DRAW) e 'message'.
    """

    player_move = player_move.upper()
    cpu_move = cpu_move.upper()

    # Mapeamento da lógica: {Movimento Vencedor: Movimento Perdedor}
    rules = {
        "PEDRA": "TESOURA",
        "TESOURA": "PAPEL",
        "PAPEL": "PEDRA"
    }

    if player_move == cpu_move:
        return {"result": "DRAW", "message": f"{player_move} e {cpu_move}. Empate!"}

    elif rules.get(player_move) == cpu_move:
        return {"result": "WIN", "message": f"{player_move} quebra {cpu_move}. Você venceu!"}

    else:
        # A CPU ganhou
        return {"result": "LOSE", "message": f"{cpu_move} ganha de {player_move}. A CPU venceu!"}