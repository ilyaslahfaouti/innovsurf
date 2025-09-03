#!/bin/bash

# Script de déploiement InnovSurf sur AWS
set -e

echo "🚀 Déploiement InnovSurf sur AWS"

# Variables
DOCKERHUB_USERNAME=${DOCKERHUB_USERNAME:-"your_dockerhub_username"}
AWS_REGION=${AWS_REGION:-"us-east-1"}
INSTANCE_TYPE=${INSTANCE_TYPE:-"t2.micro"}
KEY_NAME=${KEY_NAME:-"innovsurf-key"}

# Vérifier que AWS CLI est configuré
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI n'est pas configuré. Exécutez 'aws configure' d'abord."
    exit 1
fi

# Vérifier que Docker fonctionne
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas démarré. Démarrez Docker Desktop."
    exit 1
fi

echo "📦 Construction des images Docker..."

# Build et push des images
docker build -t $DOCKERHUB_USERNAME/innovsurf-backend:latest ./backend
docker build -t $DOCKERHUB_USERNAME/innovsurf-frontend:latest ./frontend

echo "🔐 Connexion à Docker Hub..."
docker login

echo "📤 Push des images vers Docker Hub..."
docker push $DOCKERHUB_USERNAME/innovsurf-backend:latest
docker push $DOCKERHUB_USERNAME/innovsurf-frontend:latest

echo "🔑 Création d'une paire de clés SSH..."
aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > ~/.ssh/$KEY_NAME.pem
chmod 400 ~/.ssh/$KEY_NAME.pem

echo "🖥️  Création de l'instance EC2..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-groups innovsurf-sg \
    --user-data file://user-data.sh \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "⏳ Attente du démarrage de l'instance..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Obtenir l'IP publique
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "🌐 Instance créée avec l'IP: $PUBLIC_IP"
echo "🔗 Connectez-vous avec: ssh -i ~/.ssh/$KEY_NAME.pem ubuntu@$PUBLIC_IP"

# Créer le fichier .env de production
cat > .env.prod << EOF
DOCKERHUB_USERNAME=$DOCKERHUB_USERNAME
SECRET_KEY=$(openssl rand -base64 32)
DB_USER=innovsurf
DB_PASSWORD=$(openssl rand -base64 16)
ALLOWED_HOSTS=$PUBLIC_IP
EOF

echo "📋 Fichier .env.prod créé"
echo "✅ Déploiement terminé !"
echo "🌐 Votre site sera disponible sur: http://$PUBLIC_IP"
