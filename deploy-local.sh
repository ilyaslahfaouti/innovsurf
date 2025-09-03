#!/bin/bash

# Déploiement local InnovSurf
set -e

echo "🚀 Déploiement local InnovSurf"

# Vérifier Docker
if ! docker --version > /dev/null 2>&1; then
    echo "❌ Docker n'est pas disponible. Démarrez Docker Desktop."
    exit 1
fi

echo "✅ Docker fonctionne"

# Créer le fichier .env local
cat > .env.local << EOF
DOCKERHUB_USERNAME=local
SECRET_KEY=local-secret-key-for-development
DB_USER=innovsurf
DB_PASSWORD=innovsurf2024
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

echo "📋 Fichier .env.local créé"

# Démarrer les services localement
echo "🐳 Démarrage des services Docker..."
docker-compose up -d

echo "⏳ Attente du démarrage des services..."
sleep 30

echo "✅ Déploiement local terminé !"
echo "🌐 Votre site est disponible sur :"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend: http://localhost:8000"
echo "   - PhpMyAdmin: http://localhost:8080"
echo ""
echo "📊 Commandes utiles :"
echo "   - Voir les logs: docker-compose logs -f"
echo "   - Arrêter: docker-compose down"
echo "   - Redémarrer: docker-compose restart"
