from django.contrib.sitemaps import Sitemap
from .models import Artikull, Kategoria

class ArtikullSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Artikull.objects.all().order_by('-data_publikimit')

    def lastmod(self, obj):
        return obj.data_publikimit

class KategoriaSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Kategoria.objects.all()