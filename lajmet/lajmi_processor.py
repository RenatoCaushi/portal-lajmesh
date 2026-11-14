from .models import LajmIFundit


def lajmi_i_fundit_processor(request):
    """Vendos lajmin urgjent aktiv (me te riun) ne te gjitha template-t."""
    lajmi = LajmIFundit.objects.filter(eshte_aktiv=True).first()
    return {"lajmi_i_fundit": lajmi}