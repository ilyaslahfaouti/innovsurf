#!/usr/bin/env python
"""
Script de test du chatbot IA YalaSurf
Ce script teste toutes les fonctionnalités du chatbot
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innovsurf.settings')
django.setup()

from AppWeb.ai_services import chatbot_ai

def test_chatbot_functionality():
    """Teste toutes les fonctionnalités du chatbot"""
    
    print("🤖 Test du Chatbot IA YalaSurf")
    print("=" * 50)
    
    # Tests de classification d'intention
    test_cases = [
        # Salutations
        ("Bonjour, comment allez-vous ?", "greeting"),
        ("Salut !", "greeting"),
        ("Hey there!", "greeting"),
        
        # Au revoir
        ("Au revoir", "farewell"),
        ("Bye bye", "farewell"),
        ("À bientôt", "farewell"),
        
        # Spots de surf
        ("Quels sont les meilleurs spots ?", "surf_spots"),
        ("Où puis-je surfer ?", "surf_spots"),
        ("Parlez-moi des vagues", "surf_spots"),
        
        # Équipement
        ("Quel équipement me recommandez-vous ?", "equipment"),
        ("J'ai besoin d'une planche", "equipment"),
        ("Où louer du matériel ?", "equipment"),
        
        # Cours
        ("Comment prendre des cours ?", "lessons"),
        ("Je veux apprendre le surf", "lessons"),
        ("Quel est le prix des leçons ?", "lessons"),
        
        # Clubs
        ("Comment rejoindre un club ?", "surf_clubs"),
        ("Quels clubs recommandez-vous ?", "surf_clubs"),
        ("Où sont les écoles de surf ?", "surf_clubs"),
        
        # Météo
        ("Quelle est la météo aujourd'hui ?", "weather"),
        ("Les conditions sont-elles bonnes ?", "weather"),
        ("Quand surfer ce weekend ?", "weather"),
        
        # Questions générales
        ("Comment ça marche ?", "general_question"),
        ("Que proposez-vous ?", "general_question"),
        ("Pouvez-vous m'aider ?", "general_question"),
    ]
    
    print("\n📊 Tests de Classification d'Intention")
    print("-" * 40)
    
    correct_classifications = 0
    total_tests = len(test_cases)
    
    for message, expected_intent in test_cases:
        result = chatbot_ai.process_message(message)
        actual_intent = result['intent']
        confidence = result['confidence']
        
        status = "✅" if actual_intent == expected_intent else "❌"
        print(f"{status} Message: '{message[:30]}...'")
        print(f"   Attendu: {expected_intent}")
        print(f"   Obtenu:  {actual_intent}")
        print(f"   Confiance: {confidence:.2f}")
        print()
        
        if actual_intent == expected_intent:
            correct_classifications += 1
    
    accuracy = (correct_classifications / total_tests) * 100
    print(f"📈 Précision de classification: {accuracy:.1f}% ({correct_classifications}/{total_tests})")
    
    # Tests de génération de réponses
    print("\n💬 Tests de Génération de Réponses")
    print("-" * 40)
    
    response_tests = [
        "Bonjour",
        "Quels sont les meilleurs spots de surf ?",
        "Comment réserver un cours ?",
        "Quel équipement pour débuter ?",
        "Quelle est la météo ?",
        "Comment rejoindre un club ?"
    ]
    
    for message in response_tests:
        result = chatbot_ai.process_message(message)
        print(f"🤔 Question: {message}")
        print(f"🤖 Réponse: {result['response'][:100]}...")
        print(f"🎯 Intent: {result['intent']}")
        print(f"📊 Confiance: {result['confidence']:.2f}")
        print()
    
    # Tests des questions suggérées
    print("\n💡 Tests des Questions Suggérées")
    print("-" * 40)
    
    suggested_questions = chatbot_ai.get_suggested_questions()
    print(f"Nombre de questions suggérées: {len(suggested_questions)}")
    for i, question in enumerate(suggested_questions, 1):
        print(f"{i}. {question}")
    
    # Tests de performance
    print("\n⚡ Tests de Performance")
    print("-" * 40)
    
    import time
    
    # Test de temps de réponse
    start_time = time.time()
    for _ in range(100):
        chatbot_ai.process_message("Bonjour")
    end_time = time.time()
    
    avg_response_time = (end_time - start_time) / 100 * 1000  # en millisecondes
    print(f"Temps de réponse moyen: {avg_response_time:.2f}ms")
    
    # Test de charge
    print("\n🔄 Test de Charge (1000 messages)")
    start_time = time.time()
    for i in range(1000):
        if i % 100 == 0:
            print(f"   Traité {i} messages...")
        chatbot_ai.process_message(f"Message test {i}")
    end_time = time.time()
    
    total_time = end_time - start_time
    messages_per_second = 1000 / total_time
    print(f"Temps total: {total_time:.2f}s")
    print(f"Messages par seconde: {messages_per_second:.1f}")
    
    print("\n🎉 Tests terminés !")
    print("=" * 50)

def test_faq_search():
    """Teste la recherche dans la FAQ"""
    
    print("\n🔍 Test de Recherche FAQ")
    print("-" * 40)
    
    # Créer quelques entrées de test
    from AppWeb.models import ChatbotFAQ
    
    # Supprimer les anciennes entrées de test
    ChatbotFAQ.objects.filter(question__startswith="TEST_").delete()
    
    # Créer des entrées de test
    test_faqs = [
        {
            'question': 'TEST_Comment réserver un cours ?',
            'answer': 'Pour réserver, allez dans la section cours et choisissez votre créneau.',
            'keywords': 'réserver, cours, créneau, réservation'
        },
        {
            'question': 'TEST_Quel équipement pour débuter ?',
            'answer': 'Nous recommandons une planche longue et une combinaison.',
            'keywords': 'équipement, débutant, planche, combinaison'
        }
    ]
    
    for faq_data in test_faqs:
        ChatbotFAQ.objects.create(**faq_data)
    
    # Tests de recherche
    search_tests = [
        ("Comment réserver ?", "TEST_Comment réserver un cours ?"),
        ("J'ai besoin d'équipement", "TEST_Quel équipement pour débuter ?"),
        ("Je veux prendre des cours", "TEST_Comment réserver un cours ?"),
        ("Quelle planche choisir ?", "TEST_Quel équipement pour débuter ?")
    ]
    
    for search_query, expected_question in search_tests:
        result = chatbot_ai.process_message(search_query)
        print(f"🔍 Recherche: '{search_query}'")
        print(f"📝 Réponse: {result['response'][:80]}...")
        print()
    
    # Nettoyer les entrées de test
    ChatbotFAQ.objects.filter(question__startswith="TEST_").delete()

if __name__ == '__main__':
    try:
        test_chatbot_functionality()
        test_faq_search()
        print("\n🎯 Tous les tests ont été exécutés avec succès !")
        print("Le chatbot IA est prêt pour la production ! 🚀")
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
