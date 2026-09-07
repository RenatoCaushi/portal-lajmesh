import re
from django.db import models
from django.utils.text import slugify


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
    shikime = models.PositiveIntegerField(
        default=0, verbose_name="Numri i shikimeve"
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

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulli)
            # Nëse titulli përmban vetëm karaktere speciale/shkronja që nuk konvertohen direkt, sigurojmë një fallback
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
        """
        Kjo metodë konverton linkat e thjeshtë të Instagram, Facebook (Reels/Videos/Posts)
        në elemente HTML Embed dhe gjithashtu ruhen kalimet e rreshtave (paragraphs).
        """
        teksti = self.permbajtja

        # 1. Shndërrim i linkave të Instagram (Postime & Reels)
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

        # 2. Shndërrim i Facebook REELS dhe VIDEOVE
        fb_reel_pattern = r"(https?://(?:www\.)?facebook\.com/(?:reel|watch|videos)/[^/\s]+/?)"
        fb_reel_embed = (
            r'<iframe src="https://www.facebook.com/plugins/video.php?href=\1&show_text=false&width=350"'
            r' width="350" height="500" style="border:none;overflow:hidden;display:block;margin:20px auto;"'
            r' scrolling="no" frameborder="0" allowfullscreen="true"'
            r' allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>'
        )
        teksti = re.sub(fb_reel_pattern, fb_reel_embed, teksti)

        # 3. Shndërrim i Facebook Postimeve standarde
        fb_post_pattern = r"(https?://(?:www\.)?facebook\.com/[^/\s]+/posts/[^/\s]+/?)"
        fb_post_embed = r'<div class="fb-post mb-3 d-flex justify-content-center" data-href="\1" data-width="500"></div>'
        teksti = re.sub(fb_post_pattern, fb_post_embed, teksti)

        # 4. Ruan paragrafët e tekstit (kalimet e rreshtit kthehen në <br>)
        teksti = teksti.replace("\r\n", "<br>").replace("\n", "<br>")

        return teksti


class Koment(models.Model):
    artikulli = models.ForeignKey(
        Artikull, on_delete=models.CASCADE, related_name="komentet"
    )
    emri = models.CharField(
        max_length=100, default="Anonim", blank=True, null=True
    )
    permbajtja = models.TextField()
    data_publikimit = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, verbose_name="I aprovuar")

    def __str__(self):
        return f"Koment te {self.artikulli.titulli}"


class Video(models.Model):
    titulli = models.CharField(max_length=200, verbose_name="Titulli i Videos")
    youtube_id = models.CharField(
        max_length=100,
        verbose_name="YouTube Video ID ose Link",
        help_text="Mund të vendosni vetëm ID-në ose të gjithë linkun e YouTube.",
    )
    data_publikimit = models.DateTimeField(
        auto_now_add=True, verbose_name="Data e Publikimit"
    )

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videot"
        ordering = ["-data_publikimit"]

    def save(self, *args, **kwargs):
        # Nxjerr automatikisht ID-në 11-shifrore nga çdo lloj linku
        if self.youtube_id:
            pattern = r"(?:v=|\/([0-9A-Za-z_-]{11}).*|youtu\.be\/)([0-9A-Za-z_-]{11})"
            match = re.search(pattern, self.youtube_id)
            if match:
                self.youtube_id = match.group(2) or match.group(1)
            else:
                self.youtube_id = self.youtube_id.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulli


class Reklama(models.Model):
    titulli = models.CharField(
        max_length=100, verbose_name="Emri i Reklamës / Klientit"
    )
    imazhi = models.ImageField(upload_to="reklama/", verbose_name="Foto Banneri")
    linku = models.URLField(verbose_name="Linku i Destinacionit")
    is_active = models.BooleanField(
        default=True, verbose_name="Aktivizo Reklamën"
    )
    data_krijimit = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reklamë"
        verbose_name_plural = "Reklumat"

    def __str__(self):
        return self.titulli


# --- MODELI PËR RUAJTJEN E ABONIMEVE PUSH (Web Push API) ---
class PushSubscription(models.Model):
    endpoint = models.TextField(unique=True, verbose_name="Endpoint URL")
    p256dh = models.CharField(max_length=255, verbose_name="P256DH Key")
    auth = models.CharField(max_length=255, verbose_name="Auth Key")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data e Regjistrimit")

    class Meta:
        verbose_name = "Abonim Njoftimesh"
        verbose_name_plural = "Abonimet e Njoftimeve"

    def __str__(self):
        return f"Abonues #{self.id}"