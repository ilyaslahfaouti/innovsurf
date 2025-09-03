#!/bin/bash

# Script de démarrage du pipeline ETL de prédiction des réservations
# InnovSurf - Système IA de prédiction

echo "🚀 DÉMARRAGE DU PIPELINE ETL INNOVSURF"
echo "======================================"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis le répertoire backend/"
    echo "📁 Répertoire actuel: $(pwd)"
    echo "🔄 Veuillez naviguer vers backend/ et réessayer"
    exit 1
fi

# Vérifier l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "⚠️  Environnement virtuel non trouvé. Création..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
if [ ! -f "requirements_ai.txt" ]; then
    echo "⚠️  Fichier requirements_ai.txt non trouvé, utilisation de requirements.txt"
    pip install -r requirements.txt
else
    pip install -r requirements_ai.txt
fi

# Vérifier la base de données
echo "🗄️  Vérification de la base de données..."
python manage.py check --database default

if [ $? -ne 0 ]; then
    echo "❌ Problème avec la base de données. Vérification des migrations..."
    python manage.py migrate
fi

# Lancer le pipeline ETL
echo "🧪 Lancement du pipeline ETL..."
echo "📊 Extraction des données de réservation..."
echo "🔄 Transformation des données..."
echo "📥 Chargement et entraînement des modèles IA..."

python test_etl_pipeline.py

# Vérifier le résultat
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ PIPELINE ETL TERMINÉ AVEC SUCCÈS!"
    echo "🎯 Le système de prédiction est maintenant opérationnel"
    echo ""
    echo "📈 Fonctionnalités disponibles:"
    echo "   - Prédiction de la demande de réservations"
    echo "   - Optimisation dynamique des prix"
    echo "   - Prédiction des risques d'annulation"
    echo "   - Analyse des tendances saisonnières"
    echo ""
    echo "🔮 Pour tester les prédictions:"
    echo "   python -c \"from AppWeb.booking_prediction import *; test_predictions(BookingPredictionSystem())\""
else
    echo ""
    echo "❌ ERREUR DANS LE PIPELINE ETL"
    echo "🔍 Vérifiez les logs pour plus de détails"
    echo ""
    echo "💡 Solutions possibles:"
    echo "   - Vérifiez la connexion à la base de données"
    echo "   - Assurez-vous que les modèles Django sont corrects"
    echo "   - Vérifiez les permissions des fichiers"
fi

# Désactiver l'environnement virtuel
deactivate

echo ""
echo "🏁 Script terminé"
