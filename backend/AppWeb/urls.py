from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import token_obtain_pair

from .views import register, login_view, get_surfclub_profile, surfclub_monitors, surfclub_monitor, \
    surfclub_equipements, surfclub_equipment, surfclub_LessonSchedules, \
    surfclub_LessonSchedule, surfclub_SurfLessons, surfclub_SurfLesson, update_surfclub_profile, \
    update_surfer_profile, add_monitor_to_surfclub, add_equipment, add_lesson_schedule, surfclub_statistics, \
    get_surfspots, get_surfspot, book_surf_lesson, get_surfclub_lesson, create_order, \
    get_forum_details, create_message, surfclub_SurfSessions, EquipmentUpdateDeleteView, \
    SurfSessionUpdateDeleteView, LessonScheduleUpdateDeleteView, MonitorUpdateDeleteView, surfclub_equipement_types, \
    create_surf_session, surfclub_SurfSession, surfclub_orders, surfclub_orderItems, get_surfclub_equipments_buy, \
    surf_spot_details, get_surfer_profile, get_order_details, get_new_messages, ContactView, surfclub_monitors_dispo, \
    delete_surfclub, delete_surfer, ChatbotView, ChatbotFAQView, ChatbotAnalyticsView, WindyForecastView, WindyOptimalTimesView, WindyConditionsSummaryView, AIDemandForecastView

urlpatterns = [
    #####Urls for users#####
    path('user/register/', register, name='register'),
    path('user/login/', login_view, name='login_view'),
    path('token/', token_obtain_pair, name='token_obtain_pair'),

    ##### GET URLs for surf club#####
    path('surf-club/profile/',get_surfclub_profile,name='get_surfclub_profile'),
    path('surf-club/monitors/',surfclub_monitors,name='surfclub_monitors'),
    path('surf-club/monitors-dispo/', surfclub_monitors_dispo, name='surfclub_monitors_dispo'),
    path('surf-club/monitors/<int:pk>/', surfclub_monitor, name='surfclub_monitor'),
    path('surf-club/equipment-types/', surfclub_equipement_types, name='surfclub_equipement_types'),
    path('surf-club/equipments/', surfclub_equipements, name='surfclub_equipments'),
    path('surf-club/equipments/<int:pk>/', surfclub_equipment, name='surfclub_equipment'),
    path('surf-club/lesson-schedules/', surfclub_LessonSchedules, name='surfclub_LessonSchedules'),
    path('surf-club/lesson-schedules/<int:pk>/', surfclub_LessonSchedule, name='surfclub_LessonSchedule'),
    path('surf-club/surf-sessions/', surfclub_SurfSessions, name='surfclub_SurfSessions'),
    path('surf-club/surf-sessions/<int:pk>/', surfclub_SurfSession, name='surfclub_SurfSession'),
    path('surf-club/surf-lessons/', surfclub_SurfLessons, name='surfclub_SurfLessons'),
    path('surf-club/orders/', surfclub_orders, name='surfclub_orders'),
    path('surf-club/orders/<int:pk>/', surfclub_orderItems, name='surfclub_orderItems'),
    path('surf-club/surf-lessons/<int:pk>/', surfclub_SurfLesson, name='surfclub_SurfLesson'),
    path('surf-club/statistics/', surfclub_statistics, name='surfclub_statistics'),
    path('surf-spots/', get_surfspots, name='surfspots'),
    ##### Update Profiles for surfers and surf clubs#####
    path('surf-club/profile/update/',update_surfclub_profile,name='update_surfclub_profile'),
    path('surfers/order/<int:order_id>/', get_order_details, name='get_order_details'),
    path('surfer/profile/update/', update_surfer_profile, name='update_surfer_profile'),
    ##### POST Urls for surf-club#####
    path('surf-club/add-monitor/',add_monitor_to_surfclub,name='add_monitor_to_surfclub'),
    path('surf-club/add-equipment/', add_equipment, name='add_equipment'),
    path('surf-club/add-lesson-schedule/', add_lesson_schedule, name='add_lesson_schedule'),
    path('surf-club/add-surf-session/', create_surf_session, name='create_surf_session'),

    ##### Get for Surfers #####
    path('surf-clubs/<int:pk>/lessons/', get_surfclub_lesson, name='get_surfclub_lesson'),
    path('surf-clubs/<int:pk>/equipments/', get_surfclub_equipments_buy, name='get_surfclub_equipments_buy'),
    path('surfer/profile/', get_surfer_profile, name='update_surfer_profile'),
    path('surf-spots/<int:pk>/', get_surfspot, name='get_surfspot'),
    path('surf-spots/prevision/<int:pk>/', surf_spot_details, name='surf_spot_details'),
    path('forums/<int:surf_spot_id>/messages/', get_new_messages, name='get_new_messages'),
    path('forums/<int:surf_spot_id>/', get_forum_details, name='get_forum_details'),
    #####POST for surfers #####
    path('surfers/book_surf_lesson/', book_surf_lesson, name='book_surf_lesson'),
    path('surfers/add-order/', create_order, name='create_order'),
    path('forums/<int:forum_id>/messages/create/', create_message, name='create_message'),
    ########Update and Delete#########
    path('surf-club/equipment/<int:pk>/', EquipmentUpdateDeleteView.as_view(), name='equipment-update-delete'),
    path('surf-club/surf-session/<int:pk>/', SurfSessionUpdateDeleteView.as_view(), name='surf-session-update-delete'),
    path('surf-club/lesson-schedule/<int:pk>/', LessonScheduleUpdateDeleteView.as_view(), name='lesson-schedule-update-delete'),
    path('surf-club/monitor/<int:pk>/', MonitorUpdateDeleteView.as_view(), name='monitor-update-delete'),
    path('surf-club/delete/', delete_surfclub, name='delete_surfclub'),
    path('surfer/delete/', delete_surfer, name='delete_surfer'),
    ########Contact form########
    path('contact/', ContactView.as_view(), name='contact_form'),

    # Chatbot IA
    path('chatbot/', ChatbotView.as_view(), name='chatbot'),
    path('chatbot/faq/', ChatbotFAQView.as_view(), name='chatbot-faq'),
    path('chatbot/analytics/', ChatbotAnalyticsView.as_view(), name='chatbot-analytics'),

    # API Windy - Prévisions météo
    path('windy/forecast/', WindyForecastView.as_view(), name='windy-forecast'),
    path('windy/optimal-times/', WindyOptimalTimesView.as_view(), name='windy-optimal-times'),
    path('windy/conditions-summary/', WindyConditionsSummaryView.as_view(), name='windy-conditions-summary'),
    # IA - Prévisions de demande/prix
    path('ai/demand-forecast/', AIDemandForecastView.as_view(), name='ai-demand-forecast'),
]
