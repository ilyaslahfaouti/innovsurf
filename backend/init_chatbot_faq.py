#!/usr/bin/env python
"""
Script d'initialisation de la FAQ du chatbot YalaSurf
Ce script ajoute des questions/réponses fréquentes pour le chatbot IA
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innovsurf.settings')
django.setup()

from AppWeb.models import ChatbotFAQ

def init_chatbot_faq():
    """Initialise la FAQ du chatbot avec des questions/réponses pertinentes"""
    
    # Supprimer les anciennes entrées
    ChatbotFAQ.objects.all().delete()
    
    # Questions/réponses pour la FAQ
    faq_data = [
        {
            'question': 'Comment réserver un cours de surf ?',
            'answer': 'Pour réserver un cours de surf, connectez-vous à votre compte et rendez-vous dans la section "Cours de surf". Choisissez votre niveau, la date et l\'horaire qui vous conviennent. Vous pouvez également contacter directement le club de surf de votre choix.',
            'category': 'reservation',
            'keywords': 'réserver, cours, surf, réservation, booking, leçon'
        },
        {
            'question': 'Quel équipement me recommandez-vous pour débuter ?',
            'answer': 'Pour débuter le surf, nous recommandons une planche de type "longboard" ou "foam board" qui offre plus de stabilité. Une combinaison adaptée à la température de l\'eau est essentielle. Nous proposons la location d\'équipement complet pour vos premières sessions.',
            'category': 'equipment',
            'keywords': 'équipement, débutant, planche, combinaison, matériel, location'
        },
        {
            'question': 'Quels sont les meilleurs spots de surf au Maroc ?',
            'answer': 'Le Maroc offre d\'excellents spots de surf ! Taghazout près d\'Agadir est très populaire, tout comme Anchor Point et Boilers. Essaouira est parfaite pour les débutants avec ses vagues plus douces. Chaque spot a ses caractéristiques selon la saison et le niveau.',
            'category': 'spots',
            'keywords': 'spots, maroc, taghazout, agadir, essaouira, vagues, plages'
        },
        {
            'question': 'Quelles sont les conditions météo idéales pour surfer ?',
            'answer': 'Les meilleures conditions pour surfer sont généralement tôt le matin ou en fin d\'après-midi, quand le vent est plus calme. Une houle de 1 à 2 mètres est idéale pour débuter. Consultez nos prévisions météo en temps réel pour planifier vos sessions.',
            'category': 'weather',
            'keywords': 'météo, conditions, vent, houle, prévisions, temps, vague'
        },
        {
            'question': 'Combien coûtent les cours de surf ?',
            'answer': 'Les prix des cours de surf varient selon le niveau et la durée. Un cours débutant coûte environ 30-40€ pour 1h30, incluant l\'équipement. Les packs de plusieurs cours sont plus avantageux. Contactez-nous pour un devis personnalisé selon vos besoins.',
            'category': 'pricing',
            'keywords': 'prix, tarif, coût, cours, surf, devis, budget'
        },
        {
            'question': 'Comment choisir mon niveau de surf ?',
            'answer': 'Débutant : Première fois sur une planche. Intermédiaire : Vous savez vous lever et surfer des vagues simples. Avancé : Vous maîtrisez les virages et surfez des vagues plus difficiles. Nos moniteurs évaluent votre niveau lors du premier cours.',
            'category': 'levels',
            'keywords': 'niveau, débutant, intermédiaire, avancé, évaluation, progression'
        },
        {
            'question': 'Quels sont les horaires des cours ?',
            'answer': 'Nos cours ont lieu tous les jours de 8h à 18h, avec des créneaux de 1h30. Les horaires varient selon les marées et la météo. Nous proposons des cours privés et en groupe. Réservez à l\'avance pour garantir votre place.',
            'category': 'schedule',
            'keywords': 'horaires, cours, planning, créneaux, réservation, disponibilité'
        },
        {
            'question': 'Comment rejoindre un club de surf ?',
            'answer': 'Pour rejoindre un club de surf, visitez notre page "Clubs de surf" et découvrez nos partenaires. Chaque club propose des formules d\'adhésion avec accès aux équipements et aux cours. Contactez directement le club qui vous intéresse.',
            'category': 'clubs',
            'keywords': 'club, adhésion, école, surf club, partenaires, adhérer'
        },
        {
            'question': 'Quels sont les équipements disponibles à la location ?',
            'answer': 'Nous louons des planches de surf de tous niveaux (longboards, shortboards, fish), des combinaisons de différentes épaisseurs, des leashs et des accessoires. Tous nos équipements sont vérifiés régulièrement pour votre sécurité.',
            'category': 'rental',
            'keywords': 'location, louer, planche, combinaison, équipement, matériel'
        },
        {
            'question': 'Comment se déroule une session de surf ?',
            'answer': 'Une session de surf commence par un briefing sur la sécurité et les conditions. Ensuite, échauffement sur la plage, puis mise à l\'eau avec votre moniteur. Vous apprenez à lire les vagues et à vous positionner. La session se termine par un débriefing et des conseils.',
            'category': 'sessions',
            'keywords': 'session, déroulement, briefing, échauffement, conseils, progression'
        }
    ]
    
    # Créer les entrées FAQ
    created_count = 0
    for faq_item in faq_data:
        try:
            ChatbotFAQ.objects.create(
                question=faq_item['question'],
                answer=faq_item['answer'],
                category=faq_item['category'],
                keywords=faq_item['keywords'],
                is_active=True
            )
            created_count += 1
            print(f"✅ FAQ créée : {faq_item['question'][:50]}...")
        except Exception as e:
            print(f"❌ Erreur lors de la création de la FAQ : {e}")
    
    print(f"\n🎉 Initialisation terminée ! {created_count} questions/réponses ont été ajoutées à la FAQ.")
    print("Le chatbot IA est maintenant prêt à répondre aux questions des utilisateurs !")

if __name__ == '__main__':
    print("🤖 Initialisation de la FAQ du chatbot YalaSurf...")
    init_chatbot_faq()
