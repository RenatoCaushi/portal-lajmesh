from django import forms
from django.urls import reverse

from .models import Media


class MediaPickerWidget(forms.Widget):
    template_name = "lajmet/widgets/media_picker.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        foto = Media.objects.filter(pk=value).first() if value else None
        context["widget"]["foto"] = foto
        context["list_url"] = reverse("media_lista")
        context["upload_url"] = reverse("media_ngarko")
        return context