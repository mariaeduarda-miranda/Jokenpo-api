from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn

# Importa a função de inicialização do banco de dados
from app.core.database import initialize_db
# Importa o roteador que contém todos os endpoints
from app.api.endpoints import router as api_router

# --- Inicialização da API e BD ---
app = FastAPI(
    title="API Jokenpô",
    description="API com persistência em SQLite e tratamento de erros customizado."
)

# Inicializa o banco de dados na primeira execução
initialize_db()

# --- Manipulador de Exceções Personalizado ---
# Formata HTTPException para o padrão {"error": "...", "code": ...}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Formata o erro da HTTPException para o JSON personalizado.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "code": exc.status_code}
    )

# --- Incluindo Roteadores ---
# Conecta os endpoints definidos em api_router à aplicação principal
app.include_router(api_router)


if __name__ == "__main__":
    # Comando para rodar a aplicação via Uvicorn (opcional, normalmente rodamos via linha de comando)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)