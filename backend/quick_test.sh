#!/bin/bash

echo "🚀 Testeur Rapide des APIs InnovSurf"
echo "====================================="

# Activer l'environnement virtuel
if [ -d "venv_api_testing" ]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source venv_api_testing/bin/activate
else
    echo "❌ Environnement virtuel non trouvé. Exécutez d'abord: ./setup_api_testing.sh"
    exit 1
fi

# Menu de sélection
echo ""
echo "🎯 Choisissez votre outil de test:"
echo "1. Test simple (rapide) - simple_api_tester.py"
echo "2. Test complet avec captures - api_screenshot_tool.py"
echo "3. Test spécialisé forecast - test_forecast_api.py"
echo "4. Test intelligent (recommandé) - smart_api_tester.py"
echo "5. Test avec authentification corrigée - fix_auth.py ⭐"
echo "6. Tous les tests"
echo "7. Configurer utilisateur de test"
echo "8. Quitter"
echo ""

read -p "Votre choix (1-8): " choice

case $choice in
    1)
        echo "🚀 Lancement du test simple..."
        python3 simple_api_tester.py
        ;;
    2)
        echo "🖼️  Lancement du test complet avec captures..."
        python3 api_screenshot_tool.py
        ;;
    3)
        echo "🌊 Lancement du test forecast..."
        python3 test_forecast_api.py
        ;;
    4)
        echo "🧠 Lancement du test intelligent..."
        python3 smart_api_tester.py
        ;;
    5)
        echo "🔧 Lancement du test avec authentification corrigée..."
        python3 fix_auth.py
        ;;
    6)
        echo "🎯 Lancement de tous les tests..."
        echo ""
        echo "=== TEST SIMPLE ==="
        python3 simple_api_tester.py
        echo ""
        echo "=== TEST COMPLET ==="
        python3 api_screenshot_tool.py
        echo ""
        echo "=== TEST FORECAST ==="
        python3 test_forecast_api.py
        echo ""
        echo "=== TEST INTELLIGENT ==="
        python3 smart_api_tester.py
        echo ""
        echo "=== TEST AUTH CORRIGÉE ==="
        python3 fix_auth.py
        echo ""
        echo "🎉 Tous les tests sont terminés !"
        ;;
    7)
        echo "🔧 Configuration de l'utilisateur de test..."
        python3 setup_test_user.py
        ;;
    8)
        echo "👋 Au revoir !"
        exit 0
        ;;
    *)
        echo "❌ Choix invalide. Veuillez sélectionner 1-8."
        exit 1
        ;;
esac

# Désactiver l'environnement virtuel
deactivate

echo ""
echo "📁 Résultats disponibles dans:"
echo "   - api_screenshots/ (test complet)"
echo "   - forecast_screenshots/ (test forecast)"
echo "   - *.md et *.json (test simple)"
echo ""
echo "🔍 Pour voir les captures d'écran:"
echo "   open api_screenshots/"
echo "   open forecast_screenshots/"
