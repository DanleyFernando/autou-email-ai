from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.api import email_routes

# ======================
# Inicialização do App
# ======================
app = FastAPI(
    title="AutoU Email Classifier",
    description="API para classificar e-mails e sugerir respostas",
    version="1.0.0"
)

# ======================
# Rotas da API
# ======================
app.include_router(email_routes.router, prefix="/api", tags=["Emails"])

# ======================
# Frontend (arquivos estáticos)
# ======================
app.mount("/static", StaticFiles(directory="public", html=True), name="static")

# ======================
# Redirect da raiz -> frontend
# ======================
@app.get("/", include_in_schema=False)
async def root():
    # Redireciona para o index.html do frontend
    return RedirectResponse(url="/static/index.html")
