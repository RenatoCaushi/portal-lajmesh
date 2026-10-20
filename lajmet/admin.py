from django.contrib import admin
from .models import Kategoria, Artikull, Koment, Video, Reklama

@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'emri')
    search_fields = ('emri',)

@admin.register(Artikull)
class ArtikullAdmin(admin.ModelAdmin):
    # Shtuam fushat e reja në list_display dhe list_filter për kontroll më të mirë
    list_display = ('titulli', 'kategoria', 'data_publikimit', 'eshte_premium')
    list_filter = ('kategoria', 'eshte_premium', 'data_publikimit')
    search_fields = ('titulli', 'permbajtja')
    
    # E hoqëm nga readonly_fields që të mund të caktosh/ndryshosh orarin lirisht (Schedule)
    # readonly_fields = ('data_publikimit',) 
    
    ordering = ('-data_publikimit',)
    prepopulated_fields = {'slug': ('titulli',)} # Gjeneron automatikisht slug-un nga titulli

@admin.register(Koment)
class KomentAdmin(admin.ModelAdmin):
    list_display = ('emri', 'artikulli', 'data_publikimit', 'is_approved')
    list_filter = ('is_approved', 'data_publikimit')
    search_fields = ('emri', 'permbajtja')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulli', 'youtube_id', 'data_publikimit')
    search_fields = ('titulli',)

@admin.register(Reklama)
class ReklamaAdmin(admin.ModelAdmin):
    list_display = ('titulli', 'is_active', 'data_krijimit')
    list_filter = ('is_active', 'data_krijimit')
    search_fields = ('titulli',)
    list_editable = ('is_active',)