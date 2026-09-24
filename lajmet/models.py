import re
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Kategoria(models.Model):
    emri = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Kategoritë"

    def __str__(self):
        return self.emri


class Artikull(models.Model):
    titulli = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    permbajtja = models.TextField()
    data_publikimit = models.DateTimeField(auto_now_add=True)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to="lajmet/", blank=True, null=True)
    
    eshte_premium = models.BooleanField(
        default=False, 
        verbose_name="Artikull Premium (Paywall)", 
        help_text="Zgjidhni nëse ky artikull kërkon abonim/pagesë për t'u lexuar plotësisht."
    )

    youtube_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="YouTube Video ID",
        help_text=(
            "Shkruaj vetëm ID-në e videos (p.sh. për linkun"
            " https://www.youtube.com/watch?v=dQw4w9WgXcQ vendos vetëm"
            " dQw4w9WgXcQ)"
        ),
    )

    class Meta:
        verbose_name_plural = "Artikujt"

    def __str__(self):
        return self.titulli

    def get_absolute_url(self):
        return reverse('detajet_e_lajmit', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulli)
            if not base_slug:
                base_slug = "lajm"
            slug = base_slug
            count = 1
            while Artikull.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def permbajtja_me_embeds(self):
        pass