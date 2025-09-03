#!/usr/bin/env python3
"""
Script de configuration d'un utilisateur de test pour les APIs InnovSurf
Crée un utilisateur avec les bonnes permissions pour tester toutes les APIs
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innovsurf.settings')
django.setup()

from AppWeb.models import CustomUser, SurfClub, Surfer, Monitor
from django.contrib.auth import authenticate
from django.db import transaction

def create_test_user():
    """Créer un utilisateur de test avec toutes les permissions"""
    print("🔧 Configuration de l'utilisateur de test...")
    
    try:
        # Vérifier si l'utilisateur existe déjà
        username = "testuser"
        email = "test@innovsurf.com"
        
        if CustomUser.objects.filter(email=email).exists():
            print(f"✅ L'utilisateur {email} existe déjà")
            user = CustomUser.objects.get(email=email)
        else:
            # Créer l'utilisateur
            user = CustomUser.objects.create_user(
                email=email,
                password="testpass123",
                is_staff=True,
                is_superuser=True,
                is_surfer=True,
                is_surfclub=True
            )
            print(f"✅ Utilisateur {email} créé avec succès")
        
        # Créer un profil de club de surf si nécessaire
        if not SurfClub.objects.filter(user=user).exists():
            # Vérifier s'il y a des spots de surf disponibles
            from AppWeb.models import SurfSpot
            if SurfSpot.objects.exists():
                surf_spot = SurfSpot.objects.first()
                club = SurfClub.objects.create(
                    user=user,
                    name="Test Surf Club",
                    surf_spot=surf_spot
                )
                print(f"✅ Club de surf créé: {club.name}")
            else:
                print("⚠️  Aucun spot de surf disponible pour créer le club")
        
        # Créer un profil de surfeur si nécessaire
        if not Surfer.objects.filter(user=user).exists():
            from datetime import date
            surfer = Surfer.objects.create(
                user=user,
                firstname="Test",
                lastname="User",
                birthday=date(1990, 1, 1),
                level="intermediate"
            )
            print(f"✅ Profil surfeur créé pour {user.email}")
        
        # Créer un profil de moniteur si nécessaire
        if not Monitor.objects.filter(surf_club__user=user).exists():
            # Récupérer le club créé
            club = SurfClub.objects.get(user=user)
            from datetime import date
            monitor = Monitor.objects.create(
                first_name="Test",
                last_name="Monitor",
                birthday=date(1985, 1, 1),
                active=True,
                surf_club=club
            )
            print(f"✅ Profil moniteur créé pour {user.email}")
        
        print("\n🎯 Utilisateur de test configuré avec succès !")
        print(f"   Email: {email}")
        print(f"   Password: testpass123")
        print(f"   Superuser: Oui")
        print(f"   Staff: Oui")
        print(f"   Surfer: Oui")
        print(f"   SurfClub: Oui")
        
        return email, "testpass123"
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
        return None, None

def test_authentication(username, password):
    """Tester l'authentification de l'utilisateur"""
    print(f"\n🔐 Test d'authentification pour {username}...")
    
    try:
        # Test d'authentification Django
        user = authenticate(username=username, password=password)
        if user:
            print(f"✅ Authentification Django réussie")
            print(f"   User ID: {user.id}")
            print(f"   Is active: {user.is_active}")
            print(f"   Is staff: {user.is_staff}")
            print(f"   Is superuser: {user.is_superuser}")
        else:
            print(f"❌ Authentification Django échouée")
            return False
        
        # Test de l'API token
        import requests
        
        auth_url = "http://localhost:8000/api/token/"
        auth_data = {
            "email": username,  # username est en fait l'email
            "password": password
        }
        
        response = requests.post(auth_url, json=auth_data)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access')
            refresh_token = token_data.get('refresh')
            
            print(f"✅ Authentification API réussie")
            print(f"   Access token: {access_token[:20]}...")
            print(f"   Refresh token: {refresh_token[:20]}...")
            
            # Test d'un endpoint protégé
            test_url = "http://localhost:8000/api/surf-club/profile/"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            test_response = requests.get(test_url, headers=headers)
            print(f"   Test endpoint protégé: {test_response.status_code}")
            
            return True
        else:
            print(f"❌ Authentification API échouée: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'authentification: {e}")
        return False

def update_test_config(username, password):
    """Mettre à jour la configuration des tests"""
    print(f"\n📝 Mise à jour de la configuration des tests...")
    
    # Mettre à jour api_screenshot_tool.py
    try:
        with open('api_screenshot_tool.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer les identifiants par défaut
        content = content.replace('username="admin"', f'username="{username}"')
        content = content.replace('password="admin"', f'password="{password}"')
        content = content.replace('username="testuser"', f'username="{username}"')
        content = content.replace('password="testpass123"', f'password="{password}"')
        
        with open('api_screenshot_tool.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ api_screenshot_tool.py mis à jour")
    except Exception as e:
        print(f"⚠️  Impossible de mettre à jour api_screenshot_tool.py: {e}")
    
    # Mettre à jour test_forecast_api.py
    try:
        with open('test_forecast_api.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('username="admin"', f'username="{username}"')
        content = content.replace('password="admin"', f'password="{password}"')
        
        with open('test_forecast_api.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ test_forecast_api.py mis à jour")
    except Exception as e:
        print(f"⚠️  Impossible de mettre à jour test_forecast_api.py: {e}")
    
    # Mettre à jour smart_api_tester.py
    try:
        with open('smart_api_tester.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('username="admin"', f'username="{username}"')
        content = content.replace('password="admin"', f'password="{password}"')
        
        with open('smart_api_tester.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ smart_api_tester.py mis à jour")
    except Exception as e:
        print(f"⚠️  Impossible de mettre à jour smart_api_tester.py: {e}")

def main():
    """Fonction principale"""
    print("🔧 Configuration de l'utilisateur de test InnovSurf")
    print("=" * 60)
    
    # Vérifier que Django est accessible
    try:
        from django.conf import settings
        print("✅ Configuration Django chargée")
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        print("Assurez-vous d'être dans le bon répertoire")
        return
    
    # Créer l'utilisateur de test
    username, password = create_test_user()
    
    if not username or not password:
        print("❌ Impossible de créer l'utilisateur de test")
        return
    
    # Tester l'authentification
    if test_authentication(username, password):
        # Mettre à jour la configuration des tests
        update_test_config(username, password)
        
        print("\n🎉 Configuration terminée avec succès !")
        print("\n📋 Prochaines étapes:")
        print("1. Relancez vos tests d'API")
        print("2. Tous les endpoints protégés devraient maintenant fonctionner")
        print("3. Utilisez: python3 smart_api_tester.py")
        
        print(f"\n🔑 Identifiants de test:")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        
    else:
        print("\n❌ Configuration échouée")
        print("Vérifiez que votre serveur Django fonctionne")

if __name__ == "__main__":
    main()
