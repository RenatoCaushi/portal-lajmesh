from django.contrib import admin
from .models import Kategoria, Artikull, Koment, Video, Reklama

@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'emri')
    search_fields = ('emri',)

@admin.register(Artikull)
class ArtikullAdmin(admin.ModelAdmin):
    list_display = ('titulli', 'kategoria', 'data_publikimit', 'shikime')
    list_filter = ('kategoria', 'data_publikimit')
    search_fields = ('titulli', 'permbajtja')
    readonly_fields = ('shikime',)

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