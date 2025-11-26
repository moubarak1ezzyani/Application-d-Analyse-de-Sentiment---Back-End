import os, requests, jwt
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware # <--- 1. Import vital
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

# ---------------------------------------------------------
# 1. CONFIGURATION DU CORS (Indispensable pour Next.js)
# ---------------------------------------------------------
origins = [
    "http://localhost:3000", # L'adresse de votre Frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Autorise POST, GET, OPTIONS...
    allow_headers=["*"], # Autorise les headers comme Authorization
)

# Variables d'environnement
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = os.getenv("API_URL_env")
JWT_SECRET = os.getenv("JWT_SECRET_env")
ALGO = os.getenv("algo_env")

# ---------------------------------------------------------
# 2. MODELES DE DONNEES
# ---------------------------------------------------------
class User(BaseModel):
    username: str
    password: str

class TextInput(BaseModel):
    text: str  # <--- 2. Renommé de 'text_tx' à 'text' pour matcher le frontend

# ---------------------------------------------------------
# 3. ROUTES
# ---------------------------------------------------------

@app.post("/login")
def login(user: User):
    # Authentification simulée (Hardcodée comme demandé)
    if user.username == "admin" and user.password == "1234":
        token = jwt.encode({"sub": user.username}, JWT_SECRET, algorithm=ALGO)
        # Gestion compatibilité version python pour jwt
        return {"access_token": token if isinstance(token, str) else token.decode()}
    
    raise HTTPException(status_code=401, detail="Mauvais identifiants")


# <--- 3. Route renommée de '/predict' à '/sentiment'
@app.post("/sentiment") 
def analyze_sentiment(input: TextInput, authorization: str = Header(None)):
    
    # --- A. Vérification du Token (Sécurité) ---
    if not authorization:
        raise HTTPException(status_code=401, detail="Token manquant")
    
    try:
        # Le frontend envoie : "Bearer eyJhbGci..."
        # On doit couper la chaîne pour ne garder que le code après "Bearer "
        token_clean = authorization.split(" ")[1] 
        
        # On vérifie si le token est valide
        payload = jwt.decode(token_clean, key=JWT_SECRET, algorithms=[ALGO])
        user_sub = payload.get("sub")
        
    except Exception as e:
        print(f"Erreur Token: {e}")
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    # --- B. Appel à Hugging Face ---
    try:
        response = requests.post(
            API_URL, 
            headers={"Authorization": f"Bearer {HF_TOKEN}"}, 
            json={"inputs": input.text} # On utilise input.text ici
        )
        response.raise_for_status()
        data_hf = response.json() 
        
        # Hugging Face renvoie souvent une liste de listes [[{'label': 'POS', 'score': 0.9}]]
        # On aplatit le résultat pour le frontend
        if isinstance(data_hf, list) and len(data_hf) > 0:
            # On prend le premier résultat (cas simple)
            # Parfois c'est une liste imbriquée (classification de texte)
            first_result = data_hf[0]
            if isinstance(first_result, list):
                first_result = first_result[0]
                
            return {
                "sentiment": first_result.get('label'),
                "score": first_result.get('score'),
                "user": user_sub
            }
            
        return data_hf # Cas de secours

    except Exception as e:
        print(f"Erreur API IA: {e}")
        raise HTTPException(status_code=503, detail="Erreur du service IA")