from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Kategoria, Artikull, Koment, Video, Reklama, Media
from .widgets import MediaPickerWidget


@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'emri')
    search_fields = ('emri',)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('miniatura', 'titulli', 'data_ngarkimit')
    search_fields = ('titulli', 'skedari')
    readonly_fields = ('miniatura',)

    def miniatura(self, obj):
        if obj.skedari:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:4px;">',
                obj.skedari.url,
            )
        return "-"
    miniatura.short_description = "Pamja"


class ArtikullAdminForm(forms.ModelForm):
    class Meta:
        model = Artikull
        fields = "__all__"
        widgets = {"foto_media": MediaPickerWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Heq ikonat "+", "ndrysho", "fshi" pranë fushës së fotos
        widget = self.fields["foto_media"].widget
        for attr in ("can_add_related", "can_change_related",
                     "can_delete_related", "can_view_related"):
            if hasattr(widget, attr):
                setattr(widget, attr, False)


@admin.register(Artikull)
class ArtikullAdmin(admin.ModelAdmin):
    form = ArtikullAdminForm
    list_display = ('titulli', 'kategoria', 'data_publikimit', 'eshte_premium')
    list_filter = ('kategoria', 'eshte_premium', 'data_publikimit')
    search_fields = ('titulli', 'permbajtja')
    ordering = ('-data_publikimit',)
    prepopulated_fields = {'slug': ('titulli',)}


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