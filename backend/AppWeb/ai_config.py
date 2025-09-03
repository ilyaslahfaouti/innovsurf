# ai_config.py
"""
Configuration des paramètres IA pour le chatbot YalaSurf
"""

# Paramètres de classification d'intention
INTENT_CLASSIFICATION = {
    # Seuil de confiance minimum pour la classification
    'MIN_CONFIDENCE': 0.3,
    
    # Mots-clés pour chaque intention
    'GREETING_KEYWORDS': [
        'bonjour', 'salut', 'hey', 'hello', 'hi', 'coucou', 'bonsoir'
    ],
    
    'FAREWELL_KEYWORDS': [
        'au revoir', 'bye', 'ciao', 'adieu', 'à bientôt', 'à plus'
    ],
    
    'SURF_SPOTS_KEYWORDS': [
        'spot', 'vague', 'plage', 'océan', 'mer', 'surfer', 'surf'
    ],
    
    'EQUIPMENT_KEYWORDS': [
        'planche', 'board', 'équipement', 'matériel', 'combinaison', 
        'wetsuit', 'leash', 'location', 'louer'
    ],
    
    'LESSONS_KEYWORDS': [
        'cours', 'leçon', 'apprendre', 'moniteur', 'professeur', 
        'école', 'formation', 'niveau'
    ],
    
    'SURF_CLUBS_KEYWORDS': [
        'club', 'école', 'surf club', 'association', 'partenaire'
    ],
    
    'WEATHER_KEYWORDS': [
        'météo', 'temps', 'vent', 'marée', 'forecast', 'conditions',
        'houle', 'vague'
    ],
    
    'GENERAL_QUESTION_KEYWORDS': [
        'quoi', 'comment', 'où', 'quand', 'pourquoi', 'combien',
        'que', 'qui', 'quel'
    ]
}

# Paramètres de recherche FAQ
FAQ_SEARCH = {
    # Seuil de similarité minimum pour une correspondance
    'SIMILARITY_THRESHOLD': 0.3,
    
    # Poids des différents facteurs de recherche
    'QUESTION_WEIGHT': 0.7,
    'KEYWORD_WEIGHT': 0.3,
    
    # Nombre maximum de résultats retournés
    'MAX_RESULTS': 5,
    
    # Catégories de questions
    'CATEGORIES': [
        'general', 'reservation', 'equipment', 'spots', 'weather',
        'lessons', 'clubs', 'pricing', 'levels', 'schedule', 'sessions'
    ]
}

# Paramètres de génération de réponses
RESPONSE_GENERATION = {
    # Réponses par défaut pour chaque intention
    'DEFAULT_RESPONSES': {
        'greeting': [
            "Bonjour ! Je suis YalaBot, votre assistant surf. Comment puis-je vous aider ?",
            "Salut ! Prêt pour une session de surf ? Que souhaitez-vous savoir ?",
            "Hey ! Je suis là pour vous aider avec tout ce qui concerne le surf !"
        ],
        'farewell': [
            "Bon surf ! N'hésitez pas à revenir si vous avez d'autres questions.",
            "À bientôt sur les vagues ! 🏄‍♂️",
            "Amusez-vous bien sur l'eau !"
        ],
        'unknown': [
            "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler ?",
            "Désolé, je n'ai pas saisi votre question. Essayez avec d'autres mots.",
            "Je suis encore en apprentissage. Pourriez-vous être plus spécifique ?"
        ]
    },
    
    # Questions suggérées par défaut
    'SUGGESTED_QUESTIONS': [
        "Quels sont les meilleurs spots de surf ?",
        "Comment réserver un cours de surf ?",
        "Quel équipement me recommandez-vous ?",
        "Quelles sont les conditions météo aujourd'hui ?",
        "Comment rejoindre un club de surf ?"
    ]
}

# Paramètres de performance
PERFORMANCE = {
    # Cache des réponses fréquentes
    'ENABLE_CACHE': True,
    'CACHE_TTL': 3600,  # 1 heure
    
    # Limite de messages par session
    'MAX_MESSAGES_PER_SESSION': 100,
    
    # Timeout pour le traitement des messages
    'PROCESSING_TIMEOUT': 5.0,  # 5 secondes
}

# Paramètres de personnalisation
PERSONALIZATION = {
    # Utiliser l'historique utilisateur pour personnaliser les réponses
    'USE_USER_HISTORY': True,
    
    # Nombre de messages d'historique à considérer
    'HISTORY_CONTEXT_SIZE': 5,
    
    # Personnalisation basée sur le niveau de surf
    'ADAPT_TO_SURF_LEVEL': True,
    
    # Personnalisation basée sur la localisation
    'ADAPT_TO_LOCATION': True
}

# Paramètres de sécurité
SECURITY = {
    # Validation des messages entrants
    'VALIDATE_INPUT': True,
    
    # Longueur maximale des messages
    'MAX_MESSAGE_LENGTH': 500,
    
    # Filtrage des contenus inappropriés
    'CONTENT_FILTERING': True,
    
    # Rate limiting par utilisateur
    'RATE_LIMIT_ENABLED': True,
    'RATE_LIMIT_MESSAGES': 10,  # messages par minute
}

# Configuration des modèles IA
AI_MODELS = {
    # Modèle de classification d'intention
    'INTENT_MODEL': 'rule_based',  # 'rule_based', 'ml_model', 'hybrid'
    
    # Modèle de recherche sémantique
    'SEMANTIC_MODEL': 'sequence_matcher',  # 'sequence_matcher', 'word2vec', 'bert'
    
    # Modèle de génération de réponses
    'RESPONSE_MODEL': 'template_based',  # 'template_based', 'generative', 'hybrid'
}

# Configuration des logs et monitoring
MONITORING = {
    # Niveau de log
    'LOG_LEVEL': 'INFO',  # 'DEBUG', 'INFO', 'WARNING', 'ERROR'
    
    # Collecte des métriques
    'COLLECT_METRICS': True,
    
    # Alertes de performance
    'PERFORMANCE_ALERTS': True,
    'RESPONSE_TIME_THRESHOLD': 1000,  # ms
    
    # Alertes d'erreur
    'ERROR_ALERTS': True,
    'ERROR_RATE_THRESHOLD': 0.05  # 5%
}
