import json

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CustomUser, Surfer, SurfClub, SurfSpot, EquipmentType, Equipment, Monitor,Photo

class UserRegisterTestCase(APITestCase):

    def setUp(self):
        # Créez un SurfSpot pour les tests
        self.surf_spot = SurfSpot.objects.create(
            name='Taghazout Beach',
            zip_code='80022',
            address='Taghazout, Morocco',
            description='A popular surf spot in Morocco',
            latitude=30.5425,
            longitude=-9.7075
        )

        self.surf_club_user = CustomUser.objects.create_user(
            email='surfclub@example.com',
            password='strong_password',
            is_surfclub=True
        )
        self.surf_club = SurfClub.objects.create(
            user=self.surf_club_user,
            name='Cool Surf Club',
            surf_spot=self.surf_spot  # Utilisez le surf spot créé plus haut
        )

        # Générez un jeton JWT pour l'utilisateur surf club
        self.token = str(RefreshToken.for_user(self.surf_club_user).access_token)

    def test_register_surfer(self):
        url = reverse('register')
        data = {
            'email': 'testsurfer@example.com',
            'password': 'strong_password',
            'role': 'surfer',
            'firstname': 'Jo',
            'lastname': 'Doe',
            'birthday': '1990-01-01',
            'level': 'beginner',
        }

        response = self.client.post(url, data, format='multipart')  # Simule une requête POST
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

        user = CustomUser.objects.get(email='testsurfer@example.com')
        self.assertTrue(user.is_surfer)
        self.assertFalse(user.is_surfclub)
        self.assertTrue(check_password('strong_password', user.password))

        surfer = Surfer.objects.get(user=user)
        self.assertEqual(surfer.firstname, 'Jo')
        self.assertEqual(surfer.lastname, 'Doe')
        self.assertEqual(surfer.level, 'beginner')

    def test_register_surfclub(self):
        url = reverse('register')
        data = {
            'email': 'testsurfclub@example.com',
            'password': 'strong_password',
            'role': 'surfclub',
            'name': 'Cool Surf Club',
            'surf_spot': self.surf_spot.id,  # Utilisation de surf_spot
        }

        response = self.client.post(url, data, format='multipart')

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print("Errors:", response.data)  # Affiche les erreurs de validation

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

        user = CustomUser.objects.get(email='testsurfclub@example.com')
        self.assertTrue(user.is_surfclub)
        self.assertFalse(user.is_surfer)
        self.assertTrue(check_password('strong_password', user.password))

        surf_club = SurfClub.objects.get(user=user)
        self.assertEqual(surf_club.name, 'Cool Surf Club')
        self.assertEqual(surf_club.surf_spot, self.surf_spot)

    def test_login_after_registration(self):
        register_url = reverse('register')
        register_data = {
            'email': 'testsurfer@example.com',
            'password': 'strong_password',
            'role': 'surfer',
            'firstname': 'Jo',
            'lastname': 'Doe',
            'birthday': '1990-01-01',
            'level': 'beginner',
        }
        register_response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        login_url = reverse('login_view')
        login_data = {
            'email': 'testsurfer@example.com',
            'password': 'strong_password',
        }
        login_response = self.client.post(login_url, login_data, format='json')

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)

        self.assertEqual(login_response.data['user']['email'], 'testsurfer@example.com')
        self.assertTrue(login_response.data['user']['is_surfer'])
        self.assertFalse(login_response.data['user']['is_surfclub'])

        self.assertIn('surfer', login_response.data)
        self.assertEqual(login_response.data['surfer']['firstname'], 'Jo')
        self.assertEqual(login_response.data['surfer']['lastname'], 'Doe')


    def test_add_monitor_to_surf_club(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'birthday': '1990-01-01',
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        url = reverse('add_monitor_to_surfclub')
        response = self.client.post(url, data, format='json')

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print("Errors:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        monitor = Monitor.objects.get(first_name='John', last_name='Doe')
        self.assertEqual(monitor.surf_club, self.surf_club)
        self.assertEqual(monitor.first_name, 'John')
        self.assertEqual(monitor.last_name, 'Doe')

    def test_add_monitor_without_authentication(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'birthday': '1985-05-05',
        }

        url = reverse('add_monitor_to_surfclub')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
class AddEquipmentTestCase(APITestCase):

    def setUp(self):
        self.surf_spot = SurfSpot.objects.create(
            name='Taghazout Beach',
            zip_code='80022',
            address='Taghazout, Morocco',
            description='A popular surf spot in Morocco',
            latitude=30.5425,
            longitude=-9.7075
        )

        self.surf_club_user = CustomUser.objects.create_user(
            email='surfclub@example.com',
            password='strong_password',
            is_surfclub=True
        )

        self.surf_club = SurfClub.objects.create(
            user=self.surf_club_user,
            name='Cool Surf Club',
            surf_spot=self.surf_spot
        )

        self.surfboard_type = EquipmentType.objects.create(type='surfboard')
        self.leash_type = EquipmentType.objects.create(type='leash')
        self.surfsuit_type = EquipmentType.objects.create(type='surfsuit')

        self.token = str(RefreshToken.for_user(self.surf_club_user).access_token)

    def test_add_equipment(self):
        data = {
            'name': 'Test Surfboard',
            'description': 'A high-quality surfboard',
            'size': '6 feet',
            'state': 'New',
            'material_type': 'rent',
            'equipment_type': self.surfboard_type.id,  # Référence à l'ID du type d'équipement
            'sale_price': None,
            'rent_price': '20.00',
            'quantity': 5
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('add_equipment')
        response = self.client.post(url, data, format='json')

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print("Errors:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        equipment = Equipment.objects.get(name='Test Surfboard')
        self.assertEqual(equipment.name, 'Test Surfboard')
        self.assertEqual(equipment.surf_club, self.surf_club)
        self.assertEqual(equipment.equipment_type, self.surfboard_type)
        self.assertEqual(equipment.rent_price, 20.00)
        self.assertEqual(equipment.quantity, 5)

    def test_add_equipment_without_authentication(self):
        data = {
            'name': 'Test Surfboard',
            'description': 'A high-quality surfboard',
            'size': '6 feet',
            'state': 'New',
            'material_type': 'rent',
            'equipment_type': self.surfboard_type.id,
            'sale_price': None,
            'rent_price': '20.00',
            'quantity': 5
        }

        url = reverse('add_equipment')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MonitorUpdateDeleteTestCase(APITestCase):

    def setUp(self):
        self.surf_spot = SurfSpot.objects.create(
            name='Taghazout Beach',
            zip_code='80022',
            address='Taghazout, Morocco',
            description='A popular surf spot in Morocco',
            latitude=30.5425,
            longitude=-9.7075
        )

        self.surf_club_user = CustomUser.objects.create_user(
            email='surfclub@example.com',
            password='strong_password',
            is_surfclub=True
        )

        self.surf_club = SurfClub.objects.create(
            user=self.surf_club_user,
            name='Cool Surf Club',
            surf_spot=self.surf_spot
        )

        self.monitor = Monitor.objects.create(
            first_name='John',
            last_name='Doe',
            birthday='1990-01-01',
            surf_club=self.surf_club
        )

        self.token = str(RefreshToken.for_user(self.surf_club_user).access_token)

    def test_delete_monitor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        url = reverse('monitor-update-delete', kwargs={'pk': self.monitor.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Monitor.objects.filter(pk=self.monitor.id).exists())
