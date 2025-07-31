from fastapi import FastAPI
from api.pokemon_routes import router as pokemon_router
from api.ask_routes import router as ask_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir origens do front-end
origins = [
    "http://localhost:5173",  # Vite
    "http://localhost:3000",  # React dev padrão
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # Libera só essas origens
    allow_credentials=True,
    allow_methods=["*"],                # Libera todos os métodos (GET, POST etc.)
    allow_headers=["*"],                # Libera todos os headers
)

app.include_router(pokemon_router)
app.include_router(ask_router)