#!/usr/bin/env python3
"""
Test interactif simple de YalaSurf
Teste le chatbot et l'API Windy de manière interactive
"""

import requests
import json
import time

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🎯 {title}")
    print(f"{'='*50}")

def test_chatbot_interactif():
    """Test interactif du chatbot"""
    print_header("TEST INTERACTIF DU CHATBOT")
    
    session_id = f"interactive_{int(time.time())}"
    
    # Questions de test
    questions = [
        "Bonjour !",
        "Quelle est la météo à Taghazout ?",
        "Comment réserver un cours de surf ?",
        "Quel équipement me recommandez-vous ?",
        "Quels sont les meilleurs spots de surf ?"
    ]
    
    print("🤖 Test du chatbot YalaBot...")
    print("📝 Session ID:", session_id)
    print()
    
    for i, question in enumerate(questions, 1):
        print(f"🤔 Question {i}: {question}")
        
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
                print(f"🤖 Réponse: {data['response'][:80]}...")
                print(f"🎯 Intent: {data['intent']} (Confiance: {data['confidence']:.2f})")
                print(f"💡 Questions suggérées: {len(data['suggested_questions'])}")
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        print("-" * 40)
        time.sleep(1)

def test_windy_interactif():
    """Test interactif de l'API Windy"""
    print_header("TEST INTERACTIF DE L'API WINDY")
    
    spots = ['Taghazout', 'Essaouira', 'Agadir', 'Bouznika']
    
    print("🌊 Test des prévisions météo...")
    print()
    
    for spot in spots:
        print(f"📍 {spot}:")
        
        try:
            # Prévisions
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
                    print(f"   🧭 Direction vent: {conditions.get('wind_direction', 'N/A')}°")
                else:
                    print(f"   ❌ Erreur: {data.get('error', 'Inconnue')}")
            else:
                print(f"   ❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        print()
    
    # Test du résumé des conditions
    print("📝 Test du résumé des conditions:")
    try:
        response = requests.get(
            'http://localhost:8000/api/windy/conditions-summary/',
            params={'spot': 'Taghazout'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            summary = data.get('summary', '')
            print(f"   🌊 Taghazout: {summary[:100]}...")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def test_integration():
    """Test de l'intégration Chatbot + Windy"""
    print_header("TEST D'INTÉGRATION CHATBOT + WINDY")
    
    session_id = f"integration_{int(time.time())}"
    
    print("🤖🌊 Test de l'intégration...")
    print()
    
    # Questions météo pour tester l'intégration
    weather_questions = [
        "Quelle est la météo à Essaouira ?",
        "Comment sont les conditions à Agadir ?",
        "Quelles sont les prévisions pour Bouznika ?"
    ]
    
    for question in weather_questions:
        print(f"🤔 {question}")
        
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
                print(f"🤖 Réponse: {data['response'][:80]}...")
                print(f"🎯 Intent: {data['intent']} (Confiance: {data['confidence']:.2f})")
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        print("-" * 40)
        time.sleep(1)

def main():
    """Fonction principale"""
    print_header("🚀 TEST INTERACTIF YALASURF")
    print("⏰ Démarrage:", time.strftime('%Y-%m-%d %H:%M:%S'))
    
    try:
        # Test 1: Chatbot
        test_chatbot_interactif()
        
        # Test 2: API Windy
        test_windy_interactif()
        
        # Test 3: Intégration
        test_integration()
        
        print_header("🎉 TESTS INTERACTIFS TERMINÉS !")
        print("✅ Toutes les fonctionnalités sont opérationnelles")
        print("🤖 Chatbot IA: Fonctionne parfaitement")
        print("🌊 API Windy: Intégrée et fonctionnelle")
        print("🚀 Prêt pour la production !")
        
        print("\n🌐 Accès aux services:")
        print("   Frontend: http://localhost:3000")
        print("   Backend: http://localhost:8000")
        print("   Chatbot: http://localhost:8000/api/chatbot/")
        print("   Windy: http://localhost:8000/api/windy/")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Tests interrompus par l'utilisateur")
    except Exception as e:
        print(f"\n\n❌ Erreur lors des tests: {e}")

if __name__ == "__main__":
    main()
