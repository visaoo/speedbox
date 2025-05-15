import os

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

# Defina o diretório dos templates, ajustando o caminho para a pasta "api/templates"
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Monta a pasta "static" para servir arquivos estáticos
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Rota que renderiza o index
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para a página de login
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Rota para a página de cadastro
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# API para registrar usuário

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # vercel.com
    allow_methods=["*"],  #get e post
    allow_headers=["*"], 
)

@app.post("/api/register-client")
async def get_data(
    client_name: str = Form(...),
    client_cpf: str = Form(...),
    client_phone: str = Form(...),
    client_birth: str = Form(...),
    client_email: str = Form(...),
    client_password: str = Form(...),
    client_address: str = Form(...),
    client_neighborhood: str = Form(...),
    client_city: str = Form(...),
    client_state: str = Form(...),
): 
    try:
        return {
            "msg": "Cliente cadastrado com sucesso",
            "data": {
                "client_name": client_name,
                "client_cpf": client_cpf,
                "client_phone": client_phone,
                "client_birth": client_birth,
                "client_email": client_email,
                "client_password": client_password,
                "client_address": client_address,
                "client_neighborhood": client_neighborhood,
                "client_city": client_city,
                "client_state": client_state,
            }
        }
    except Exception as e:
        return {"error": f"Erro ao salvar: {str(e)}"}

@app.post("/api/register-delivery")
async def register_delivery(
    delivery_name: str = Form(...),
    delivery_cpf: str = Form(...),
    delivery_phone: str = Form(...),
    delivery_birth: str = Form(...),
    delivery_cnh: str = Form(...),
    delivery_vehicle_type: str = Form(...),
    delivery_email: str = Form(...),
    delivery_password: str = Form(...),
):
    try:
        return {
            "msg": "Entregador cadastrado com sucesso",
            "data": {
                "delivery_name": delivery_name,
                "delivery_cpf": delivery_cpf,
                "delivery_phone": delivery_phone,
                "delivery_birth": delivery_birth,
                "delivery_cnh": delivery_cnh,
                "delivery_vehicle_type": delivery_vehicle_type,
                "delivery_email": delivery_email,
                "delivery_password": delivery_password,
            }
        }
    except Exception as e:
        return {"error": f"Erro ao salvar: {str(e)}"}

@app.post("/api/register-enterprise")
async def register_enterprise(
    enterprise_owner_name: str = Form(...),
    enterprise_name: str = Form(...),
    enterprise_cnpj: str = Form(...),
    enterprise_phone: str = Form(...),
    enterprise_address: str = Form(...),
    enterprise_neighborhood: str = Form(...),
    enterprise_city: str = Form(...),
    enterprise_state: str = Form(...),
    enterprise_email: str = Form(...),
    enterprise_password: str = Form(...),
):
    try:
        return {
            "msg": "Empresa cadastrada com sucesso",
            "data": {
                "enterprise_owner_name": enterprise_owner_name,
                "enterprise_name": enterprise_name,
                "enterprise_cnpj": enterprise_cnpj,
                "enterprise_phone": enterprise_phone,
                "enterprise_address": enterprise_address,
                "enterprise_neighborhood": enterprise_neighborhood,
                "enterprise_city": enterprise_city,
                "enterprise_state": enterprise_state,
                "enterprise_email": enterprise_email,
                "enterprise_password": enterprise_password,
            }
        }
    except Exception as e:
        return {"error": f"Erro ao salvar: {str(e)}"}
    
    # lista de atividades para amanhã
    
    # fazer conexão e armazenar no banco
    # agora deve manter a página e de preferencia devo colocar validação de input msg/modal de confirmação e erro,
    # a pessoa vai poder logar na sua conta (se der tempo)
    # aí eu acho que iria precisar de uma rota get para poder pegar os dados validados no banco