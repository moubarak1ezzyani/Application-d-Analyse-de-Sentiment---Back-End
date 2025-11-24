# Syntaxe Gitignore
## Fichiers individuels :
```
fichier.txt
database.db
*.log
```

## Dossiers complets :
```
dossier/
env/
node_modules/
__pycache__/
```

## Patterns courants :
```
# Environnements virtuels Python
env/
venv/
.venv/
envrmnt/

# Fichiers compilés
*.pyc
__pycache__/
*.so
*.dll

# Fichiers de données
*.csv
*.json
*.pkl

# Logs et temporaires
*.log
.cache/
temp/
```

## Exemple complet pour Python :
```
# Environnements
env/
venv/
.venv/
envrmnt/

# Fichiers Python
*.pyc
__pycache__/
.pytest_cache/

# Données et logs
*.db
*.sqlite3
*.log
data/
models/

# IDE
.vscode/
.idea/
*.swp
```

**Important :** Le fichier s'appelle exactement `.gitignore` (avec le point au début).