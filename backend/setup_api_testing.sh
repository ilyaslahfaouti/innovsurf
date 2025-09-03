#!/bin/bash

echo "🚀 Configuration des outils de test des APIs InnovSurf"
echo "=================================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Python3 détecté: $(python3 --version)"

# Vérifier si pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ pip3 détecté: $(pip3 --version)"

# Créer un environnement virtuel si nécessaire
if [ ! -d "venv_api_testing" ]; then
    echo "🔧 Création d'un environnement virtuel..."
    python3 -m venv venv_api_testing
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv_api_testing/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install requests pillow matplotlib numpy

echo "✅ Dépendances installées avec succès!"

# Vérifier que le serveur Django est accessible
echo "🔍 Vérification de l'accessibilité du serveur..."
if curl -s http://localhost:8000/api/ > /dev/null; then
    echo "✅ Serveur Django accessible sur http://localhost:8000"
else
    echo "⚠️  Serveur Django non accessible sur http://localhost:8000"
    echo "   Assurez-vous que votre serveur Django est démarré"
    echo "   Vous pouvez le démarrer avec: python manage.py runserver"
fi

echo ""
echo "🎯 Outils disponibles:"
echo "   1. Test simple: python3 simple_api_tester.py"
echo "   2. Test complet: python3 api_screenshot_tool.py"
echo "   3. Test forecast: python3 test_forecast_api.py"
echo ""
echo "💡 Pour commencer, lancez: python3 simple_api_tester.py"

# Désactiver l'environnement virtuel
deactivate
