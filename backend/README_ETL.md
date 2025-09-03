# 🚀 Pipeline ETL - Système de Prédiction des Réservations InnovSurf

## 📋 Vue d'ensemble

Ce système implémente un pipeline ETL (Extract, Transform, Load) complet pour l'analyse prédictive des réservations de surf. Il utilise l'intelligence artificielle pour prédire la demande, optimiser les prix et évaluer les risques d'annulation.

## 🏗️ Architecture du Pipeline

### 1. **EXTRACT** 📥
- Récupération des données de réservation depuis la base Django
- Sources de données :
  - `SurfLesson` : Leçons de surf
  - `SurfSession` : Sessions de surf
  - `Equipment` : Locations d'équipement
  - `SurfClub` : Informations sur les clubs
  - `Monitor` : Données des moniteurs

### 2. **TRANSFORM** 🔄
- Transformation des données brutes en features d'IA
- Calcul des facteurs de demande :
  - Saisonnalité (hiver, printemps, été, automne)
  - Facteurs weekend et vacances
  - Score météo (vagues, vent, température)
  - Niveau de surf et expérience

### 3. **LOAD** 📤
- Chargement des données transformées
- Vérification de la qualité des données
- Préparation pour l'entraînement des modèles

## 🤖 Modèles IA

### Modèle de Prédiction de Demande
- **Algorithme** : Random Forest, Gradient Boosting, Régression Linéaire
- **Prédit** : Nombre de réservations attendues
- **Features** : Météo, saison, weekend, vacances

### Modèle d'Optimisation des Prix
- **Algorithme** : Random Forest, Gradient Boosting, Régression Linéaire
- **Prédit** : Prix optimal pour maximiser les revenus
- **Features** : Demande prédite, conditions météo, saison

### Modèle de Prédiction d'Annulation
- **Algorithme** : Random Forest, Régression Logistique
- **Prédit** : Probabilité d'annulation d'une réservation
- **Features** : Conditions météo, prix, demande

## 🚀 Utilisation Rapide

### 1. Démarrage Automatique
```bash
cd backend/
./start_etl_pipeline.sh
```

### 2. Test Manuel
```bash
cd backend/
python test_etl_pipeline.py
```

### 3. Utilisation dans le Code
```python
from AppWeb.booking_prediction import BookingPredictionSystem

# Créer une instance
system = BookingPredictionSystem()

# Exécuter le pipeline ETL complet
result = system.run_full_etl_pipeline(days_back=365)

# Faire des prédictions
future_date = datetime.now() + timedelta(days=7)
weather = {'wave_height': 2.5, 'wind_speed': 12, 'water_temp': 24}

# Prédire la demande
demand = system.predict_demand(future_date, weather, 'Taghazout')

# Optimiser le prix
price = system.optimize_price(future_date, weather, 100)
```

## 📊 Fonctionnalités Avancées

### Analyse des Tendances
- Détection des patterns saisonniers
- Analyse des facteurs météorologiques
- Identification des pics de demande

### Optimisation Dynamique
- Ajustement des prix en temps réel
- Recommandations de tarification
- Stratégies de réduction des annulations

### Intégration Météo
- Données en temps réel via API Windy
- Historique météorologique
- Score de qualité des conditions

## 🔧 Configuration

### Variables d'Environnement
```bash
# Base de données Django
DJANGO_SETTINGS_MODULE=innovsurf.settings

# API Windy (optionnel)
WINDY_API_KEY=your_api_key_here
```

### Paramètres du Pipeline
```python
# Nombre de jours de données historiques
days_back = 730  # 2 ans par défaut

# Types de modèles
model_types = ['random_forest', 'gradient_boosting', 'linear']

# Seuils de qualité des données
min_data_quality = 0.8
```

## 📈 Métriques et Performance

### Métriques d'Entraînement
- **R² Score** : Qualité de la prédiction
- **RMSE** : Erreur moyenne quadratique
- **Précision** : Pour les modèles de classification

### Surveillance Continue
- Vérification automatique de la qualité des données
- Détection des dérives de modèles
- Re-entraînement automatique si nécessaire

## 🚨 Dépannage

### Erreurs Communes

#### 1. Base de Données
```bash
# Vérifier la connexion
python manage.py check --database default

# Appliquer les migrations
python manage.py migrate
```

#### 2. Dépendances
```bash
# Installer les packages IA
pip install -r requirements_ai.txt

# Vérifier scikit-learn
python -c "import sklearn; print(sklearn.__version__)"
```

#### 3. Modèles Non Entraînés
```python
# Vérifier le statut
status = system.get_system_status()
print(f"Modèles entraînés: {status}")

# Forcer l'entraînement
system.run_full_etl_pipeline()
```

## 🔮 Développements Futurs

### Fonctionnalités Prévues
- [ ] Interface web de visualisation
- [ ] API REST pour les prédictions
- [ ] Intégration avec d'autres sources météo
- [ ] Modèles de deep learning
- [ ] Prédictions multi-spots

### Optimisations
- [ ] Cache des prédictions
- [ ] Entraînement incrémental
- [ ] Parallélisation des calculs
- [ ] Compression des modèles

## 📚 Documentation Technique

### Structure des Données
```python
# Format des données transformées
{
    'id': int,
    'booking_date': str,  # ISO format
    'month': int,
    'season': str,
    'weather_score': float,
    'predicted_demand': float,
    'actual_bookings': int,
    'optimized_price': float,
    'cancellation_probability': float
}
```

### API des Modèles
```python
# Interface commune pour tous les modèles
class PredictionModel:
    def train(self, X, y) -> Dict
    def predict(self, X) -> np.ndarray
    def evaluate(self, X, y) -> Dict
    def save(self, path: str) -> bool
    def load(self, path: str) -> bool
```

## 🤝 Contribution

### Ajout de Nouveaux Modèles
1. Créer une classe héritant de `PredictionModel`
2. Implémenter les méthodes requises
3. Ajouter au dictionnaire `self.models`
4. Tester avec `test_etl_pipeline.py`

### Amélioration des Features
1. Modifier `_prepare_prediction_features()`
2. Ajouter la logique de transformation
3. Mettre à jour la documentation
4. Ajouter des tests unitaires

---

**🎯 Objectif** : Fournir un système de prédiction robuste et évolutif pour optimiser la gestion des réservations de surf.

**🔧 Maintenance** : Le système s'auto-optimise et se re-entraîne automatiquement avec de nouvelles données.

**📊 Impact** : Amélioration de la rentabilité et de la satisfaction client grâce à une tarification intelligente et une gestion proactive des risques.
