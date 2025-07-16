from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fpdf import FPDF

# 🔥 Instanciando o app FastAPI
app = FastAPI()

# 🔓 Liberando CORS para acessar via Frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 💰 Função para cálculo baseado no cargo
def calcular_valor(cargo):
    tabela = {
        'Auxiliar': 4195.56,
        'Porteiro': 4595.00,
        'Zelador': 4895.00
    }
    return tabela.get(cargo, 0)

# 📄 Endpoint para gerar o PDF
@app.post("/gerar-pdf")
async def gerar_pdf(
    condominio: str = Form(...),
    periodo: str = Form(...),
    cargo: str = Form(...)
):
    valor = calcular_valor(cargo)

    # 📝 Criando o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    texto = f"""
Ao Condomínio {condominio},

Apresentamos a proposta do nosso plano de cobertura terceirizada para o cargo de {cargo} no período {periodo}.

✔ Mão de obra especializada e sem vínculos empregatícios.
✔ Garantia de 100% na cobertura dos serviços contratados.
✔ Economia na aquisição de fardamentos.
✔ Possibilidade de substituição sem custo.

O valor da cobertura é de R$ {valor:,.2f}.

O valor contempla salários, encargos, fardamentos e benefícios.

Salvador-BA, 25 de Junho de 2025.

Atenciosamente,

Grupo Solução & Cia
    """

    # 🔥 Inserindo texto no PDF
    for linha in texto.strip().split('\n'):
        pdf.multi_cell(0, 10, linha)

    # 💾 Salvando o PDF
    pdf.output("proposta.pdf")

    # 📤 Retornando o PDF como download
    return FileResponse(
        "proposta.pdf",
        media_type="application/pdf",
        filename="proposta.pdf"
    )

from fastapi.responses import FileResponse
import os

@app.get("/")
def home():
    return FileResponse(os.path.join("frontend", "index.html"))
