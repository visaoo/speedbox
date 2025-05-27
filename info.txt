# speedbox

# comandos:
task lint
task format

# adicionar bibliotecas externas:
poetry add 

# se for apenas para nós usarmos
poetry add --group dev 

# entrar no venv (talvez irao ter que install o shell, mas aí é mais pra frente)
poetry env activate

# comando para rodar a landing page localmente (caso de erro troque de rota)

poetry run uvicorn api.main:app --reload

poetry run uvicorn api.main:app --reload --route(numero da porta)