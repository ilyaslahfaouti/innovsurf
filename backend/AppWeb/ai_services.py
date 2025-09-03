# ai_services.py
import re
import json
import random
from typing import List, Dict, Tuple
import os
import requests
from difflib import SequenceMatcher
from django.db.models import Q
from .models import ChatbotFAQ, SurfSpot, Equipment, SurfClub, Surfer
from .windy_api_service import windy_service

class ChatbotAI:
    """Service IA pour le chatbot YalaSurf avec intégration Windy"""
    
    def __init__(self):
        self.greetings = [
            "Bonjour ! Je suis YalaBot, votre assistant surf. Comment puis-je vous aider ?",
            "Salut ! Prêt pour une session de surf ? Que souhaitez-vous savoir ?",
            "Hey ! Je suis là pour vous aider avec tout ce qui concerne le surf !"
        ]
        
        self.farewells = [
            "Bon surf ! N'hésitez pas à revenir si vous avez d'autres questions.",
            "À bientôt sur les vagues ! 🏄‍♂️",
            "Amusez-vous bien sur l'eau !"
        ]
        
        self.unknown_responses = [
            "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler ?",
            "Désolé, je n'ai pas saisi votre question. Essayez avec d'autres mots.",
            "Je suis encore en apprentissage. Pourriez-vous être plus spécifique ?"
        ]
    
    def process_message(self, message: str, user_id: int = None, use_llm: bool | None = None) -> Dict:
        """
        Traite un message utilisateur et retourne une réponse intelligente
        """
        message = message.lower().strip()
        
        # Si une clé OPENAI_API_KEY est configurée, on enrichit les réponses avec un LLM
        # On laisse la logique métier prioritaire pour météo/horaires optimaux
        intent = self._classify_intent(message)
        if intent in {"weather", "optimal_times"}:
            response = self._generate_response(message, intent, user_id)
        else:
            llm_api_key = os.environ.get("OPENAI_API_KEY")
            # Décision d'usage LLM: si use_llm == True on force LLM (si clé dispo);
            # si use_llm == False on évite LLM; sinon comportement automatique.
            should_use_llm = (use_llm is True) or (use_llm is None)
            if llm_api_key and should_use_llm:
                context = self._build_context_from_data(message)
                response = self._generate_llm_response(message, llm_api_key, context)
                if not response:  # fallback si l'appel LLM échoue
                    response = self._generate_response(message, intent, user_id)
                else:
                    intent = "llm"
            else:
                response = self._generate_response(message, intent, user_id)
        
        return {
            'response': response,
            'intent': intent,
            'confidence': self._calculate_confidence(message, intent)
        }

    def _generate_llm_response(self, message: str, api_key: str, context: str) -> str:
        """
        Appelle un modèle de langage (type ChatGPT) pour générer une réponse riche et créative.
        Utilise l'API HTTP sans dépendance supplémentaire.
        """
        try:
            # Modèle par défaut; peut être surchargé via OPENAI_MODEL
            model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": model,
                "temperature": 0.8,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Tu es InnovBot, un assistant surf expert. Propose des idées utiles, claires,"
                            " et actionnables (itineraires surf, équipement adapté, planning, conseils de sécurité)."
                            " Si pertinent, suggère 2-3 pistes concrètes. Réponds en français."
                        ),
                    },
                    {
                        "role": "system",
                        "content": (
                            "Contexte (données internes du site) à respecter en priorité pour répondre: \n" + context
                        ),
                    },
                    {"role": "user", "content": message},
                ],
            }
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=20,
            )
            if resp.status_code != 200:
                return ""
            data = resp.json()
            content = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
                .strip()
            )
            return content or ""
        except Exception:
            return ""

    def _build_context_from_data(self, message: str) -> str:
        """
        Construit un contexte concis issu de la base (spots/clubs/équipements) et, si un spot est mentionné,
        ajoute un résumé météo via windy_service. Objectif: réponses ancrées dans les données du projet.
        """
        try:
            parts: List[str] = []
            # Spots disponibles
            spots = list(SurfSpot.objects.all()[:10])
            if spots:
                parts.append("Spots disponibles: " + ", ".join(s.name for s in spots))
            # Clubs (par spot)
            clubs = list(SurfClub.objects.select_related('surf_spot').all()[:10])
            if clubs:
                club_summ = {}
                for c in clubs:
                    club_summ.setdefault(c.surf_spot.name, 0)
                    club_summ[c.surf_spot.name] += 1
                parts.append("Clubs par spot: " + ", ".join(f"{k}:{v}" for k,v in club_summ.items()))
            # Équipements (compte global)
            eq_count = Equipment.objects.count()
            if eq_count:
                parts.append(f"Équipements total: {eq_count}")
            # Détection spot mentionné et météo
            msg = (message or "").lower()
            known_spots = [
                'taghazout','agadir','essaouira','bouznika','anchor point','boilers'
            ]
            mentioned = None
            for ks in known_spots:
                if ks in msg:
                    mentioned = ks
                    break
            if mentioned:
                try:
                    summary = windy_service.get_surf_conditions_summary(mentioned)
                    parts.append(f"Météo ({mentioned}): {summary}")
                except Exception:
                    pass
            return "\n".join(parts) if parts else ""
        except Exception:
            return ""
    
    def _classify_intent(self, message: str) -> str:
        """
        Classification de l'intention du message utilisateur
        """
        # Salutations
        if any(word in message for word in ['bonjour', 'salut', 'hey', 'hello', 'hi']):
            return 'greeting'
        
        # Au revoir
        if any(word in message for word in ['au revoir', 'bye', 'ciao', 'adieu']):
            return 'farewell'
        
        # Questions sur les spots (mots-clés génériques)
        if any(word in message for word in ['spot', 'vague', 'plage', 'océan', 'mer']):
            return 'surf_spots'
        
        # Questions sur l'équipement
        if any(word in message for word in ['planche', 'board', 'équipement', 'matériel', 'combinaison']):
            return 'equipment'
        
        # Questions sur les cours
        if any(word in message for word in ['cours', 'leçon', 'apprendre', 'moniteur', 'professeur']):
            return 'lessons'
        
        # Questions sur les clubs
        if any(word in message for word in ['club', 'école', 'surf club']):
            return 'surf_clubs'
        
        # Questions sur la météo (étendu avec Windy)
        if any(word in message for word in ['météo', 'temps', 'vent', 'marée', 'forecast', 'prévision', 'conditions', 'houle']):
            return 'weather'
        
        # Questions sur les meilleurs moments pour surfer (doit PRENDRE LE DESSUS sur la simple détection de spot)
        if any(word in message for word in ['quand', 'meilleur moment', 'optimal', 'conditions', 'surfer']):
            return 'optimal_times'

        # Détecter directement un nom de spot pour répondre même sans mot-clé (après optimal_times)
        known_spots = ['agadir', 'taghazout', 'essaouira', 'bouznika', 'anchor point', 'boilers']
        if any(ks in message for ks in known_spots):
            return 'surf_spots'
        
        # Questions générales
        if any(word in message for word in ['quoi', 'comment', 'où', 'quand', 'pourquoi']):
            return 'general_question'
        
        return 'unknown'
    
    def _generate_response(self, message: str, intent: str, user_id: int = None) -> str:
        """
        Génère une réponse basée sur l'intention et le contexte
        """
        if intent == 'greeting':
            return random.choice(self.greetings)
        
        elif intent == 'farewell':
            return random.choice(self.farewells)
        
        elif intent == 'surf_spots':
            return self._get_surf_spots_info(message)
        
        elif intent == 'equipment':
            return self._get_equipment_info(message)
        
        elif intent == 'lessons':
            return self._get_lessons_info(message)
        
        elif intent == 'surf_clubs':
            return self._get_surf_clubs_info(message)
        
        elif intent == 'weather':
            return self._get_weather_info_with_windy(message)
        
        elif intent == 'optimal_times':
            return self._get_optimal_surf_times(message)
        
        elif intent == 'general_question':
            return self._search_faq(message)
        
        else:
            return random.choice(self.unknown_responses)
    
    def _get_surf_spots_info(self, message: str) -> str:
        """
        Génère des informations sur les spots de surf
        """
        spots = SurfSpot.objects.all()
        if not spots.exists():
            return "Je n'ai pas encore d'informations sur les spots de surf disponibles."
        
        # Recherche intelligente basée sur les mots-clés
        keywords = ['agadir', 'taghazout', 'bouznika', 'essaouira']
        for keyword in keywords:
            if keyword in message:
                spot = spots.filter(name__icontains=keyword).first()
                if spot:
                    # Utiliser les champs existants du modèle SurfSpot
                    addr = spot.address or 'adresse inconnue'
                    zipc = spot.zip_code or ''
                    lat = f"{spot.latitude}" if spot.latitude is not None else 'N/A'
                    lon = f"{spot.longitude}" if spot.longitude is not None else 'N/A'
                    base = (
                        f"📍 {spot.name} (CP {zipc})\n"
                        f"Adresse: {addr}\n"
                        f"Coordonnées: lat {lat}, lon {lon}\n"
                    )
                    # Essayer de joindre un résumé des meilleurs moments (2 jours)
                    try:
                        ot = windy_service.get_optimal_surf_times(
                            lat=float(spot.latitude) if spot.latitude is not None else 30.0,
                            lon=float(spot.longitude) if spot.longitude is not None else -9.0,
                            days=2
                        )
                        formatted = self._format_optimal_times(ot, spot.name)
                        if formatted:
                            return base + "\n" + formatted
                    except Exception:
                        pass
                    return base + "\n💡 Dites: 'Quand surfer à {spot.name} ?' pour un planning optimal."
        
        # Réponse générale
        spot_names = [spot.name for spot in spots[:3]]
        return f"Voici quelques spots populaires : {', '.join(spot_names)}. Que souhaitez-vous savoir sur un spot en particulier ?"
    
    def _get_equipment_info(self, message: str) -> str:
        """
        Génère des informations sur l'équipement
        """
        equipment = Equipment.objects.all()
        if not equipment.exists():
            return "Je n'ai pas encore d'informations sur l'équipement disponible."
        
        # Recherche par type
        if 'planche' in message or 'board' in message:
            boards = equipment.filter(name__icontains='planche')
            if boards.exists():
                return f"Nous avons {boards.count()} planches disponibles. Voulez-vous des détails sur une planche spécifique ?"
        
        if 'combinaison' in message or 'wetsuit' in message:
            suits = equipment.filter(name__icontains='combinaison')
            if suits.exists():
                return f"Nous avons {suits.count()} combinaisons disponibles. Quelle taille recherchez-vous ?"
        
        return f"Nous avons {equipment.count()} équipements disponibles. Que souhaitez-vous louer ou acheter ?"
    
    def _get_lessons_info(self, message: str) -> str:
        """
        Génère des informations sur les cours de surf
        """
        if 'niveau' in message or 'débutant' in message:
            return "Nos cours s'adaptent à tous les niveaux : débutant, intermédiaire et avancé. Chaque cours dure 1h30 et inclut l'équipement."
        
        if 'prix' in message or 'tarif' in message:
            return "Les cours de surf coûtent entre 30€ et 50€ selon le niveau et la durée. Contactez-nous pour un devis personnalisé !"
        
        if 'moniteur' in message or 'professeur' in message:
            return "Nos moniteurs sont diplômés et expérimentés. Ils s'adaptent au niveau de chaque élève pour un apprentissage optimal."
        
        return "Nous proposons des cours de surf pour tous niveaux avec des moniteurs expérimentés. Que souhaitez-vous savoir en particulier ?"
    
    def _get_surf_clubs_info(self, message: str) -> str:
        """
        Génère des informations sur les clubs de surf
        """
        clubs = SurfClub.objects.all()
        if not clubs.exists():
            return "Je n'ai pas encore d'informations sur les clubs de surf."
        
        if 'agadir' in message or 'taghazout' in message:
            agadir_clubs = clubs.filter(surf_spot__location__icontains='agadir')
            if agadir_clubs.exists():
                return f"À Agadir/Taghazout, nous avons {agadir_clubs.count()} clubs partenaires. Voulez-vous leurs coordonnées ?"
        
        return f"Nous collaborons avec {clubs.count()} clubs de surf dans différentes régions. Dans quelle zone souhaitez-vous surfer ?"
    
    def _get_weather_info_with_windy(self, message: str) -> str:
        """
        Génère des informations météo avec l'API Windy
        """
        # Détecter le spot mentionné dans le message
        spots = ['taghazout', 'agadir', 'essaouira', 'bouznika', 'anchor point', 'boilers']
        mentioned_spot = None
        
        for spot in spots:
            if spot in message:
                mentioned_spot = spot
                break
        
        if mentioned_spot:
            # Utiliser l'API Windy pour des prévisions précises
            try:
                summary = windy_service.get_surf_conditions_summary(mentioned_spot)
                return summary
            except Exception as e:
                # Fallback si l'API échoue
                return self._get_basic_weather_info(message)
        else:
            # Pas de spot spécifique mentionné
            if 'aujourd\'hui' in message or 'maintenant' in message:
                return "Pour les conditions actuelles, je vous recommande de me dire sur quel spot vous voulez des infos (ex: 'Météo à Taghazout aujourd\'hui'). Je peux vous donner des prévisions précises avec Windy !"
            
            if 'demain' in message or 'weekend' in message:
                return "Pour les prévisions, dites-moi sur quel spot vous voulez des infos (ex: 'Météo à Essaouira demain'). Je peux analyser les conditions optimales pour le surf !"
            
            return "La météo est cruciale pour le surf ! Dites-moi sur quel spot vous voulez des prévisions (ex: Taghazout, Essaouira, Agadir) et je vous donnerai un rapport détaillé avec Windy !"
    
    def _get_basic_weather_info(self, message: str) -> str:
        """
        Informations météo de base si l'API Windy n'est pas disponible
        """
        if 'aujourd\'hui' in message or 'maintenant' in message:
            return "Pour les conditions actuelles, je vous recommande de consulter notre page météo en temps réel. Les conditions changent rapidement !"
        
        if 'demain' in message or 'weekend' in message:
            return "Pour les prévisions, consultez notre section météo. En général, les meilleures conditions sont tôt le matin ou en fin d'après-midi."
        
        return "La météo est cruciale pour le surf ! Consultez nos prévisions détaillées sur la page météo pour planifier vos sessions."
    
    def _get_optimal_surf_times(self, message: str) -> str:
        """
        Détermine les meilleurs moments pour surfer avec Windy
        """
        # Détecter le spot et la période
        spots = ['taghazout', 'agadir', 'essaouira', 'bouznika']
        mentioned_spot = None
        
        for spot in spots:
            if spot in message:
                mentioned_spot = spot
                break
        
        if mentioned_spot:
            try:
                # Obtenir les meilleurs moments pour surfer
                optimal_times = windy_service.get_optimal_surf_times(
                    lat=30.5451 if 'taghazout' in mentioned_spot else 31.5085,
                    lon=-9.7101 if 'taghazout' in mentioned_spot else -9.7595,
                    days=3
                )
                
                formatted = self._format_optimal_times(optimal_times, mentioned_spot.title())
                if formatted:
                    return formatted
                else:
                    return f"Je n'ai pas pu récupérer les prévisions optimales pour {mentioned_spot} actuellement. Essayez plus tard ou consultez notre page météo !"
                    
            except Exception as e:
                return f"Je rencontre un problème technique pour analyser les conditions optimales à {mentioned_spot}. Consultez notre page météo pour les prévisions !"
        else:
            return "Pour vous dire quand c'est le meilleur moment pour surfer, dites-moi sur quel spot vous voulez des infos (ex: 'Quand surfer à Taghazout ?'). Je peux analyser les conditions optimales !"

    def _format_optimal_times(self, optimal_times: Dict, spot_name: str) -> str:
        """Formate une réponse riche (emojis, multilignes) pour les meilleurs moments."""
        try:
            if not (optimal_times.get('success') and optimal_times.get('optimal_times')):
                return ""
            lines = [f"🏄‍♂️ Meilleurs moments pour surfer à {spot_name} :", ""]
            for day in optimal_times['optimal_times'][:2]:
                lines.append(f"📅 {day.get('date','?')} - Score: {day.get('score','?')}/10")
                lines.append(f"   📏 Vagues moyennes: {day.get('wave_height','?')}m")
                lines.append(f"   💨 Vent moyen: {day.get('wind_speed','?')} km/h")
                if day.get('best_hours'):
                    best_hour = day['best_hours'][0]
                    lines.append(f"   ⏰ Meilleure heure: {best_hour.get('hour','?')}h (Score: {best_hour.get('score','?')}/10)")
                lines.append(f"   💡 {day.get('recommendation','Bonnes conditions')}")
                lines.append("")
            lines.append("💡 Conseil: Les conditions sont optimales quand les vagues font 1-3m et le vent est inférieur à 15 km/h !")
            return "\n".join(lines)
        except Exception:
            return ""
    
    def _search_faq(self, message: str) -> str:
        """
        Recherche dans la FAQ pour trouver des réponses pertinentes
        """
        faqs = ChatbotFAQ.objects.filter(is_active=True)
        if not faqs.exists():
            return "Je n'ai pas encore de FAQ disponible. Pouvez-vous reformuler votre question ?"
        
        # Recherche par similarité
        best_match = None
        best_score = 0
        
        for faq in faqs:
            # Recherche dans la question
            question_score = SequenceMatcher(None, message, faq.question.lower()).ratio()
            
            # Recherche dans les mots-clés
            keywords = [kw.strip().lower() for kw in faq.keywords.split(',')]
            keyword_score = max([SequenceMatcher(None, message, kw).ratio() for kw in keywords]) if keywords else 0
            
            # Score combiné
            combined_score = max(question_score, keyword_score)
            
            if combined_score > best_score and combined_score > 0.3:  # Seuil de similarité
                best_score = combined_score
                best_match = faq
        
        if best_match:
            return best_match.answer
        
        return "Je n'ai pas trouvé de réponse précise à votre question. Pouvez-vous être plus spécifique ?"
    
    def _calculate_confidence(self, message: str, intent: str) -> float:
        """
        Calcule le niveau de confiance de la classification
        """
        # Logique simple de calcul de confiance
        if intent == 'unknown':
            return 0.1
        
        # Mots-clés spécifiques augmentent la confiance
        confidence = 0.6
        
        if intent == 'greeting' and any(word in message for word in ['bonjour', 'salut']):
            confidence = 0.9
        elif intent == 'surf_spots' and any(word in message for word in ['spot', 'vague']):
            confidence = 0.8
        elif intent == 'equipment' and any(word in message for word in ['planche', 'équipement']):
            confidence = 0.8
        elif intent == 'weather' and any(word in message for word in ['météo', 'conditions']):
            confidence = 0.85
        elif intent == 'optimal_times' and any(word in message for word in ['quand', 'meilleur']):
            confidence = 0.8
        
        return min(confidence, 1.0)
    
    def get_suggested_questions(self) -> List[str]:
        """
        Retourne des questions suggérées pour guider l'utilisateur
        """
        return [
            "Quels sont les meilleurs spots de surf ?",
            "Comment réserver un cours de surf ?",
            "Quel équipement me recommandez-vous ?",
            "Quelles sont les conditions météo à Taghazout ?",
            "Quand est le meilleur moment pour surfer ?",
            "Comment rejoindre un club de surf ?"
        ]

# Instance globale du chatbot
chatbot_ai = ChatbotAI()
