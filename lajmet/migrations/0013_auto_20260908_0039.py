from django.db import migrations
from django.utils.text import slugify

def gjenero_slugs(apps, schema_editor):
    Artikull = apps.get_model('lajmet', 'Artikull')
    for artikull in Artikull.objects.filter(slug__isnull=True):
        base_slug = slugify(artikull.titulli) or "lajm"
        slug = base_slug
        count = 1
        while Artikull.objects.filter(slug=slug).exclude(id=artikull.id).exists():
            slug = f"{base_slug}-{count}"
            count += 1
        artikull.slug = slug
        artikull.save()

class Migration(migrations.Migration):

    dependencies = [
        ('lajmet', '0012_artikull_slug'),
    ]

    operations = [
        migrations.RunPython(gjenero_slugs),
    ]