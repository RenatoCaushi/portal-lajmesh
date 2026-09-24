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
        teksti = self.permbajtja
        insta_pattern = r"(https?://(?:www\.)?instagram\.com/(?:p|reel)/([^/?#&]+)/?)"
        insta_embed = (
            r'<blockquote class="instagram-media" data-instgrm-permalink="\1"'
            r' data-instgrm-version="14" style="background:#FFF; border:0;'
            r' border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0'
            r' rgba(0,0,0,0.15); margin: 15px auto; max-width:540px;'
            r' min-width:326px; padding:0; width:99.375%;"><a href="\1"'
            r' target="_blank"></a></blockquote>'
        )
        teksti = re.sub(insta_pattern, insta_embed, teksti)

        fb_reel_pattern = r"(https?://(?:www\.)?facebook\.com/(?:reel|watch|videos)/[^/\s]+/?)"
        fb_reel_embed = (
            r'<iframe src="https://www.facebook.com/plugins/video.php?href=\1&show_text=false&width=350"'
            r' width="350" height="500" style="border:none;overflow:hidden;display:block;margin:20px auto;"'
            r' scrolling="no" frameborder="0" allowfullscreen="true"'
            r' allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>'
        )
        teksti = re.sub(fb_reel_pattern, fb_reel_embed, teksti)

        fb_post_pattern = r"(https?://(?:www\.)?facebook\.com/[^/\s]+/posts/[^/\s]+/?)"
        fb_post_embed = r'<div class="fb-post mb-3 d-flex justify-content-center" data-href="\1" data-width="500"></div>'
        teksti = re.sub(fb_post_pattern, fb_post_embed, teksti)

        teksti = teksti.replace("\r\n", "<br>").replace("\n", "<br>")
        return teksti