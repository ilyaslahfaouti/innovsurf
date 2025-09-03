#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innovsurf.settings')
django.setup()

from AppWeb.models import LessonSchedule, SurfClub

def create_test_lessons():
    try:
        club = SurfClub.objects.get(name='InnovSurf Club Taghazout')
        print(f'Création de leçons pour {club.name}')
        
        # Supprimer les anciennes leçons de test
        LessonSchedule.objects.filter(surf_club=club).delete()
        print('Anciennes leçons supprimées')
        
        # Créer des leçons sur 6 semaines
        base_date = datetime.now() - timedelta(weeks=6)
        
        for i in range(6):
            week_date = base_date + timedelta(weeks=i)
            lessons_count = random.randint(15, 35)
            
            for j in range(lessons_count):
                lesson_date = week_date + timedelta(days=random.randint(0, 6))
                start_time = f"{random.randint(8, 18):02d}:00"
                end_time = f"{random.randint(9, 19):02d}:00"
                
                LessonSchedule.objects.create(
                    surf_club=club,
                    start_time=start_time,
                    end_time=end_time,
                    day=lesson_date
                )
            
            print(f'Semaine {i+1}: {lessons_count} leçons créées')
        
        print('✅ Leçons créées avec succès!')
        
        # Vérifier
        total_lessons = LessonSchedule.objects.filter(surf_club=club).count()
        print(f'Total des leçons: {total_lessons}')
        
    except Exception as e:
        print(f'Erreur: {e}')

if __name__ == '__main__':
    create_test_lessons()
