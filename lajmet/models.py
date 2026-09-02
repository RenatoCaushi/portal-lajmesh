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
    foto = models.ImageField(upload_to='lajmet/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Artikujt"

    def __str__(self):
        return self.titulli

from django.db import models

class Koment(models.Model):
    artikulli = models.ForeignKey('Artikull', on_delete=models.CASCADE, related_name='komentet')
    emri = models.CharField(max_length=100, default="Anonim", blank=True, null=True)
    permbajtja = models.TextField()  # <--- Sigurohu qe eshte me 'e' dhe jo 'ë' apo emer tjeter
    data_publikimit = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, verbose_name="I aprovuar")

    def __str__(self):
        return f"Koment te {self.artikulli.titulli}"
