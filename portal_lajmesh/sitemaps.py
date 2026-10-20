from django.contrib.sitemaps import Sitemap
from .models import Lajmi # Vendos emrin e modelit tend te lajmeve

class LajmiSitemap(Sitemap):
    changefreq = "hourly"  # Lajmet ndryshojne shpesh
    priority = 0.9

    def items(self):
        return Lajmi.objects.filter(publikuar=True).order_by('-data_publikimit')

    def lastmod(self, obj):
        return obj.data_publikimit