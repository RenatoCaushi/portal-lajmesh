import re
from django.db import models


class Kategoria(models.Model):
  emri = models.CharField(max_length=50)

  class Meta:
    verbose_name_plural = "Kategoritë"

  def __str__(self):
    return self.emri


class Artikull(models.Model):
  titulli = models.CharField(max_length=200)
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

# --- MODELI I RI PËR NJOFTIMET (PUSH NOTIFICATIONS) ---
class PushNotificationSubscription(models.Model):
    onesignal_player_id = models.CharField(
        max_length=255, unique=True, verbose_name="OneSignal Player ID"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data e regjistrimit")

    class Meta:
        verbose_name = "Abonim Njoftimesh"
        verbose_name_plural = "Abonimet e Njoftimeve"

    def __str__(self):
        return f"Abonues - {self.onesignal_player_id[:10]}..."