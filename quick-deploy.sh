#!/bin/bash

# Script de déploiement rapide InnovSurf
set -e

echo "🚀 Déploiement InnovSurf - Version Simplifiée"

# Variables par défaut
DOCKERHUB_USERNAME="innovsurf$(date +%s)"
AWS_REGION="us-east-1"
INSTANCE_TYPE="t2.micro"

echo "📋 Configuration automatique..."

# Vérifier Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas démarré. Démarrez Docker Desktop et relancez le script."
    exit 1
fi

echo "✅ Docker fonctionne"

# Créer un nom d'utilisateur Docker Hub unique
echo "🐳 Nom d'utilisateur Docker Hub généré: $DOCKERHUB_USERNAME"
echo "📝 Créez un compte sur https://hub.docker.com avec ce nom: $DOCKERHUB_USERNAME"

# Attendre que l'utilisateur confirme
read -p "✅ Avez-vous créé le compte Docker Hub ? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Créez d'abord le compte Docker Hub sur https://hub.docker.com"
    exit 1
fi

# Connexion Docker Hub
echo "🔐 Connexion à Docker Hub..."
echo "Entrez vos identifiants Docker Hub :"
docker login

# Build des images
echo "📦 Construction des images Docker..."
docker build -t $DOCKERHUB_USERNAME/innovsurf-backend:latest ./backend
docker build -t $DOCKERHUB_USERNAME/innovsurf-frontend:latest ./frontend

# Push des images
echo "📤 Push des images vers Docker Hub..."
docker push $DOCKERHUB_USERNAME/innovsurf-backend:latest
docker push $DOCKERHUB_USERNAME/innovsurf-frontend:latest

echo "✅ Images Docker Hub créées et poussées !"
echo "🌐 Vos images sont disponibles sur :"
echo "   - https://hub.docker.com/r/$DOCKERHUB_USERNAME/innovsurf-backend"
echo "   - https://hub.docker.com/r/$DOCKERHUB_USERNAME/innovsurf-frontend"

# Créer le fichier .env de production
cat > .env.prod << EOF
DOCKERHUB_USERNAME=$DOCKERHUB_USERNAME
SECRET_KEY=$(openssl rand -base64 32)
DB_USER=innovsurf
DB_PASSWORD=$(openssl rand -base64 16)
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

echo "📋 Fichier .env.prod créé"
echo "🎉 Déploiement Docker Hub terminé !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Créez un compte AWS sur https://aws.amazon.com/fr/free/"
echo "2. Configurez AWS CLI : aws configure"
echo "3. Lancez : ./deploy-aws.sh"
echo ""
echo "🔗 Ou utilisez un autre hébergeur cloud gratuit :"
echo "   - Railway.app (gratuit)"
echo "   - Render.com (gratuit)"
echo "   - Fly.io (gratuit)"
