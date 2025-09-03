# Configuration des clés API et paramètres
import os

# StormGlass API (météo marine)
# Gratuit : 50 requêtes/jour
# Payant : jusqu'à 1000+ requêtes/jour
STORMGLASS_API_KEY = os.getenv('STORMGLASS_API_KEY', 'f2a0d83a-82c6-11f0-a59f-0242ac130006-f2a0d8da-82c6-11f0-a59f-0242ac130006')

# Alternative : OpenWeatherMap API (météo générale)
# Gratuit : 1000 requêtes/jour
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', None)

# Configuration des timeouts et retry
API_TIMEOUT = 10  # secondes
API_MAX_RETRIES = 3

# Configuration des quotas
STORMGLASS_DAILY_QUOTA = 50  # requêtes gratuites par jour
OPENWEATHER_DAILY_QUOTA = 1000  # requêtes gratuites par jour

# URLs des APIs
STORMGLASS_BASE_URL = 'https://api.stormglass.io/v2'
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'
