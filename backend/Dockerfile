# Utiliser une image de base Python officielle
FROM python:3.10-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    && apt-get clean

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du répertoire backend dans le conteneur
COPY . /app/

# Exposer le port utilisé par Django
EXPOSE 8000

# Commande par défaut pour lancer l'application Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
