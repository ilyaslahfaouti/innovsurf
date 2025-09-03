#!/bin/bash

# Script d'initialisation pour l'instance EC2
set -e

# Mise à jour du système
apt-get update
apt-get upgrade -y

# Installation de Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu

# Installation de Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Installation de Git
apt-get install -y git

# Cloner le repository
cd /home/ubuntu
git clone https://github.com/ilyaslahfaouti/innovsurf.git
cd innovsurf

# Créer le fichier .env de production
cat > .env.prod << EOF
DOCKERHUB_USERNAME=your_dockerhub_username
SECRET_KEY=change-this-secret-key
DB_USER=innovsurf
DB_PASSWORD=innovsurf2024
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

# Démarrer les services
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

# Configurer le redémarrage automatique
echo "@reboot cd /home/ubuntu/innovsurf && docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d" | crontab -

echo "✅ Installation terminée !"
