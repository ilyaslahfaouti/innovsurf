from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time

from AppWeb.models import (
    CustomUser, SurfSpot, SurfClub, EquipmentType, Equipment,
    Surfer, Monitor, LessonSchedule, SurfSession,
)


class Command(BaseCommand):
    help = "Seed demo data for InnovSurf: spots, clubs, equipment, users, sessions"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding InnovSurf demo data..."))

        # Admin user
        admin_email = "admin@innovsurf.com"
        admin, _ = CustomUser.objects.get_or_create(
            email=admin_email,
            defaults={"is_staff": True, "is_superuser": True}
        )
        if not admin.has_usable_password():
            admin.set_password("admin123")
            admin.save()
        self.stdout.write(self.style.SUCCESS(f"Admin ready: {admin_email} / admin123"))

        # Surfer user
        surfer_user, _ = CustomUser.objects.get_or_create(
            email="surfer@innovsurf.com",
            defaults={"is_surfer": True}
        )
        if not surfer_user.has_usable_password():
            surfer_user.set_password("surfer123")
            surfer_user.save()
        surfer, _ = Surfer.objects.get_or_create(
            user=surfer_user,
            defaults={
                "firstname": "Sam",
                "lastname": "Rider",
                "birthday": date(2000, 1, 1),
                "level": "intermediate",
            },
        )

        # Spots
        spots_data = [
            {
                "name": "Taghazout",
                "zip_code": "80022",
                "address": "Taghazout, Morocco",
                "description": "World-class right-handers",
                "latitude": 30.542,
                "longitude": -9.710,
            },
            {
                "name": "Agadir",
                "zip_code": "80000",
                "address": "Agadir, Morocco",
                "description": "Beach breaks and mellow waves",
                "latitude": 30.427,
                "longitude": -9.598,
            },
        ]
        spots = []
        for sd in spots_data:
            spot, _ = SurfSpot.objects.get_or_create(name=sd["name"], defaults=sd)
            spots.append(spot)
        self.stdout.write(self.style.SUCCESS(f"Spots ready: {[s.name for s in spots]}"))

        # Club owners (distinct users because SurfClub.user is OneToOne)
        club_user1, _ = CustomUser.objects.get_or_create(
            email="club1@innovsurf.com",
            defaults={"is_surfclub": True}
        )
        if not club_user1.has_usable_password():
            club_user1.set_password("club123")
            club_user1.save()

        club_user2, _ = CustomUser.objects.get_or_create(
            email="club2@innovsurf.com",
            defaults={"is_surfclub": True}
        )
        if not club_user2.has_usable_password():
            club_user2.set_password("club123")
            club_user2.save()

        # Clubs
        club_1, _ = SurfClub.objects.get_or_create(
            user=club_user1,
            defaults={
                "name": "InnovSurf Club Taghazout",
                "surf_spot": spots[0],
            },
        )
        club_2, _ = SurfClub.objects.get_or_create(
            user=club_user2,
            defaults={
                "name": "InnovSurf Club Agadir",
                "surf_spot": spots[1],
            },
        )

        # Equipment types
        types = {}
        for t in ("surfboard", "leash", "surfsuit"):
            et, _ = EquipmentType.objects.get_or_create(type=t)
            types[t] = et

        # Equipment inventory
        eq_list = [
            {"name": "Shortboard 6'0", "description": "Fast and agile", "size": "6'0", "state": "good", "material_type": "rent", "equipment_type": types["surfboard"], "surf_club": club_1, "rent_price": 15, "quantity": 5},
            {"name": "Longboard 9'0", "description": "Stable and easy", "size": "9'0", "state": "excellent", "material_type": "rent", "equipment_type": types["surfboard"], "surf_club": club_1, "rent_price": 20, "quantity": 3},
            {"name": "Leash 6'", "description": "Standard leash", "size": "6'", "state": "new", "material_type": "sale", "equipment_type": types["leash"], "surf_club": club_1, "sale_price": 25, "quantity": 10},
            {"name": "Wetsuit M", "description": "3/2mm", "size": "M", "state": "good", "material_type": "rent", "equipment_type": types["surfsuit"], "surf_club": club_2, "rent_price": 12, "quantity": 7},
        ]
        for e in eq_list:
            Equipment.objects.get_or_create(
                name=e["name"],
                surf_club=e["surf_club"],
                defaults=e,
            )

        # Monitors
        mon_1, _ = Monitor.objects.get_or_create(
            first_name="Youssef", last_name="A.", birthday=date(1995, 5, 10), active=True, surf_club=club_1
        )
        mon_2, _ = Monitor.objects.get_or_create(
            first_name="Sara", last_name="B.", birthday=date(1998, 7, 20), active=True, surf_club=club_2
        )

        # Schedules and sessions (today)
        ls1, _ = LessonSchedule.objects.get_or_create(
            surf_club=club_1, day=date.today(), start_time=time(9, 0), end_time=time(11, 0)
        )
        ls2, _ = LessonSchedule.objects.get_or_create(
            surf_club=club_1, day=date.today(), start_time=time(14, 0), end_time=time(16, 0)
        )
        SurfSession.objects.get_or_create(surf_club=club_1, monitor=mon_1, lesson_schedule=ls1)
        SurfSession.objects.get_or_create(surf_club=club_1, monitor=mon_1, lesson_schedule=ls2)

        self.stdout.write(self.style.SUCCESS("Seed complete."))


