import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from AppWeb.models import SurfSpot, Photo


class Command(BaseCommand):
    help = "Attach demo photos to surf spots (copies files into media/uploads and creates Photo objects)."

    def handle(self, *args, **options):
        media_uploads = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(media_uploads, exist_ok=True)

        # Map of spot name (lower) -> source image absolute path
        project_root = os.path.abspath(os.path.join(settings.BASE_DIR))
        assets = os.path.join(project_root, '..', 'frontend', 'src', 'assets')
        candidates = {
            'taghazout': os.path.join(assets, 'taghazout.jpg'),
            'agadir': os.path.join(assets, 'agadir.jpg'),
            'bouznika': os.path.join(assets, 'bouznika.jpg'),
        }

        created = 0
        for spot in SurfSpot.objects.all():
            name_key = spot.name.lower()
            src = candidates.get(name_key)
            if not src or not os.path.isfile(src):
                continue
            dest_name = f"spot_{name_key}.jpg"
            dest_path = os.path.join(media_uploads, dest_name)
            if not os.path.isfile(dest_path):
                shutil.copy2(src, dest_path)
                self.stdout.write(self.style.NOTICE(f"Copied {src} -> {dest_path}"))

            # Create photo if not existing
            rel_path = f"uploads/{dest_name}"
            if not Photo.objects.filter(surf_spot=spot, image=rel_path).exists():
                Photo.objects.create(surf_spot=spot, image=rel_path)
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Spot photos attached. New photos: {created}"))


