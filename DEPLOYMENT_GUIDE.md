# Guide de Déploiement InnovSurf sur AWS

## 🚀 Déploiement Automatique

### Prérequis
1. **Compte AWS** avec accès gratuit (12 mois)
2. **Docker Hub** compte
3. **GitHub** repository

### Étapes de Déploiement

#### 1. Configuration AWS
```bash
# Installer AWS CLI (déjà fait)
aws configure
# Entrez vos clés d'accès AWS
```

#### 2. Créer un Security Group
```bash
# Créer un security group pour l'instance
aws ec2 create-security-group \
    --group-name innovsurf-sg \
    --description "Security group for InnovSurf"

# Ouvrir les ports nécessaires
aws ec2 authorize-security-group-ingress \
    --group-name innovsurf-sg \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-name innovsurf-sg \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-name innovsurf-sg \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0
```

#### 3. Configuration Docker Hub
1. Créez un compte sur [Docker Hub](https://hub.docker.com)
2. Notez votre nom d'utilisateur
3. Créez un token d'accès

#### 4. Déploiement Automatique
```bash
# Modifier le nom d'utilisateur Docker Hub
export DOCKERHUB_USERNAME=votre_nom_utilisateur

# Lancer le déploiement
./deploy-aws.sh
```

#### 5. Configuration GitHub Actions (Optionnel)
1. Allez dans Settings > Secrets and variables > Actions
2. Ajoutez ces secrets :
   - `DOCKERHUB_USERNAME` : votre nom d'utilisateur Docker Hub
   - `DOCKERHUB_TOKEN` : votre token Docker Hub
   - `AWS_HOST` : IP de votre instance EC2
   - `AWS_SSH_KEY` : contenu de votre clé SSH privée

## 🔧 Déploiement Manuel

### 1. Créer l'instance EC2
```bash
# Créer une instance Ubuntu 22.04
aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --count 1 \
    --instance-type t2.micro \
    --key-name innovsurf-key \
    --security-groups innovsurf-sg
```

### 2. Se connecter à l'instance
```bash
ssh -i ~/.ssh/innovsurf-key.pem ubuntu@IP_DE_VOTRE_INSTANCE
```

### 3. Installer Docker
```bash
# Sur l'instance EC2
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker ubuntu
```

### 4. Cloner et déployer
```bash
git clone https://github.com/ilyaslahfaouti/innovsurf.git
cd innovsurf

# Créer le fichier .env.prod
cp env.prod.example .env.prod
# Modifier les valeurs dans .env.prod

# Démarrer les services
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

## 🌐 Configuration HTTPS (Optionnel)

### Avec Let's Encrypt
```bash
# Installer Certbot
sudo apt install certbot

# Obtenir un certificat
sudo certbot certonly --standalone -d votre-domaine.com

# Copier les certificats
sudo cp /etc/letsencrypt/live/votre-domaine.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/votre-domaine.com/privkey.pem ./ssl/key.pem
```

## 📊 Monitoring

### Vérifier les logs
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### Redémarrer les services
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Mettre à jour
```bash
git pull origin main
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## 💰 Coûts AWS

- **EC2 t2.micro** : Gratuit pendant 12 mois (750h/mois)
- **Stockage EBS** : 30GB gratuit
- **Transfert de données** : 1GB/mois gratuit

## 🔒 Sécurité

1. **Changez les mots de passe par défaut**
2. **Configurez un firewall**
3. **Utilisez HTTPS**
4. **Sauvegardez régulièrement**

## 🆘 Dépannage

### Problèmes courants
1. **Port 80/443 fermé** : Vérifiez le security group
2. **Docker ne démarre pas** : Vérifiez les logs
3. **Base de données inaccessible** : Vérifiez les variables d'environnement

### Commandes utiles
```bash
# Vérifier le statut des conteneurs
docker ps

# Voir les logs
docker logs innovsurf_backend
docker logs innovsurf_frontend

# Redémarrer un service
docker restart innovsurf_backend
```
