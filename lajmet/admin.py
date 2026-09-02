from django.contrib import admin
from .models import Artikull, Kategoria, Koment

@admin.register(Koment)
class KomentAdmin(admin.ModelAdmin):
    list_display = ('emri', 'artikulli', 'data_publikimit', 'is_approved')
    list_filter = ('is_approved', 'data_publikimit')
    search_fields = ('emri', 'permbajtja')
    actions = ['aprovo_komentet', 'blloko_komentet']

    def aprovo_komentet(self, request, queryset):
        queryset.update(is_approved=True)
    aprovo_komentet.short_description = "Aprovo komentet e zgjedhura"

    def blloko_komentet(self, request, queryset):
        queryset.update(is_approved=False)
    blloko_komentet.short_description = "Blloko/Fshih komentet e zgjedhura"
