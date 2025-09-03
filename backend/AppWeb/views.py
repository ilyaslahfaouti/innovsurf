import json
import logging
from django.utils import timezone

from django.db import transaction

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import SurfClub, CustomUser, Monitor, Equipment, SurfSpot, LessonSchedule, SurfLesson, Order, Surfer, \
    SurfSession, EquipmentSelection, OrderItem, Forum, Message, Photo, EquipmentType, Contact, ChatbotConversation, ChatbotMessage, ChatbotFAQ
from .serializer import CustomUserSerializer, SurferSerializer, SurfClubSerializer, MonitorSerializer, \
    EquipmentSerializer, SurfSpotSerializer, SurfLessonSerializer, LessonScheduleSerializer, OrderSerializer, \
    SurfSessionSerializer, MessageSerializer, ForumSerializer, EquipmentTypeSerializer, \
    GetOrderSerializer, GetOrderItemSerializer, GetSurfSessionSerializer, GetSurfSessionProfileSerializer, \
    GetEquipmentSerializer, ContactSerializer, GetMessageSerializer, ChatbotFAQSerializer
from .services import fetch_forecast
from .ai_services import chatbot_ai
import uuid
from .windy_api_service import windy_service
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncWeek

#######################Registration and Login###################
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        print("Request data:", request.data)
        data = request.data.copy()
        password = data.get('password')
        if not password:
            print("Password not provided")
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(password)
        data['password'] = hashed_password

        user_serializer = CustomUserSerializer(data=data)
        print("User serializer data:", data)

        if user_serializer.is_valid():
            user = user_serializer.save()
            print("User created:", user)

            role = data.get('role')
            print("Role:", role)

            if role == 'surfer':
                user.is_surfer = True
                user.is_surfclub = False
                user.save()
                print("User updated as surfer:", user)

                surfer_data = {
                    'user_id': user.id,
                    'firstname': data.get('firstname'),
                    'lastname': data.get('lastname'),
                    'birthday': data.get('birthday'),
                    'level': data.get('level'),
                    'photo': request.FILES.get('photo')
                }
                print("Surfer data:", surfer_data)

                surfer_serializer = SurferSerializer(data=surfer_data)
                if surfer_serializer.is_valid():
                    surfer_serializer.save()
                    print("Surfer profile created")
                else:
                    user.delete()
                    print("Surfer serializer errors:", surfer_serializer.errors)
                    return Response(surfer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif role == 'surfclub':
                user.is_surfer = False
                user.is_surfclub = True
                user.save()
                print("User updated as surf club:", user)

                surfclub_data = {
                    'user_id': user.id,
                    'name': data.get('name'),
                    'surf_spot': data.get('surf_spot'),
                    'logo': request.FILES.get('logo'),
                }
                print("Surf club data:", surfclub_data)

                surfclub_serializer = SurfClubSerializer(data=surfclub_data)
                if surfclub_serializer.is_valid():
                    surfclub_serializer.save()
                    print("Surf club profile created")
                else:
                    user.delete()
                    print("Surf club serializer errors:", surfclub_serializer.errors)
                    return Response(surfclub_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        print("User serializer errors:", user_serializer.errors)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    # USERNAME_FIELD = 'email', donc utiliser 'username' pour authenticate
    user = authenticate(request, username=email, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'phone_number': user.phone_number,
                'address': user.address,
                'is_surfer': user.is_surfer,
                'is_surfclub': user.is_surfclub,

            }
        }
        if user.is_surfclub:
            surfclub = SurfClub.objects.get(user_id=user.id)
            response_data['surfclub'] = {
                'id': surfclub.id,
                'name': surfclub.name,
                'surf_spot': surfclub.surf_spot.name,  # Suppose que surf_spot a un champ 'name'
                'logo': surfclub.logo.url if surfclub.logo else None

            }
        elif user.is_surfer:
            surfer = Surfer.objects.get(user_id=user.id)
            response_data['surfer'] = {
                'id': surfer.id,
                'firstname': surfer.firstname,
                'lastname': surfer.lastname,
                'birthday': surfer.birthday,
                'level': surfer.level,
                'photo':surfer.photo.url if surfer.photo else None
            }

        return Response(response_data, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




#####################Espace surf-club [GET] ################
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_surfclub_profile(request):
    try:

        custom_user = CustomUser.objects.get(pk=request.user.id)

        surf_club = SurfClub.objects.get(user=custom_user)

        user_serializer = CustomUserSerializer(custom_user)
        surfclub_serializer = SurfClubSerializer(surf_club)

        return Response({
            'user': user_serializer.data,
            'surf-club': surfclub_serializer.data
        }, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except SurfClub.DoesNotExist:
        return Response({"error": "SurfClub not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_monitors(request):
    try:
        surf_club = SurfClub.objects.get(user=request.user)
        monitors=Monitor.objects.filter(surf_club=surf_club)
        monitors_serializer=MonitorSerializer(monitors,many=True)
        return Response({
             'monitors': monitors_serializer.data
         }, status=status.HTTP_200_OK)
    except Monitor.DoesNotExist:
        return Response({"error": "Monitors not found."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_monitors_dispo(request):
    try:
        surf_club = SurfClub.objects.get(user=request.user)
        monitors=Monitor.objects.filter(surf_club=surf_club,active=0)
        monitors_serializer=MonitorSerializer(monitors,many=True)
        return Response({
             'monitors': monitors_serializer.data
         }, status=status.HTTP_200_OK)
    except Monitor.DoesNotExist:
        return Response({"error": "Monitors not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def surfclub_equipement_types(request):
    try:

        equipment_types = EquipmentType.objects.all()

        equipment_type_serializer = EquipmentTypeSerializer(equipment_types, many=True)
        return Response({
            'equipment_types': equipment_type_serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_monitor(request,pk):
    try:
        monitor=Monitor.objects.get(pk=pk)
        monitor_serializer=MonitorSerializer(monitor)
        return Response({
            'monitor': monitor_serializer.data
        }, status=status.HTTP_200_OK)
    except Monitor.DoesNotExist:
        return Response({"error": "Monitors not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_equipements(request):
    try:
        surf_club = SurfClub.objects.get(user=request.user)
        equipments = Equipment.objects.filter(surf_club=surf_club)
        for equipment in equipments:
            photos = Photo.objects.filter(equipment=equipment)
            equipment.photos.set(photos)
        equipments_serializer = GetEquipmentSerializer(equipments, many=True)
        return Response({
            'equipments': equipments_serializer.data
        }, status=status.HTTP_200_OK)
    except Equipment.DoesNotExist:
        return Response({"error": "Equipments not found."}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_equipment(request,pk):
    try:
        equipment=Equipment.objects.get(pk=pk)
        equipment_serializer=EquipmentSerializer(equipment)
        return Response({
            'equipment': equipment_serializer.data
        }, status=status.HTTP_200_OK)
    except Equipment.DoesNotExist:
        return Response({"error": "Equipment not found."}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_LessonSchedules(request):
    try:
        surf_club=SurfClub.objects.get(user=request.user)
        lessonSchedules = LessonSchedule.objects.filter(surf_club=surf_club)
        lessonSchedules_serializer = LessonScheduleSerializer(lessonSchedules, many=True)
        return Response({
        'LessonSchedules': lessonSchedules_serializer.data
    }, status=status.HTTP_200_OK)
    except LessonSchedule.DoesNotExist:
        return Response({"error": "LessonSchedules not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_LessonSchedule(request,pk):
    try:
        lesson_schedule = LessonSchedule.objects.get(pk=pk)
        LessonSchedule_serializer = LessonScheduleSerializer(lesson_schedule)
        return Response({
            'lesson_schedules': LessonSchedule_serializer.data
        }, status=status.HTTP_200_OK)
    except LessonSchedule.DoesNotExist:
        return Response({"error": "LessonSchedule not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_SurfSessions(request):
    try:
        surf_club = SurfClub.objects.get(user=request.user)

        surf_sessions = SurfSession.objects.filter(surf_club=surf_club).select_related('lesson_schedule', 'monitor')

        surf_sessions_data = []

        for session in surf_sessions:
            monitor = session.monitor
            lesson_schedule = session.lesson_schedule

            session_data = SurfSessionSerializer(session).data
            monitor_data = MonitorSerializer(monitor).data
            lesson_schedule_data = LessonScheduleSerializer(lesson_schedule).data

            session_data['monitor'] = monitor_data
            session_data['lesson_schedule'] = lesson_schedule_data

            surf_sessions_data.append(session_data)

        return Response({'surf_sessions': surf_sessions_data}, status=status.HTTP_200_OK)

    except SurfClub.DoesNotExist:
        return Response({"error": "SurfClub not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_SurfSession(request, pk):
    try:
        surf_session = SurfSession.objects.get(pk=pk)
        surf_session_data = SurfSessionSerializer(surf_session).data
        monitor_data = MonitorSerializer(surf_session.monitor).data
        lesson_schedule_data = LessonScheduleSerializer(surf_session.lesson_schedule).data
        surf_session_data['monitor'] = monitor_data
        surf_session_data['lesson_schedule'] = lesson_schedule_data
        return Response({'SurfSession': surf_session_data}, status=status.HTTP_200_OK)
    except SurfSession.DoesNotExist:
        return Response({"error": "SurfSession not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_SurfLessons(request):
    try:
        surf_club = SurfClub.objects.get(user=request.user)
        surflessons = SurfLesson.objects.filter(surf_session__surf_club=surf_club)
        surflessons_serializer = SurfLessonSerializer(surflessons, many=True)

        surf_lessons_data = surflessons_serializer.data
        for lesson_data in surf_lessons_data:
            surfer = Surfer.objects.get(id=lesson_data['surfer'])
            lesson_data['surfer'] = SurferSerializer(surfer).data

        return Response({'SurfLessons': surf_lessons_data}, status=status.HTTP_200_OK)

    except SurfClub.DoesNotExist:
        return Response({"error": "Surf Club not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_SurfLesson(request, pk):
    try:
        surf_lesson = SurfLesson.objects.get(pk=pk)
        surf_lesson_serializer = SurfLessonSerializer(surf_lesson)
        surf_session = surf_lesson.surf_session
        surfer = surf_lesson.surfer
        monitor = surf_session.monitor
        lesson_schedule = surf_session.lesson_schedule
        equipment_selections = EquipmentSelection.objects.filter(surf_lesson=surf_lesson)

        surfer_serializer = SurferSerializer(surfer)
        monitor_serializer = MonitorSerializer(monitor)
        lesson_schedule_serializer = LessonScheduleSerializer(lesson_schedule)

        equipment_details = []
        for selection in equipment_selections:
            equipment = selection.equipment
            equipment_serializer = EquipmentSerializer(equipment)
            equipment_details.append({
                'id': equipment.id,
                'name': equipment.name,
                'state': equipment.state,
                'quantity': selection.quantity,
                'equipment_details': equipment_serializer.data
            })

        return Response({
            'SurfLesson': {
                'surf_lesson': surf_lesson_serializer.data,
                'surfer': surfer_serializer.data,
                'monitor': monitor_serializer.data,
                'LessonSchedule': lesson_schedule_serializer.data,
                'equipment_selection': equipment_details
            }
        }, status=status.HTTP_200_OK)

    except SurfLesson.DoesNotExist:
        return Response({"error": "SurfLesson not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

 ############# statistics for surf-club#########

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_statistics(request):
    try:
        surf_club = SurfClub.objects.get(user=request.user)

        num_monitors = Monitor.objects.filter(surf_club=surf_club).count()
        num_equipment = Equipment.objects.filter(surf_club=surf_club).count()
        num_orders = Order.objects.filter(surf_club=surf_club).count()
        num_surf_lessons = SurfLesson.objects.filter(surf_session__surf_club=surf_club).count()
        num_surf_sessions = SurfSession.objects.filter(surf_club=surf_club).count()

        data = {
            "surf_club_name": surf_club.name,
            "number_of_monitors": num_monitors,
            "number_of_equipment": num_equipment,
            "number_of_orders": num_orders,
            "number_of_surf_lessons": num_surf_lessons,
            "number_of_surf_sessions": num_surf_sessions,
        }

        return Response(data, status=status.HTTP_200_OK)

    except SurfClub.DoesNotExist:
        return Response({"error": "Surf Club not found."}, status=status.HTTP_404_NOT_FOUND)
#########Update profiles for surf-club#########


logger = logging.getLogger(__name__)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_surfclub_profile(request):
    try:
        # Récupérer l'utilisateur actuel
        custom_user = CustomUser.objects.get(pk=request.user.id)
        if not custom_user.is_surfclub:
            logger.warning("User is not a surf club.")
            return Response({"error": "User is not a surf club."}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f"Received data: {request.data}")
        print(request.data)

        # Désérialisation des données JSON en dictionnaires Python
        user_data = json.loads(request.data.get('user', '{}'))
        surfclub_data = json.loads(request.data.get('surf_club', '{}'))

        # Hachage du mot de passe s'il est fourni
        if 'password' in user_data and user_data['password']:
            logger.debug("Hashing the password.")
            user_data['password'] = make_password(user_data['password'])

        # Mise à jour des informations de l'utilisateur
        user_serializer = CustomUserSerializer(custom_user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            logger.info("User data updated successfully.")
        else:
            logger.error(f"User data is invalid: {user_serializer.errors}")
            return Response({
                "error": "User data is invalid.",
                "details": user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            surfclub = SurfClub.objects.get(user=custom_user)
        except SurfClub.DoesNotExist:
            logger.error("Surf club profile not found.")
            return Response({"error": "Surf club profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Gestion du logo
        if 'logo' in request.FILES:
            surfclub_data['logo'] = request.FILES['logo']

        surfclub_serializer = SurfClubSerializer(surfclub, data=surfclub_data, partial=True)
        if surfclub_serializer.is_valid():
            surfclub_serializer.save()
            logger.info("Surf club data updated successfully.")
        else:
            logger.error(f"Surf club data is invalid: {surfclub_serializer.errors}")
            return Response({
                "error": "Surf club data is invalid.",
                "details": surfclub_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'user': user_serializer.data,
            'surf_club': surfclub_serializer.data
        }, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        logger.error("User not found.")
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {str(e)}")
        return Response({"error": "An unexpected error occurred.", "details": str(e)},
                        status=status.HTTP_400_BAD_REQUEST)


####################### Post urls for surf club############
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_monitor_to_surfclub(request):
    try:
        custom_user = CustomUser.objects.get(pk=request.user.id)
        if not custom_user.is_surfclub:
            return Response({"error": "User is not a surf club."}, status=status.HTTP_400_BAD_REQUEST)

        surf_club = SurfClub.objects.get(user=custom_user)

        monitor_data = request.data.copy()
        monitor_data['surf_club'] = surf_club.id  # Ajouter l'ID du Surf Club aux données

        monitor_serializer = MonitorSerializer(data=monitor_data)
        if monitor_serializer.is_valid():
            monitor_serializer.save()
            return Response(monitor_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(monitor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except SurfClub.DoesNotExist:
        return Response({"error": "Surf Club not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_equipment(request):
    try:
        custom_user = CustomUser.objects.get(pk=request.user.id)
        if not custom_user.is_surfclub:
            return Response({"error": "User is not a surf club."}, status=status.HTTP_400_BAD_REQUEST)

        surf_club = SurfClub.objects.get(user=custom_user)

        equipment_data = request.data.copy()
        equipment_data['surf_club'] = surf_club.id
        print(equipment_data)

        equipment_serializer = EquipmentSerializer(data=equipment_data)
        if equipment_serializer.is_valid():
            equipment = equipment_serializer.save()

            photos = request.FILES.getlist('photos')
            for photo in photos:
                Photo.objects.create(equipment=equipment, image=photo)

            return Response(equipment_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(equipment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except SurfClub.DoesNotExist:
        return Response({"error": "Surf Club not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_lesson_schedule(request):
    try:
        surf_club = SurfClub.objects.get(user=request.user)

        lesson_schedule_data = request.data.copy()
        lesson_schedule_data['surf_club'] = surf_club.id

        lesson_schedule_serializer = LessonScheduleSerializer(data=lesson_schedule_data)

        if lesson_schedule_serializer.is_valid():
            lesson_schedule_serializer.save()
            return Response(lesson_schedule_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(lesson_schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except SurfClub.DoesNotExist:
        return Response({"error": "Surf Club not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_surf_session(request):
    try:
        user = request.user
        surf_club = get_object_or_404(SurfClub, user=user)

        lesson_schedule_id = request.data.get('lesson_schedule')
        monitor_id = request.data.get('monitor')

        if not lesson_schedule_id:
            return Response({"error": "Lesson schedule is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not monitor_id:
            return Response({"error": "Monitor is required."}, status=status.HTTP_400_BAD_REQUEST)

        lesson_schedule = get_object_or_404(LessonSchedule, id=lesson_schedule_id, surf_club=surf_club)
        monitor = get_object_or_404(Monitor, id=monitor_id, surf_club=surf_club, active=False)

        surf_session_data = {
            'surf_club': surf_club.id,
            'lesson_schedule': lesson_schedule.id,
            'monitor': monitor.id
        }
        print(surf_session_data)
        serializer = SurfSessionSerializer(data=surf_session_data)

        if serializer.is_valid():
            surf_session = serializer.save()

            monitor.active = True
            monitor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("Serializer Errors:", serializer.errors)  # Debugging line
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





######### Get for SurfSpot########
@api_view(['GET'])
def get_surfspots(request):
    try:
        surfspots=SurfSpot.objects.all()
        surfspots_serializer=SurfSpotSerializer(surfspots,many=True)
        return Response(surfspots_serializer.data, status=status.HTTP_200_OK)
    except SurfSpot.DoesNotExist:
        return Response({"error": "Surf Spots not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def surf_spot_details(request, pk):
    try:
        spot = SurfSpot.objects.get(id=pk)
        forecast = fetch_forecast(spot.latitude, spot.longitude)
        spot_data = SurfSpotSerializer(spot).data
        spot_data['forecast'] = forecast
        return Response(spot_data, status=status.HTTP_200_OK)
    except SurfSpot.DoesNotExist:
        return Response({"error": "Surf spot not found."}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_surfspot(request,pk):
    try:
        surfspot= SurfSpot.objects.get(pk=pk)
        surfspot_serializer = SurfSpotSerializer(surfspot)

        return Response({'surf-spot':surfspot_serializer.data,
                               }, status=status.HTTP_200_OK)
    except SurfSpot.DoesNotExist:
        return Response({"error": "Surf Spots not found."}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_surfclub_lesson(request, pk):
    try:
        surfclub = SurfClub.objects.get(pk=pk)
        surfsessions = SurfSession.objects.filter(surf_club=surfclub)
        surfsessions_serializer = GetSurfSessionSerializer(surfsessions, many=True)
        equipments = Equipment.objects.filter(surf_club=surfclub, material_type='rent', quantity__gt=0)
        equipments_serializer = GetEquipmentSerializer(equipments, many=True)

        return Response({
            'SurfSession': surfsessions_serializer.data,
            'Equipments': equipments_serializer.data
        }, status=status.HTTP_200_OK)
    except SurfClub.DoesNotExist:
        return Response({"error": "Surf club not found."}, status=status.HTTP_404_NOT_FOUND)

#################UPDATE Profile for surfer###########################
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_surfer_profile(request):
    try:
        # Récupérer l'utilisateur actuel
        custom_user = CustomUser.objects.get(pk=request.user.id)

        # Récupérer le profil de surfeur associé
        surfer = Surfer.objects.get(user=custom_user)

        # Récupérer la date actuelle
        now = timezone.now().date()

        # Récupérer les sessions de surf associées au surfeur
        past_sessions = SurfLesson.objects.filter(
            surfer=surfer,
            surf_session__lesson_schedule__day__lt=now
        )
        upcoming_sessions = SurfLesson.objects.filter(
            surfer=surfer,
            surf_session__lesson_schedule__day__gte=now
        )

        # Récupérer les commandes passées par le surfeur
        orders = Order.objects.filter(surfer=surfer)

        # Sérialiser les données
        user_serializer = CustomUserSerializer(custom_user)
        surfer_serializer = SurferSerializer(surfer)
        past_sessions_serializer = GetSurfSessionProfileSerializer(past_sessions, many=True)
        upcoming_sessions_serializer = GetSurfSessionProfileSerializer(upcoming_sessions, many=True)

        # Ajouter une sérialisation personnalisée pour les commandes
        orders_data = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            order_data = {
                'id': order.id,
                'order_date': order.order_date,
                'surf_club_name': order.surf_club.name,
                'total_price': order.total_price,
                'items_count': order_items.count(),
                'items': GetOrderItemSerializer(order_items, many=True).data  # Serialize the order items
            }
            orders_data.append(order_data)

        # Retourner les données
        return Response({
            'user': user_serializer.data,
            'surfer': surfer_serializer.data,
            'past_sessions': past_sessions_serializer.data,
            'upcoming_sessions': upcoming_sessions_serializer.data,
            'orders': orders_data,
        }, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Surfer.DoesNotExist:
        return Response({"error": "Surfer profile not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_order_details(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)

        order_serializer = GetOrderSerializer(order)
        order_items_serializer = GetOrderItemSerializer(order_items, many=True)
        return Response({
            'order': order_serializer.data,
            'items': order_items_serializer.data,
        }, status=status.HTTP_200_OK)

    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_surfclub_equipments_buy(request, pk):
    try:
        surfclub = SurfClub.objects.get(pk=pk)

        equipments = Equipment.objects.filter(surf_club=surfclub, material_type='sale',quantity__gt=0 )
        equipments_serializer = GetEquipmentSerializer(equipments, many=True)
        return Response({
            'Equipments': equipments_serializer.data
        }, status=status.HTTP_200_OK)
    except SurfClub.DoesNotExist:
        return Response({"error": "Surf club not found."}, status=status.HTTP_404_NOT_FOUND)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_surfer_profile(request):
    try:
        custom_user = CustomUser.objects.get(pk=request.user.id)
        if not custom_user.is_surfer:
            return Response({"error": "User is not a surfer."}, status=status.HTTP_400_BAD_REQUEST)
        user_data = json.loads(request.data.get('user', '{}'))
        surfer_data = json.loads(request.data.get('surfer', '{}'))
        if user_data:
            if 'password' in user_data:
                user_data['password'] = make_password(user_data['password'])
        user_serializer = CustomUserSerializer(custom_user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        surfer = Surfer.objects.get(user=custom_user)
        if 'photo' in request.FILES:
            surfer_data['photo'] = request.FILES['photo']
        else:
            surfer_data.pop('photo', None)  # Supprime le champ 'photo'

        surfer_serializer = SurferSerializer(surfer, data=surfer_data, partial=True)
        if surfer_serializer.is_valid():
            surfer_serializer.save()
        else:
            return Response(surfer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'user': user_serializer.data,
            'surfer': surfer_serializer.data
        }, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Surfer.DoesNotExist:
        return Response({"error": "Surfer profile not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_surfclub(request, pk):
    try:
        surfclub = SurfClub.objects.get(pk=pk)

        equipments = Equipment.objects.filter(surf_club=surfclub, material_type='rent', quantity__gt=0)
        equipments_serializer = EquipmentSerializer(equipments, many=True)

        return Response({
            'Equipments': equipments_serializer.data
        }, status=status.HTTP_200_OK)
    except SurfClub.DoesNotExist:
        return Response({"error": "Surf club not found."}, status=status.HTTP_404_NOT_FOUND)

#########POST for Surfer##########
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_surf_lesson(request):
    try:
        data = request.data
        surfer = request.user.surfer
        surf_session = SurfSession.objects.get(pk=data['surf_session_id'])
        equipment_ids = data.get('equipment_ids', [])
        equipment_quantities = data.get('equipment_quantities', {})
        surf_lesson = SurfLesson.objects.create(
            surfer=surfer,
            surf_session=surf_session
        )
        total_price = 0
        for equipment_id in equipment_ids:
            quantity = int(equipment_quantities.get(str(equipment_id), 1))
            equipment = Equipment.objects.get(pk=equipment_id)
            if equipment.quantity < quantity:
                return Response({
                    "error": f"Not enough quantity available for {equipment.name}. Requested: {quantity}, Available: {equipment.quantity}"
                }, status=status.HTTP_400_BAD_REQUEST)
            EquipmentSelection.objects.create(
                surf_lesson=surf_lesson,
                equipment=equipment,
                quantity=quantity
            )
            equipment.quantity -= quantity
            equipment.save()
            total_price += equipment.rent_price * quantity
        surf_lesson.total_price = total_price
        surf_lesson.save()
        return Response({'message': 'Surf lesson booked successfully.', 'total_price': total_price}, status=status.HTTP_201_CREATED)
    except SurfSession.DoesNotExist:
        return Response({"error": "Surf session not found."}, status=status.HTTP_404_NOT_FOUND)
    except Equipment.DoesNotExist:
        return Response({"error": "One or more equipment items not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


#######Buy equipments##########

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        with transaction.atomic():
            data = request.data
            print("Request Data:", data)

            surfer = request.user.surfer

            surf_club_id = data.get('surf_club')
            if not surf_club_id:
                return Response({"error": "Surf Club ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                surf_club = SurfClub.objects.get(pk=surf_club_id)
            except SurfClub.DoesNotExist:
                return Response({"error": f"Surf Club with ID {surf_club_id} not found."}, status=status.HTTP_404_NOT_FOUND)

            order = Order.objects.create(surfer=surfer, surf_club=surf_club)
            print("Order Created:", order.id)

            items = data.get('items', [])
            if not items:
                return Response({"error": "No items provided."}, status=status.HTTP_400_BAD_REQUEST)

            total_price = 0
            for item in items:
                equipment_id = item.get('equipment')
                quantity = item.get('quantity', 1)

                if not equipment_id:
                    return Response({"error": "Equipment ID is required for each item."}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    equipment = Equipment.objects.get(pk=equipment_id)
                except Equipment.DoesNotExist:
                    return Response({"error": f"Equipment with ID {equipment_id} not found."}, status=status.HTTP_404_NOT_FOUND)

                if equipment.quantity < quantity:
                    return Response({"error": f"Not enough quantity available for equipment {equipment.name}."}, status=status.HTTP_400_BAD_REQUEST)
                equipment.quantity -= quantity
                equipment.save()

                OrderItem.objects.create(
                    order=order,
                    equipment=equipment,
                    quantity=quantity
                )
                print("OrderItem Created:", equipment_id, quantity)

                total_price += equipment.sale_price * quantity

            order.total_price = total_price
            order.save()

            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("Exception:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
##########Forums#########
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_forum_details(request, surf_spot_id):
    try:
        forum = Forum.objects.get(surf_spot_id=surf_spot_id)
        messages = Message.objects.filter(forum=forum)
        forum_serializer = ForumSerializer(forum)
        message_serializer = GetMessageSerializer(messages, many=True)
        return Response({
            'forum': forum_serializer.data,
            'messages': message_serializer.data
        }, status=status.HTTP_200_OK)
    except Forum.DoesNotExist:
        return Response({"error": "Forum not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_message(request, forum_id):
    try:
        forum = Forum.objects.get(id=forum_id)
        message_data = request.data
        message_data['forum'] = forum.id
        custom_user=CustomUser.objects.get(pk=request.user.id)
        surfer=Surfer.objects.get(user=custom_user)
        message_data['sender'] = surfer.id
        serializer = MessageSerializer(data=message_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Forum.DoesNotExist:
        return Response({"error": "Forum not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_new_messages(request, surf_spot_id):
    try:
        forum = Forum.objects.get(surf_spot_id=surf_spot_id)
        last_message_id = request.query_params.get('last_message_id')

        if last_message_id:
            messages = Message.objects.filter(forum=forum, id__gt=last_message_id)
        else:
            messages = Message.objects.filter(forum=forum)

        message_serializer = GetMessageSerializer(messages, many=True)
        return Response({'messages': message_serializer.data}, status=status.HTTP_200_OK)
    except Forum.DoesNotExist:
        return Response({"error": "Forum not found."}, status=status.HTTP_404_NOT_FOUND)


class EquipmentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data.copy()

        # Supprimer les anciennes photos si de nouvelles photos sont téléchargées
        if 'photos' in request.FILES:
            instance.photos.all().delete()  # Suppression des anciennes photos

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Traitement des nouvelles photos
        if 'photos' in request.FILES:
            for photo in request.FILES.getlist('photos'):
                Photo.objects.create(equipment=instance, image=photo)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)


logger = logging.getLogger(__name__)

class SurfSessionUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SurfSession.objects.all()
    serializer_class = SurfSessionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        logger.info("Starting the update process for surf session.")

        user = request.user
        surf_club = get_object_or_404(SurfClub, user=user)
        logger.info(f"Surf club ID {surf_club.id} associated with the current user.")

        surf_session = self.get_object()
        logger.info(f"Fetched SurfSession with ID {surf_session.id}.")

        new_monitor_id = request.data.get('monitor')
        logger.info(f"Current monitor ID: {surf_session.monitor.id}, New monitor ID from request: {new_monitor_id}")

        if new_monitor_id and new_monitor_id != str(surf_session.monitor.id):
            logger.info("Monitor change detected, processing monitor update.")
            try:
                old_monitor = surf_session.monitor
                old_monitor.active = False
                old_monitor.save()
                logger.info(f"Old monitor with ID {old_monitor.id} set to inactive.")

                new_monitor = Monitor.objects.get(id=new_monitor_id)
                new_monitor.active = True
                new_monitor.save()
                logger.info(f"New monitor with ID {new_monitor.id} set to active.")
            except Monitor.DoesNotExist:
                logger.error(f"Monitor with ID {new_monitor_id} does not exist.")
                return Response({"error": "Monitor not found."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['surf_club'] = surf_club.id
        logger.info(f"Request data before validation: {data}")

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(surf_session, data=data, partial=partial)
        if serializer.is_valid():
            logger.info("Data is valid, saving the surf session.")
            self.perform_update(serializer)
            logger.info("Surf session updated successfully.")
            return Response(serializer.data)
        else:
            logger.error(f"Data validation failed with errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        logger.info("Starting the delete process for surf session.")

        surf_session = self.get_object()
        monitor = surf_session.monitor

        # Set the monitor to inactive
        monitor.active = False
        monitor.save()
        logger.info(f"Monitor with ID {monitor.id} set to inactive.")

        response = super().destroy(request, *args, **kwargs)
        logger.info("Surf session deleted successfully.")
        return response

class LessonScheduleUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonSchedule.objects.all()
    serializer_class = LessonScheduleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
logger = logging.getLogger(__name__)

class MonitorUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        print(request.data)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            logger.debug(f"Update successful: {serializer.data}")
            return Response(serializer.data)
        else:
            logger.error(f"Update failed with errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_orders(request):
    try:
        surf_club = SurfClub.objects.get(user=request.user)
        orders = Order.objects.filter(surf_club=surf_club)
        orders_serializer = GetOrderSerializer(orders, many=True)
        return Response({
            'orders': orders_serializer.data
        }, status=status.HTTP_200_OK)
    except SurfClub.DoesNotExist:
        return Response({"error": "Surf club not found."}, status=status.HTTP_404_NOT_FOUND)
    except Order.DoesNotExist:
        return Response({"error": "Orders not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def surfclub_orderItems(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        order_items = OrderItem.objects.filter(order=order)
        order_items_serializer = GetOrderItemSerializer(order_items, many=True)
        return Response({
            'orderItems': order_items_serializer.data
        }, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    except OrderItem.DoesNotExist:
        return Response({"error": "Order items not found."}, status=status.HTTP_404_NOT_FOUND)



class ContactView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message received successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_surfer(request):
    if request.method == 'DELETE':
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            surfer = Surfer.objects.get(user=user)
            surfer.delete()
            user.delete()
            return Response({'message': 'Surfer and user deleted successfully'}, status=200)
        except Surfer.DoesNotExist:
            return Response({'error': 'Surfer not found'}, status=404)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_surfclub(request):
    if request.method == 'DELETE':
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            surfclub = SurfClub.objects.get(user=user)
            surfclub.delete()
            user.delete()
            return Response({'message': 'Surf club and user deleted successfully'}, status=200)
        except SurfClub.DoesNotExist:
            return Response({'error': 'Surf club not found'}, status=404)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class ChatbotView(APIView):
    """Vue pour l'API du chatbot IA"""
    
    def post(self, request):
        """Traite un message utilisateur et retourne une réponse du chatbot"""
        try:
            message = request.data.get('message', '').strip()
            session_id = request.data.get('session_id')
            use_llm = request.data.get('use_llm', None)
            user_id = request.user.id if request.user.is_authenticated else None
            
            if not message:
                return Response({'error': 'Message requis'}, status=400)
            
            # Créer ou récupérer la conversation
            if not session_id:
                session_id = str(uuid.uuid4())
            
            conversation, created = ChatbotConversation.objects.get_or_create(
                session_id=session_id,
                defaults={'user_id': user_id}
            )
            
            # Sauvegarder le message utilisateur
            user_message = ChatbotMessage.objects.create(
                conversation=conversation,
                message_type='user',
                content=message
            )
            
            # Traiter le message avec l'IA
            ai_response = chatbot_ai.process_message(message, user_id, use_llm=use_llm)
            
            # Sauvegarder la réponse du bot
            bot_message = ChatbotMessage.objects.create(
                conversation=conversation,
                message_type='bot',
                content=ai_response['response']
            )
            
            # Mettre à jour la conversation
            conversation.save()
            
            return Response({
                'response': ai_response['response'],
                'intent': ai_response['intent'],
                'confidence': ai_response['confidence'],
                'session_id': session_id,
                'suggested_questions': chatbot_ai.get_suggested_questions()
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def get(self, request):
        """Récupère l'historique d'une conversation"""
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response({'error': 'Session ID requis'}, status=400)
        
        try:
            conversation = ChatbotConversation.objects.get(session_id=session_id)
            messages = conversation.messages.all()
            
            message_history = []
            for msg in messages:
                message_history.append({
                    'type': msg.message_type,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat()
                })
            
            return Response({
                'session_id': session_id,
                'messages': message_history,
                'suggested_questions': chatbot_ai.get_suggested_questions()
            })
            
        except ChatbotConversation.DoesNotExist:
            return Response({'error': 'Conversation non trouvée'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class ChatbotFAQView(APIView):
    """Vue pour gérer la FAQ du chatbot"""
    
    def get(self, request):
        """Récupère toutes les questions/réponses de la FAQ"""
        try:
            faqs = ChatbotFAQ.objects.filter(is_active=True)
            serializer = ChatbotFAQSerializer(faqs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def post(self, request):
        """Ajoute une nouvelle question/réponse à la FAQ"""
        if not request.user.is_staff:
            return Response({'error': 'Accès non autorisé'}, status=403)
        
        try:
            serializer = ChatbotFAQSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class ChatbotAnalyticsView(APIView):
    """Vue pour les analyses du chatbot (statistiques d'utilisation)"""
    
    def get(self, request):
        """Récupère les statistiques d'utilisation du chatbot"""
        if not request.user.is_staff:
            return Response({'error': 'Accès non autorisé'}, status=403)
        
        try:
            total_conversations = ChatbotConversation.objects.count()
            total_messages = ChatbotMessage.objects.count()
            user_messages = ChatbotMessage.objects.filter(message_type='user').count()
            bot_messages = ChatbotMessage.objects.filter(message_type='bot').count()
            
            # Intents les plus fréquents
            from django.db.models import Count
            recent_messages = ChatbotMessage.objects.filter(
                message_type='user',
                timestamp__gte=timezone.now() - timezone.timedelta(days=7)
            )
            
            # Analyse des mots-clés populaires
            popular_keywords = []
            for msg in recent_messages[:100]:  # Limiter pour les performances
                words = msg.content.lower().split()
                popular_keywords.extend([w for w in words if len(w) > 3])
            
            from collections import Counter
            keyword_counts = Counter(popular_keywords).most_common(10)
            
            return Response({
                'total_conversations': total_conversations,
                'total_messages': total_messages,
                'user_messages': user_messages,
                'bot_messages': bot_messages,
                'popular_keywords': [{'word': word, 'count': count} for word, count in keyword_counts],
                'recent_activity': {
                    'last_7_days_messages': recent_messages.count(),
                    'active_conversations': ChatbotConversation.objects.filter(
                        updated_at__gte=timezone.now() - timezone.timedelta(hours=24)
                    ).count()
                }
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class WindyForecastView(APIView):
    """Vue pour les prévisions météo Windy"""
    
    def get(self, request):
        """Récupère les prévisions météo pour un spot"""
        spot_name = request.query_params.get('spot')
        days = int(request.query_params.get('days', 3))
        
        if not spot_name:
            return Response({'error': 'Paramètre "spot" requis'}, status=400)
        
        try:
            forecast = windy_service.get_spot_forecast(spot_name, days)
            return Response(forecast)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def post(self, request):
        """Récupère les prévisions par coordonnées"""
        lat = request.data.get('lat')
        lon = request.data.get('lon')
        days = request.data.get('days', 3)
        
        if not lat or not lon:
            return Response({'error': 'Paramètres "lat" et "lon" requis'}, status=400)
        
        try:
            forecast = windy_service.get_surf_forecast(float(lat), float(lon), days)
            return Response(forecast)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class WindyOptimalTimesView(APIView):
    """Vue pour les meilleurs moments pour surfer"""
    
    def get(self, request):
        """Récupère les meilleurs moments pour surfer sur un spot"""
        spot_name = request.query_params.get('spot')
        days = int(request.query_params.get('days', 3))
        
        if not spot_name:
            return Response({'error': 'Paramètre "spot" requis'}, status=400)
        
        try:
            # Obtenir les coordonnées du spot
            forecast = windy_service.get_spot_forecast(spot_name, 1)
            if not forecast.get('success'):
                return Response({'error': f'Spot "{spot_name}" non trouvé'}, status=404)
            
            spot_info = forecast['spot_info']
            optimal_times = windy_service.get_optimal_surf_times(
                spot_info['lat'], 
                spot_info['lon'], 
                days
            )
            
            return Response(optimal_times)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class WindyConditionsSummaryView(APIView):
    """Vue pour le résumé des conditions de surf"""
    
    def get(self, request):
        """Génère un résumé des conditions pour un spot"""
        spot_name = request.query_params.get('spot')
        
        if not spot_name:
            return Response({'error': 'Paramètre "spot" requis'}, status=400)
        
        try:
            summary = windy_service.get_surf_conditions_summary(spot_name)
            return Response({
                'spot': spot_name,
                'summary': summary,
                'generated_at': datetime.now().isoformat()
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)


######################## IA - Prévision de demande / prix ########################
class AIDemandForecastView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retourne une prévision simple de la demande et un prix suggéré.
        Si le modèle est indisponible, renvoie des valeurs simulées.
        """
        try:
            # Contexte minimal: club courant
            try:
                club = SurfClub.objects.get(user=request.user)
                club_name = club.name
            except SurfClub.DoesNotExist:
                club_name = "Votre club"

            prediction = None
            suggestion = None
            
            # Pour l'instant, utiliser directement le fallback simulé
            # TODO: Implémenter la vraie logique de prédiction plus tard
            history = [21, 24, 28, 35, 42, 48]
            prediction = {
                'this_week': history[-1],
                'next_week': int(history[-1] * 1.33),
                'trend': '+33%',
                'history': history
            }
            suggestion = 29.9

            return Response({
                'club': club_name,
                'demand_forecast': prediction,
                'suggested_price': suggestion,
                'generated_at': datetime.now().isoformat()
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)
