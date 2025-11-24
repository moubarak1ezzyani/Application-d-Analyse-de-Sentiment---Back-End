# 🧠 Sentiment Analysis API (Backend)

Microservice backend performant développé avec **FastAPI**. Ce service expose une API REST sécurisée permettant d'analyser le sentiment d'un texte en utilisant le modèle d'IA `nlptown/bert-base-multilingual-uncased-sentiment` via l'API d'inférence de Hugging Face.

Ce projet assure l'authentification, la gestion des erreurs et la transformation des scores de l'IA.



## ⚡ Fonctionnalités

* **API REST Rapide :** Basée sur FastAPI et Uvicorn.
* **Sécurité JWT :** Système d'authentification complet (Login + Protection des routes).
* **Intégration IA :** Connexion asynchrone à l'API Hugging Face.
* **Documentation Interactive :** Swagger UI et Redoc intégrés automatiquement.
* **Logique Métier :** Conversion des scores "étoiles" (1-5) en sentiments (Négatif/Neutre/Positif).
* **Docker Ready :** Conteneurisation complète pour un déploiement facile.


## 🛠️ Stack Technique

* **Langage :** Python 3.11+
* **Framework :** FastAPI
* **Sécurité :** PyJWT (JSON Web Tokens)
* **Client HTTP :** Requests
* **Serveur :** Uvicorn
* **Gestion d'env :** Python-dotenv


## ⚙️ Installation et Configuration

### 1. Cloner le projet
```bash
git clone [https://github.com/VOTRE-USERNAME/NOM-DU-REPO-BACKEND.git](https://github.com/VOTRE-USERNAME/NOM-DU-REPO-BACKEND.git)
cd NOM-DU-REPO-BACKEND
````

### 2\. Variables d'environnement (Critique)

Créez un fichier `.env` à la racine du projet. **Ce fichier ne doit pas être commité.**

```ini
# .env
# Votre clé API Hugging Face ([https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens))
HF_API_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxx"

# Clé secrète pour signer les tokens JWT (générez une chaîne aléatoire)
JWT_SECRET="votre_super_secret_key_change_me"

# (Optionnel) URL du modèle si vous souhaitez le changer
HF_API_URL="[https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment](https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment)"
```

### 3\. Installation locale (Sans Docker)

Créez un environnement virtuel et installez les dépendances :

```bash
python -m venv venv
# Windows :
.\venv\Scripts\activate
# Mac/Linux :
source venv/bin/activate

pip install -r requirements.txt
```

Lancez le serveur :

```bash
uvicorn main:app --reload
```

L'API sera accessible sur : `http://localhost:8000`



## 🐳 Démarrage avec Docker

Pour lancer le backend dans un conteneur isolé :

```bash
# 1. Construire l'image
docker build -t sentiment-backend .

# 2. Lancer le conteneur (en chargeant le fichier .env)
docker run -p 8000:8000 --env-file .env sentiment-backend
```


## 📖 Documentation de l'API (Endpoints)

Une fois le serveur lancé, accédez à la documentation interactive complète sur `http://localhost:8000/docs`.

### Résumé des routes :

| Méthode | Endpoint | Accès | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/login` | Public | Prend `{username, password}` et retourne un `access_token`. |
| `POST` | `/predict` | **Privé** | Prend `{text}`. Nécessite un header `Authorization: Bearer <TOKEN>`. |
| `GET` | `/` | Public | Health check (vérification que l'API tourne). |


## 🧪 Tests

Des tests unitaires sont disponibles (si implémentés avec pytest) :

```bash
pytest
```

## 🤝 Contribution

Les contributions sont bienvenues. Merci d'ouvrir une issue pour discuter des changements majeurs.

### 📝 Descriptions pour vos dépôts GitHub

Voici les textes courts à copier-coller dans la section **"About"** (la petite description à droite sur la page d'accueil de chaque dépôt GitHub).

#### Pour le Repo **FRONTEND** :
> Interface utilisateur réactive développée avec **Next.js** et **Tailwind CSS**. Elle permet l'authentification utilisateur et la visualisation en temps réel des analyses de sentiment via une consommation sécurisée de l'API Backend.

#### Pour le Repo **BACKEND** :
> Microservice API robuste construit avec **FastAPI** et **Docker**. Il gère l'authentification **JWT** et orchestre l'analyse de sentiment en connectant le modèle **Hugging Face BERT** au frontend.
```
