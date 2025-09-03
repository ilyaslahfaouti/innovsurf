#!/bin/bash

# Déploiement InnovSurf sur Railway (gratuit et simple)
set -e

echo "🚀 Déploiement InnovSurf sur Railway"

# Vérifier que Railway CLI est installé
if ! command -v railway &> /dev/null; then
    echo "📦 Installation de Railway CLI..."
    npm install -g @railway/cli
fi

# Vérifier Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas démarré. Démarrez Docker Desktop."
    exit 1
fi

echo "🔐 Connexion à Railway..."
railway login

echo "🚂 Création du projet Railway..."
railway init

echo "📦 Déploiement des services..."

# Déployer le backend
echo "🔧 Déploiement du backend..."
cd backend
railway up --service backend
cd ..

# Déployer le frontend
echo "🎨 Déploiement du frontend..."
cd frontend
railway up --service frontend
cd ..

# Déployer la base de données
echo "🗄️ Déploiement de la base de données..."
railway add mysql

echo "✅ Déploiement Railway terminé !"
echo "🌐 Votre site est disponible sur Railway"
echo "📊 Gestion : https://railway.app/dashboard"
