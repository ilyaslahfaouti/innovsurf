# 🌊 YalaSurf - Plateforme de Surf au Maroc

YalaSurf est une plateforme complète de gestion de surf clubs et de réservation de cours de surf au Maroc, développée avec Django (backend) et React (frontend).

## 🚀 Fonctionnalités

### Pour les Surf Clubs
- Gestion des profils et informations
- Gestion des moniteurs et équipements
- Planification des cours et sessions
- Suivi des réservations et statistiques
- Gestion des équipements (location/vente)

### Pour les Surfeurs
- Inscription et gestion de profil
- Réservation de cours de surf
- Achat et location d'équipements
- Consultation des spots de surf
- Prévisions météo des spots
- Forum communautaire

## 🛠️ Technologies Utilisées

### Backend
- **Django 4.1.13** - Framework web Python
- **Django REST Framework** - API REST
- **SQLite** - Base de données
- **JWT Authentication** - Authentification sécurisée
- **Pillow** - Gestion des images
- **CORS** - Support cross-origin

### Frontend
- **React 18.3.1** - Interface utilisateur
- **React Router** - Navigation
- **Axios** - Requêtes HTTP
- **Bootstrap 5.3.3** - Styling
- **FontAwesome** - Icônes

## 📁 Structure du Projet

```
YalaSurf/
├── backend/                 # API Django
│   ├── AppWeb/             # Application principale
│   │   ├── models.py       # Modèles de données
│   │   ├── views.py        # Vues API
│   │   ├── serializer.py   # Sérialiseurs DRF
│   │   └── urls.py         # Routes API
│   ├── yalasurf/           # Configuration Django
│   └── requirements.txt    # Dépendances Python
├── frontend/               # Application React
│   ├── src/                # Code source
│   │   ├── components/     # Composants réutilisables
│   │   ├── pages/          # Pages de l'application
│   │   └── context/        # Contexte React
│   └── package.json        # Dépendances Node.js
└── docker-compose.yml      # Configuration Docker
```

## 🚀 Installation et Lancement

### Prérequis
- Python 3.8+
- Node.js 16+
- npm ou yarn

### Backend Django

1. **Créer l'environnement virtuel**
   ```bash
   cd YalaSurf/backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements_fixed.txt
   ```

3. **Effectuer les migrations**
   ```bash
   python manage.py migrate
   ```

4. **Lancer le serveur**
   ```bash
   python manage.py runserver 8001
   ```

Le backend sera accessible sur `http://localhost:8001`

### Frontend React

1. **Installer les dépendances**
   ```bash
   cd YalaSurf/frontend
   npm install
   ```

2. **Lancer le serveur de développement**
   ```bash
   npm start
   ```

Le frontend sera accessible sur `http://localhost:3000`

## 🔧 Configuration

### Variables d'environnement

Créer un fichier `.env` dans le dossier backend :

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
STORMGLASS_API_KEY=your-api-key
```

### Base de données

Le projet utilise SQLite par défaut. Pour utiliser PostgreSQL ou MySQL, modifier `settings.py`.

## 📚 API Endpoints

### Authentification
- `POST /api/user/register/` - Inscription utilisateur
- `POST /api/user/login/` - Connexion utilisateur
- `POST /api/token/` - Obtenir un token JWT

### Surf Clubs
- `GET /api/surf-club/profile/` - Profil du surf club
- `GET /api/surf-club/monitors/` - Liste des moniteurs
- `GET /api/surf-club/equipments/` - Liste des équipements
- `POST /api/surf-club/add-monitor/` - Ajouter un moniteur

### Surfeurs
- `GET /api/surfer/profile/` - Profil du surfeur
- `POST /api/surfers/book_surf_lesson/` - Réserver un cours
- `POST /api/surfers/add-order/` - Passer une commande

### Spots de Surf
- `GET /api/surf-spots/` - Liste des spots
- `GET /api/surf-spots/{id}/` - Détails d'un spot
- `GET /api/surf-spots/prevision/{id}/` - Prévisions météo

## 🐳 Docker

Pour lancer avec Docker :

```bash
docker-compose up --build
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- Développé pour la communauté surf du Maroc
- Projet académique et communautaire

## 🙏 Remerciements

- Communauté Django
- Communauté React
- Surfers du Maroc
- Moniteurs et écoles de surf

---

**YalaSurf** - Connecter la communauté surf du Maroc ! 🏄‍♂️🇲🇦
