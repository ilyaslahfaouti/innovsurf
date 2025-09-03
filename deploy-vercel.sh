#!/bin/bash

# Déploiement InnovSurf sur Vercel (gratuit et simple)
set -e

echo "🚀 Déploiement InnovSurf sur Vercel"

# Vérifier que Vercel CLI est installé
if ! command -v vercel &> /dev/null; then
    echo "📦 Installation de Vercel CLI..."
    npm install -g vercel
fi

echo "🔐 Connexion à Vercel..."
vercel login

echo "📦 Déploiement du frontend..."
cd frontend
vercel --prod
cd ..

echo "✅ Déploiement Vercel terminé !"
echo "🌐 Votre site est disponible sur Vercel"
echo "📊 Gestion : https://vercel.com/dashboard"
