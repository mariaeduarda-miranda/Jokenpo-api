import sqlite3
import os
from typing import Optional

# Nome do arquivo do banco de dados SQLite
DATABASE_FILE = "jokenpo_api.db"


def get_db_connection():
    """Retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_FILE)
    # Define a fábrica de linhas para permitir acesso a colunas por nome
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    """Cria as tabelas 'players' e 'games' se elas não existirem."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela 1: Jogadores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Tabela 2: Histórico de Jogadas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            player_move TEXT NOT NULL,
            cpu_move TEXT NOT NULL,
            result TEXT NOT NULL, -- WIN, LOSE, DRAW
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players (id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"Banco de dados '{DATABASE_FILE}' inicializado com sucesso.")