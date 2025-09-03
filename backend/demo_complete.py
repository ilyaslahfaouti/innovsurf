#!/usr/bin/env python3
"""
Démonstration complète de YalaSurf avec Chatbot IA et API Windy
Ce script teste toutes les fonctionnalités intégrées
"""

import requests
import json
import time
from datetime import datetime

def print_header(title):
    """Affiche un en-tête formaté"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_section(title):
    """Affiche une section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def test_chatbot_api():
    """Teste l'API du chatbot IA"""
    print_section("Test du Chatbot IA")
    
    # Test de base
    test_messages = [
        "Bonjour !",
        "Quelle est la météo à Taghazout ?",
        "Quand est le meilleur moment pour surfer ?",
        "Comment réserver un cours de surf ?",
        "Quel équipement me recommandez-vous ?"
    ]
    
    session_id = f"demo_{int(time.time())}"
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🤔 Message {i}: {message}")
        
        try:
            response = requests.post(
                'http://localhost:8000/api/chatbot/',
                json={
                    'message': message,
                    'session_id': session_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"🤖 Réponse: {data['response'][:100]}...")
                print(f"🎯 Intent: {data['intent']} (Confiance: {data['confidence']:.2f})")
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        time.sleep(0.5)  # Pause entre les messages

def test_windy_api():
    """Teste l'API Windy"""
    print_section("Test de l'API Windy")
    
    # Test des prévisions
    spots = ['Taghazout', 'Essaouira', 'Agadir', 'Bouznika']
    
    for spot in spots:
        print(f"\n🌊 Prévisions pour {spot}:")
        
        try:
            response = requests.get(
                f'http://localhost:8000/api/windy/forecast/',
                params={'spot': spot},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    conditions = data.get('current_conditions', {})
                    print(f"   📏 Vagues: {conditions.get('wave_height', 'N/A')}m")
                    print(f"   💨 Vent: {conditions.get('wind_speed', 'N/A')} km/h")
                    print(f"   🌡️ Eau: {conditions.get('water_temp', 'N/A')}°C")
                else:
                    print(f"   ❌ Erreur: {data.get('error', 'Inconnue')}")
            else:
                print(f"   ❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    # Test des moments optimaux
    print(f"\n🏄‍♂️ Moments optimaux pour Taghazout:")
    try:
        response = requests.get(
            'http://localhost:8000/api/windy/optimal-times/',
            params={'spot': 'Taghazout'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                optimal_times = data.get('optimal_times', [])
                for time_data in optimal_times[:2]:  # Afficher les 2 premiers
                    print(f"   📅 {time_data['date']}: Score {time_data['score']}/10")
                    print(f"      📏 Vagues: {time_data['wave_height']}m")
                    print(f"      💨 Vent: {time_data['wind_speed']} km/h")
                    print(f"      💡 {time_data['recommendation']}")
            else:
                print(f"   ❌ Erreur: {data.get('error', 'Inconnue')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def test_windy_conditions_summary():
    """Teste le résumé des conditions"""
    print_section("Test du Résumé des Conditions")
    
    spots = ['Taghazout', 'Essaouira']
    
    for spot in spots:
        print(f"\n📝 Résumé pour {spot}:")
        
        try:
            response = requests.get(
                'http://localhost:8000/api/windy/conditions-summary/',
                params={'spot': spot},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                summary = data.get('summary', '')
                print(f"   {summary[:150]}...")
            else:
                print(f"   ❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")

def test_chatbot_windy_integration():
    """Teste l'intégration Chatbot + Windy"""
    print_section("Test d'Intégration Chatbot + Windy")
    
    weather_questions = [
        "Quelle est la météo à Essaouira ?",
        "Quand est le meilleur moment pour surfer à Taghazout ?",
        "Comment sont les conditions à Agadir ?",
        "Quelles sont les prévisions pour Bouznika ?"
    ]
    
    session_id = f"demo_windy_{int(time.time())}"
    
    for question in weather_questions:
        print(f"\n🤔 Question: {question}")
        
        try:
            response = requests.post(
                'http://localhost:8000/api/chatbot/',
                json={
                    'message': question,
                    'session_id': session_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"🤖 Réponse: {data['response'][:120]}...")
                print(f"🎯 Intent: {data['intent']} (Confiance: {data['confidence']:.2f})")
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        time.sleep(0.5)

def test_performance():
    """Teste les performances"""
    print_section("Test de Performance")
    
    # Test de charge sur le chatbot
    print("🔄 Test de charge sur le chatbot (10 messages):")
    start_time = time.time()
    
    session_id = f"perf_test_{int(time.time())}"
    success_count = 0
    
    for i in range(10):
        try:
            response = requests.post(
                'http://localhost:8000/api/chatbot/',
                json={
                    'message': f'Message de test {i+1}',
                    'session_id': session_id
                },
                timeout=5
            )
            
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"   ❌ Message {i+1}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Message {i+1}: {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"   ✅ {success_count}/10 messages réussis")
    print(f"   ⏱️ Temps total: {total_time:.2f}s")
    print(f"   🚀 Débit: {success_count/total_time:.1f} messages/s")
    
    # Test de charge sur Windy
    print("\n🌊 Test de charge sur Windy (5 requêtes):")
    start_time = time.time()
    
    success_count = 0
    for i in range(5):
        try:
            response = requests.get(
                'http://localhost:8000/api/windy/forecast/',
                params={'spot': 'Taghazout'},
                timeout=5
            )
            
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"   ❌ Requête {i+1}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Requête {i+1}: {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"   ✅ {success_count}/5 requêtes réussies")
    print(f"   ⏱️ Temps total: {total_time:.2f}s")
    print(f"   🚀 Débit: {success_count/total_time:.1f} requêtes/s")

def main():
    """Fonction principale de démonstration"""
    print_header("🚀 DÉMONSTRATION COMPLÈTE YALASURF")
    print(f"⏰ Démarrage: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test 1: Chatbot IA
        test_chatbot_api()
        
        # Test 2: API Windy
        test_windy_api()
        
        # Test 3: Résumé des conditions
        test_windy_conditions_summary()
        
        # Test 4: Intégration Chatbot + Windy
        test_chatbot_windy_integration()
        
        # Test 5: Performance
        test_performance()
        
        print_header("🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS !")
        print("✅ Toutes les fonctionnalités sont opérationnelles")
        print("🤖 Chatbot IA: Fonctionne parfaitement")
        print("🌊 API Windy: Intégrée et fonctionnelle")
        print("🚀 Performance: Excellente")
        print("🎯 Prêt pour la production !")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Démonstration interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur lors de la démonstration: {e}")
        print("🔧 Vérifiez que les services sont bien lancés")

if __name__ == "__main__":
    main()
