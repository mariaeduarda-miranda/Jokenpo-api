✂️ API Jokenpô (Pedra, Papel, Tesoura)
Esta é uma API RESTful simples para o clássico jogo Jokenpô (Pedra, Papel, Tesoura), onde um jogador humano compete contra uma CPU com jogadas aleatórias.

A arquitetura da API foi desenvolvida em camadas, garantindo a separação de preocupações (Modelos, Lógica de Negócios e Persistência de Dados).


💻 Tecnologias e Frameworks Utilizados
Framework Principal: FastAPI (para criação da API e roteamento).

Servidor ASGI: Uvicorn (para rodar a aplicação).

Validação de Dados: Pydantic (para definir schemas de entrada e saída).

Persistência de Dados: SQLite3 (banco de dados leve e embutido, persistindo jogadores e histórico no arquivo jokenpo_api.db).

Linguagem: Python 3.x.


▶️ Como Rodar o Projeto
Siga estas instruções para configurar e executar a API na sua máquina local.

1. Pré-requisitos
Certifique-se de ter o Python 3.x e o pip (gerenciador de pacotes) instalados.

2. Instalação das Dependências
Na raiz do seu projeto (jokenpo-api/), instale as bibliotecas necessárias:

pip install fastapi uvicorn pydantic

O servidor estará ativo em http://127.0.0.1:8000.

A documentação interativa (Swagger UI) estará disponível em: http://127.0.0.1:8000/docs


🧪 Exemplos de Requisições (Endpoints Principais)
Todos os testes podem ser realizados diretamente pelo Swagger UI (/docs) ou utilizando uma ferramenta como o Postman. A URL base é http://localhost:8000.


1. Criar um JogadorEndpoint: POST /players -> Descrição: Registra um novo jogador e retorna seu ID

Requisição
URL: POST 
http://localhost:8000/players
Resposta: Resposta (Sucesso - 200 OK)
Body (JSON):
json\n{\n "name": "João"\n}
Body (JSON)
json\n{\n "player_id": 1,\n "name": "João"\n}
OU
Requisição:
URL: POST
http://localhost:8000/players
Resposta (Erro - 400 Bad Request)
Body (JSON): (Usando o mesmo nome "João")
json\n{\n "name": "João"\n}
Body (JSON): (Formato de erro personalizado)
json\n{\n "error": "O nome 'João' já está em uso...",\n "code": 400\n}

