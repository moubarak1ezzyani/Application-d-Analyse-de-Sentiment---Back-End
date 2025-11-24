# import os
# import requests
# import jwt
# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException,Header
# from pydantic import BaseModel


#     # _____ Integrer Hugging Face Inference API : 
#     # --- Gestion de la cle API
# load_dotenv()       # Gestion de cle : env
# app = FastAPI()
# HF_TOKEN= os.getenv("HF_TOKEN_API")
# API_URL = os.getenv("API_URL_env")
# JWT_SECRET = os.getenv("JWT_SECRET_env")

# # L'implementation de FastAPI
# class LoginData(BaseModel):
#     username : str
#     password : str

# class PredictData(BaseModel):
#     text_tx : str

# # --- endpoint Login
# @app.post("/login")
# def login(data : LoginData):
#     if data.username == "admin" and data.password == "1234":

#         # --- Creation : Token JWT
#         payload = {"username" : data.username}
#         token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
#         return {"access_token" : token, "token_type" : "Bearer"}
#     raise HTTPException(status_code = 401, detail = "Identifiants incorrects")

# # --- endpoin PREDICT (Service IA Sécurisé) ---
# @app.post("/predict")
# def predict(authorization: str = Header()):
#     print("auth : ",authorization)
    
#     # Verification de securite (Middleware manuel)
#     if authorization is None or not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Token manquant")
    
#     token_recu = authorization.split(" ")[1]        # On enlève le mot 'Bearer'
    
#     try:
#         decoded = jwt.decode(token_recu, JWT_SECRET, algorithms=["HS256"])  # PASSED : token valide
#     except:
#         raise HTTPException(status_code=401, detail="Token invalide ou expiré")

#     # --- APPEL AU SERVICE IA : HUGG FACE
#     headers_hf = {"Authorization": f"Bearer {HF_TOKEN}"}
#     payload_hf = {"inputs": data.text_tx}
    
#     try:
#         response = requests.post(API_URL, headers=headers_hf, json=payload_hf)
#         response.raise_for_status()         # Vérifie les erreurs HTTP (4xx, 5xx)
        
#         # On renvoie directement le résultat de l'IA
#         return {"resultat_ia": response.json(), "user_used": decoded['admin']}
        
#     except Exception as e:
#         raise HTTPException(status_code=503, detail=f"Erreur IA: {str(e)}")

# def verify_token(authorization: str = Header(None)):
#     # 1. Vérifier si le header existe et commence par Bearer
#     if authorization is None or not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Token manquant ou format invalide")
    
#     # 2. Extraire le token
#     token_recu = authorization.split(" ")[1]
    
#     # 3. Décoder et vérifier le token
#     try:
#         decoded = jwt.decode(token_recu, JWT_SECRET, algorithms=["HS256"])
#         return decoded # Si tout va bien, on renvoie les infos de l'utilisateur
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expiré")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Token invalide")

# ----------------------------------------------------------
import os, requests, jwt
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel

load_dotenv()       # Gestion de la cle : env
app = FastAPI()

    # _____ Integrer Hugging Face Inference API : 
    # --- Gestion de la cle API
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = os.getenv("API_URL_env")
JWT_SECRET = os.getenv("JWT_SECRET_env")
ALGO = os.getenv("algo_env")

# Implementation
class User(BaseModel):
    username : str
    password: str

class TextInput(BaseModel):
    text_tx: str

# --- Dépendance : Le Gardien  ---
def get_current_user(authorization: str = Header(...)):        # get_c()
    """ if not authorization:
        # print("Token Manquant") 
        raise HTTPException(401, "Token manquant")
    try:
        # On coupe "Bearer <token>" et on décode
        return jwt.decode(authorization.split(" ")[1], JWT_SECRET, algorithms=ALGO)
    except:
        raise HTTPException(401, "Token invalide ou expiré") """
    print(authorization)

# --- Login ---
@app.post("/login")
def login(user: User):
    if user.username == "admin" and user.password == "1234":
        token = jwt.encode({"sub": user.username}, JWT_SECRET, algorithm=ALGO)
        # Conversion bytes -> str nécessaire sur certaines versions de python
        return {"access_token": token if isinstance(token, str) else token.decode()}
    raise HTTPException(401, "Mauvais identifiants")

# --- Prédiction (Protégée) ---
@app.post("/predict")
def predict(input: TextInput, token: str = Header()):
    print(input.text_tx)
    print(HF_TOKEN)
    print(type(HF_TOKEN))

    try:
        # 🔹 Décodage du JWT
        payload = jwt.decode(token, key=JWT_SECRET, algorithms=[ALGO])

        response = requests.post(
            API_URL, 
            headers={"Authorization": f"Bearer {HF_TOKEN}"}, 
            json={"inputs": input.text_tx}
        )
        response.raise_for_status()

        return {
            "sentiment": response.json(),
            "user": payload["sub"]
        }

    except Exception as e:
        raise HTTPException(503, f"Erreur Service IA: {str(e)}")
"""     
@app.post("/get_token")
async def token(input: TextInput,token :str = Header()):
    try:
        data = jwt.decode(token,key=JWT_SECRET,algorithms=ALGO)
        if token :
            response = requests.post(
            API_URL, 
            headers={"Authorization": f"Bearer {HF_TOKEN}"}, 
            json={"inputs": input.text_tx}
        )
            response.raise_for_status()     # Vérifie si HF renvoie une erreur
        return {"sentiment": response.json(), "user": data["sub"]}
        
    except:
        raise HTTPException(402,f'token invalide') """

   