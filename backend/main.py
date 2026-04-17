from fastapi import FastAPI, Request
from pydantic import BaseModel
import database
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando servidor e conectando bd...")
    inicia_banco()

    yield

    print("Desligando servidor...")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://calculadora-cashback.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class RequisicaoCashback(BaseModel): #Classe na requisição para não ser alterado
    valor_subtotal:float
    percentual_cupom:float
    is_vip: bool


def calcula_cashback(valor_subtotal, percentual_cupom, is_vip): #Função de lógica de cashback
    cupom = (percentual_cupom/100) * valor_subtotal
    valor_total = valor_subtotal - cupom
    cashback = valor_total * 0.05
    
    if valor_total > 500:
        cashback *= 2
    
    if is_vip:
        bonus_vip = cashback * 0.10
        cashback += bonus_vip
    
    return {
        "Valor_Total":valor_total,
        "Plano":is_vip,
        "Cashback":cashback
        }

# Rotas API
@app.get("/consulta/historico")

def historico_db(request:Request):
    conexao = None
    try:
        ip_cliente = request.client.host
        conexao = database.get_conexao()
        resultado = database.consulta_tabela_ip(conexao, ip_cliente)
        return {"dados": resultado}
    
    finally:
        if conexao is not None:
            conexao.close()

@app.post("/consulta/cashback")      
def processar_venda(dados: RequisicaoCashback, request: Request):
    try:
        ip_cliente = request.client.host
        conexao = database.get_conexao()
        resultado = calcula_cashback(dados.valor_subtotal, dados.percentual_cupom, dados.is_vip)

        database.preenche_tabela(
            conexao = conexao,
            ip=ip_cliente,
            valor_total=resultado["Valor_Total"],
            cupom=dados.percentual_cupom,
            cashback=resultado["Cashback"],
            vip=dados.is_vip
        )

        return resultado
    finally:
        if conexao is not None:
            conexao.close()