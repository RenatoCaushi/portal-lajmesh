from django.db import migrations


def kalo_fotot(apps, schema_editor):
    Artikull = apps.get_model("lajmet", "Artikull")
    Media = apps.get_model("lajmet", "Media")
    for art in Artikull.objects.exclude(foto="").exclude(foto__isnull=True):
        if not art.foto_media_id:
            m = Media.objects.create(titulli=art.titulli[:200], skedari=art.foto.name)
            art.foto_media = m
            art.save(update_fields=["foto_media"])


class Migration(migrations.Migration):

    dependencies = [
        ("lajmet", "0016_media_artikull_foto_media"),
    ]

    operations = [
        migrations.RunPython(kalo_fotot, migrations.RunPython.noop),
    ]
