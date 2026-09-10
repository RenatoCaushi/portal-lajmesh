import os
import django
import cloudinary
import cloudinary.uploader

# Konfiguro mjedisin e Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_lajmesh.settings')
django.setup()

from django.conf import settings

# Konfiguro Cloudinary me të dhënat nga settings.py
cloudinary.config(
    cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
    api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
)

media_dir = os.path.join(settings.BASE_DIR, 'static', 'media')

print(f"Po nis ngarkimi i skedarëve nga: {media_dir}\n")

if not os.path.exists(media_dir):
    print("Dosja media/ nuk u gjet lokalit!")
else:
    for root, dirs, files in os.walk(media_dir):
        for file in files:
            local_path = os.path.join(root, file)
            # Ruan strukturën e dosjeve brenda media/
            relative_path = os.path.relpath(local_path, media_dir)
            public_id = os.path.splitext(relative_path)[0].replace('\\', '/')
            
            print(f"Po ngarkohet: {relative_path} ...")
            try:
                cloudinary.uploader.upload(
                    local_path,
                    public_id=public_id,
                    use_filename=True,
                    unique_filename=False
                )
                print(f"✅ U ngarkua me sukses: {public_id}")
            except Exception as e:
                print(f"❌ Gabim gjatë ngarkimit të {relative_path}: {e}")

print("\nPërfundoi ngarkimi i të gjitha fotove te Cloudinary!")