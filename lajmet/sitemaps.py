from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Artikull, Kategoria

class ArtikullSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Artikull.objects.all().order_by('-data_publikimit')

    def lastmod(self, obj):
        return obj.data_publikimit

    def location(self, obj):
        # Përdorim pk (id) për të shmangur çdo gabim fushash
        return reverse('detajet_e_lajmit', args=[obj.pk])

class KategoriaSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Kategoria.objects.all()

    def location(self, obj):
        return f"/?kategoria={obj.id}"