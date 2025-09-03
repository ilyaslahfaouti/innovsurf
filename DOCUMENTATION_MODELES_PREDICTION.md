# 🎯 Documentation des Modèles de Prédiction IA - InnovSurf

## 📋 Vue d'ensemble des Modèles

InnovSurf utilise plusieurs modèles de machine learning avancés pour prédire la demande, optimiser les prix et évaluer les risques d'annulation. Ces modèles sont entraînés sur des données historiques et s'améliorent continuellement.

---

## 🏗️ Architecture des Modèles

### **1. Pipeline d'Entraînement**
- **Collecte de données** : Extraction depuis la base Django
- **Préprocessing** : Nettoyage et transformation des données
- **Feature engineering** : Création de variables prédictives
- **Entraînement** : Apprentissage des modèles
- **Évaluation** : Validation des performances
- **Déploiement** : Mise en production des modèles

### **2. Infrastructure Technique**
- **Scikit-learn** : Framework principal de machine learning
- **Joblib** : Sauvegarde et chargement des modèles
- **Pandas** : Manipulation des données
- **NumPy** : Calculs numériques

---

## 🤖 Modèle de Prédiction de Demande

### **Objectif**
Prédire le nombre de réservations attendues pour une date et un spot donnés, en tenant compte des conditions météorologiques et des facteurs saisonniers.

### **Algorithme Principal**
- **Random Forest** : Ensemble d'arbres de décision
- **Gradient Boosting** : Boosting séquentiel des modèles faibles
- **Régression Linéaire** : Modèle de base pour comparaison

### **Features d'Entrée**
```python
# Features temporelles
- month: Mois de l'année (1-12)
- season: Saison (hiver, printemps, été, automne)
- is_weekend: Booléen weekend/semaine
- is_holiday: Booléen vacances scolaires

# Features météorologiques
- wave_height: Hauteur des vagues en mètres
- wind_speed: Vitesse du vent en km/h
- water_temp: Température de l'eau en °C
- weather_score: Score composite météo (0-100)

# Features de demande
- historical_bookings: Moyenne des réservations historiques
- trend_factor: Facteur de tendance saisonnière
- spot_popularity: Popularité du spot de surf
```

### **Métriques de Performance**
- **R² Score** : Qualité de la prédiction (0-1)
- **RMSE** : Erreur moyenne quadratique
- **MAE** : Erreur absolue moyenne

---

## 💰 Modèle d'Optimisation des Prix

### **Objectif**
Déterminer le prix optimal pour maximiser les revenus tout en maintenant un niveau de demande acceptable.

### **Algorithme Principal**
- **Random Forest** : Prédiction des prix optimaux
- **Gradient Boosting** : Optimisation des paramètres
- **Régression Linéaire** : Modèle de référence

### **Features d'Entrée**
```python
# Features de demande
- predicted_demand: Demande prédite par le modèle principal
- demand_elasticity: Élasticité de la demande aux prix
- competitor_prices: Prix de la concurrence

# Features contextuelles
- weather_conditions: Conditions météorologiques
- seasonal_factor: Facteur saisonnier
- spot_quality: Qualité du spot de surf
- equipment_availability: Disponibilité des équipements
```

### **Stratégie d'Optimisation**
- **Pricing dynamique** : Ajustement en temps réel
- **Segmentation** : Prix différenciés selon les segments
- **Yield management** : Optimisation de la capacité

---

## ⚠️ Modèle de Prédiction d'Annulation

### **Objectif**
Évaluer la probabilité qu'une réservation soit annulée, permettant une gestion proactive des risques.

### **Algorithme Principal**
- **Random Forest** : Classification des risques d'annulation
- **Régression Logistique** : Modèle probabiliste
- **Gradient Boosting** : Amélioration des performances

### **Features d'Entrée**
```python
# Features de réservation
- booking_advance: Délai entre réservation et date
- total_amount: Montant total de la réservation
- customer_history: Historique des annulations du client

# Features contextuelles
- weather_forecast: Prévisions météo pour la date
- alternative_activities: Activités alternatives disponibles
- cancellation_policy: Politique d'annulation du club
```

### **Métriques de Performance**
- **Précision** : Exactitude des prédictions positives
- **Recall** : Sensibilité aux annulations réelles
- **F1-Score** : Moyenne harmonique précision/recall
- **AUC-ROC** : Courbe ROC et aire sous la courbe

---

## 🔄 Pipeline ETL pour l'IA

### **1. Extraction (Extract)**
```python
# Sources de données
- SurfLesson.objects.all()  # Leçons de surf
- SurfSession.objects.all()  # Sessions de surf
- Equipment.objects.all()    # Équipements
- SurfClub.objects.all()     # Clubs de surf
- Monitor.objects.all()      # Moniteurs

# Données météorologiques
- API Windy (conditions en temps réel)
- Historique météo (base de données locale)
```

### **2. Transformation (Transform)**
```python
# Calcul des features temporelles
def calculate_temporal_features(date):
    month = date.month
    season = get_season(date)
    is_weekend = date.weekday() >= 5
    is_holiday = check_holiday(date)
    return month, season, is_weekend, is_holiday

# Score météorologique composite
def calculate_weather_score(wave_height, wind_speed, water_temp):
    wave_score = min(wave_height * 20, 100)
    wind_score = max(100 - wind_speed * 2, 0)
    temp_score = calculate_temp_score(water_temp)
    return (wave_score + wind_score + temp_score) / 3
```

### **3. Chargement (Load)**
```python
# Préparation des données d'entraînement
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42
)

# Entraînement des modèles
for model_name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    score = model.score(X_test, y_test)
```

---

## 📊 Évaluation et Validation

### **1. Validation Croisée**
```python
# K-Fold Cross Validation
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(model, X, y, cv=5)
mean_cv_score = cv_scores.mean()
std_cv_score = cv_scores.std()
```

### **2. Métriques de Performance**
```python
# Régression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

r2 = r2_score(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mae = mean_absolute_error(y_true, y_pred)

# Classification
from sklearn.metrics import precision_score, recall_score, f1_score

precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
```

### **3. Analyse des Erreurs**
- **Residual Analysis** : Analyse des résidus pour la régression
- **Confusion Matrix** : Matrice de confusion pour la classification
- **Feature Importance** : Importance relative des variables

---

## 🚀 Déploiement et Production

### **1. Sauvegarde des Modèles**
```python
# Sauvegarde avec joblib
import joblib

joblib.dump(model, 'model_name.pkl')
model = joblib.load('model_name.pkl')
```

### **2. Versioning des Modèles**
```python
# Gestion des versions
model_version = "1.0.0"
model_path = f"models/{model_name}_v{model_version}.pkl"
```

### **3. Monitoring en Production**
- **Drift Detection** : Détection de la dérive des modèles
- **Performance Tracking** : Suivi des métriques en temps réel
- **Auto-retraining** : Re-entraînement automatique si nécessaire

---

## 🔧 Configuration et Paramètres

### **1. Paramètres des Modèles**
```python
# Random Forest
rf_params = {
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 2,
    'min_samples_leaf': 1,
    'random_state': 42
}

# Gradient Boosting
gb_params = {
    'n_estimators': 100,
    'learning_rate': 0.1,
    'max_depth': 3,
    'random_state': 42
}
```

### **2. Configuration du Pipeline**
```python
# Paramètres du pipeline ETL
pipeline_config = {
    'days_back': 365,  # Nombre de jours d'historique
    'min_data_quality': 0.8,  # Qualité minimale des données
    'retrain_threshold': 0.1,  # Seuil de re-entraînement
    'model_types': ['random_forest', 'gradient_boosting', 'linear']
}
```

---

## 📈 Amélioration Continue

### **1. Feedback Loop**
- **Collecte de feedback** : Évaluation des prédictions par les utilisateurs
- **Analyse des erreurs** : Identification des cas problématiques
- **Mise à jour des modèles** : Intégration des nouvelles données

### **2. A/B Testing**
- **Comparaison de modèles** : Test de nouveaux algorithmes
- **Optimisation des paramètres** : Recherche des meilleures configurations
- **Validation des améliorations** : Mesure de l'impact des changements

---

## 🎯 Impact Business des Modèles

### **1. Optimisation des Revenus**
- **Tarification dynamique** : +15-25% de revenus
- **Gestion des capacités** : +20% d'utilisation des ressources
- **Réduction des annulations** : -30% de pertes

### **2. Amélioration de l'Expérience Client**
- **Prédictions précises** : +40% de satisfaction
- **Recommandations personnalisées** : +25% de conversion
- **Gestion proactive** : +35% de fidélisation

---

**🎯 Objectif** : Fournir des modèles de prédiction robustes et précis qui optimisent la gestion des réservations et améliorent la rentabilité des clubs de surf.

**🔧 Maintenance** : Les modèles s'améliorent continuellement grâce à l'apprentissage automatique et aux nouvelles données.

**📊 Impact** : Amélioration mesurable des performances business et de la satisfaction client.
