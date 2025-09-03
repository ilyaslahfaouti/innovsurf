# 🖼️ Guide de Test des APIs InnovSurf avec Captures d'Écran

Ce guide vous explique comment tester vos APIs et générer des captures d'écran automatiquement.

## 🚀 Installation Rapide

### Option 1: Script automatique (Recommandé)
```bash
cd backend
chmod +x setup_api_testing.sh
./setup_api_testing.sh
```

### Option 2: Installation manuelle
```bash
cd backend
python3 -m venv venv_api_testing
source venv_api_testing/bin/activate
pip install requests pillow matplotlib numpy
```

## 🎯 Outils Disponibles

### 1. Test Simple (`simple_api_tester.py`)
**Pour des tests rapides de toutes les APIs**
```bash
python3 simple_api_tester.py
```

**Fonctionnalités:**
- ✅ Test de tous les endpoints principaux
- ✅ Génération de rapports Markdown
- ✅ Sauvegarde des résultats JSON
- ✅ Tests GET et POST
- ⚡ Rapide et simple

### 2. Test Complet (`api_screenshot_tool.py`)
**Pour des tests approfondis avec captures d'écran**
```bash
python3 api_screenshot_tool.py
```

**Fonctionnalités:**
- 🖼️ Captures d'écran automatiques
- 📊 Graphiques de performance
- 📄 Rapports détaillés
- 🔐 Tests d'authentification
- 📁 Organisation des résultats

### 3. Test Forecast (`test_forecast_api.py`)
**Spécialisé pour l'API de prévisions météo**
```bash
python3 test_forecast_api.py
```

**Fonctionnalités:**
- 🌊 Tests spécifiques aux prévisions
- 📈 Graphiques météorologiques
- 🏄 Tests par spot de surf
- 📸 Captures des données JSON
- 📊 Analyse des quotas API

## 📋 Endpoints Testés

| Endpoint | Description | Méthodes |
|----------|-------------|----------|
| `/api/surf-spots/` | Liste des spots de surf | GET |
| `/api/surf-spots/{id}/` | Détail d'un spot | GET |
| `/api/surf-spots/prevision/{id}/` | Prévisions météo | GET |
| `/api/surf-clubs/` | Clubs de surf | GET |
| `/api/lessons/` | Leçons de surf | GET, POST |
| `/api/bookings/` | Réservations | GET, POST |
| `/api/users/` | Utilisateurs | GET |
| `/api/chatbot/` | Chatbot IA | GET |
| `/api/analytics/dashboard/` | Tableau de bord | GET |
| `/api/recommendations/` | Recommandations | GET |

## 🖼️ Types de Captures d'Écran

### 1. Captures de Données
- **Format:** PNG haute résolution
- **Contenu:** Données JSON formatées
- **Utilisation:** Documentation, debugging

### 2. Graphiques Météorologiques
- **Format:** PNG haute résolution (300 DPI)
- **Contenu:** Évolution des vagues, température
- **Utilisation:** Présentations, rapports

### 3. Captures de Performance
- **Format:** PNG avec métriques
- **Contenu:** Temps de réponse, statuts
- **Utilisation:** Monitoring, optimisation

## 📁 Structure des Résultats

```
backend/
├── api_screenshots/          # Outil complet
│   ├── api_screenshot_*.png
│   ├── api_test_results_*.json
│   └── api_report_*.md
├── forecast_screenshots/      # Test forecast
│   ├── forecast_chart_*.png
│   ├── forecast_data_*.png
│   └── forecast_test_report_*.md
├── simple_api_report_*.md    # Test simple
└── simple_api_results_*.json
```

## 🔧 Configuration

### Variables d'environnement
```bash
export INNOVSURF_API_URL="http://localhost:8000"
export INNOVSURF_USERNAME="admin"
export INNOVSURF_PASSWORD="admin"
```

### Personnalisation des tests
```python
# Dans les scripts, modifiez ces variables
BASE_URL = "http://localhost:8000"  # URL de votre serveur
API_ENDPOINTS = {
    # Ajoutez vos endpoints personnalisés
    "custom_api": "/api/custom/",
}
```

## 🚨 Dépannage

### Erreur: "Serveur non accessible"
```bash
# Vérifiez que votre serveur Django est démarré
cd backend
python manage.py runserver
```

### Erreur: "Module not found"
```bash
# Activez l'environnement virtuel
source venv_api_testing/bin/activate
pip install -r requirements.txt
```

### Erreur: "Permission denied"
```bash
# Rendez le script exécutable
chmod +x setup_api_testing.sh
```

## 📊 Exemples de Sortie

### Rapport Markdown
```markdown
# Rapport de Test des APIs InnovSurf

**Date:** 2024-12-25 14:30:00

## Résumé
- **Total des tests:** 12
- **Tests réussis:** 10 ✅
- **Tests échoués:** 2 ❌
- **Taux de succès:** 83.3%
```

### Résultats JSON
```json
{
  "name": "Prévisions",
  "url": "http://localhost:8000/api/surf-spots/prevision/1/",
  "method": "GET",
  "status_code": 200,
  "success": true,
  "response_time": 0.85,
  "data_size": 2048
}
```

## 🎨 Personnalisation Avancée

### Ajouter de nouveaux endpoints
```python
# Dans api_screenshot_tool.py
API_ENDPOINTS = {
    # ... endpoints existants ...
    "nouvelle_api": "/api/nouvelle/",
    "autre_endpoint": "/api/autre/",
}
```

### Modifier les tests POST
```python
# Ajouter des tests personnalisés
post_tests = [
    # ... tests existants ...
    ("test_personnalise", "/api/custom/", {
        "param1": "valeur1",
        "param2": "valeur2"
    })
]
```

### Personnaliser les graphiques
```python
# Dans test_forecast_api.py
plt.style.use('seaborn')  # Style de graphique
plt.rcParams['figure.figsize'] = (15, 10)  # Taille personnalisée
```

## 🔍 Surveillance Continue

### Test automatique toutes les heures
```bash
# Ajouter au crontab
0 * * * * cd /path/to/innovsurf/backend && python3 simple_api_tester.py
```

### Intégration CI/CD
```yaml
# .github/workflows/api-testing.yml
name: API Testing
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test APIs
        run: |
          cd backend
          python3 simple_api_tester.py
```

## 📞 Support

### Problèmes courants
1. **Serveur non accessible:** Vérifiez `python manage.py runserver`
2. **Dépendances manquantes:** Exécutez `./setup_api_testing.sh`
3. **Erreurs d'authentification:** Vérifiez vos identifiants

### Logs et debugging
```bash
# Activer les logs détaillés
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 -u simple_api_tester.py 2>&1 | tee api_test.log
```

## 🎯 Prochaines Étapes

1. **Testez vos APIs:** Lancez `python3 simple_api_tester.py`
2. **Analysez les résultats:** Consultez les rapports générés
3. **Optimisez:** Identifiez les endpoints lents
4. **Documentez:** Utilisez les captures d'écran pour la documentation
5. **Automatisez:** Intégrez les tests dans votre workflow

---

**🎉 Vous êtes maintenant prêt à tester vos APIs et générer des captures d'écran automatiquement !**
