from fastapi import  FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src import router


app = FastAPI(
    title="My Blog with fastapi and sqlmodel",
    description="This is a app of FastAPI with SQLModel",
    version="1.0"
)
# Configuration de CORS
origins = [
    "http://127.0.0.1:5500",  # Assure-toi que l'origine est ici
    # Ajoute d'autres origines si nécessaire
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Liste des origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP
    allow_headers=["*"],  # Autorise tous les en-têtes
)

app.include_router(router.router, prefix="/API", tags=["post"])