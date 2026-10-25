import os

from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .models import Media

MAX_MB = 10
PER_PAGE = 40


def _item(m):
    return {"id": m.id, "titulli": str(m), "url": m.skedari.url}


@staff_member_required
@require_GET
def media_lista(request):
    q = request.GET.get("q", "").strip()
    qs = Media.objects.all()
    if q:
        qs = qs.filter(titulli__icontains=q)

    paginator = Paginator(qs, PER_PAGE)
    page = paginator.get_page(request.GET.get("page", 1))
    return JsonResponse({
        "items": [_item(m) for m in page.object_list],
        "has_next": page.has_next(),
    })


@staff_member_required
@require_POST
def media_ngarko(request):
    files = request.FILES.getlist("skedari")
    if not files:
        return JsonResponse(
            {"items": [], "errors": ["Nuk u zgjodh asnjë skedar."]}, status=400
        )

    validator = forms.ImageField()
    items, errors = [], []

    for f in files[:20]:
        if f.size > MAX_MB * 1024 * 1024:
            errors.append(f"{f.name}: është më i madh se {MAX_MB} MB.")
            continue
        try:
            validator.clean(f)
        except ValidationError:
            errors.append(f"{f.name}: nuk është foto e vlefshme.")
            continue
        f.seek(0)
        m = Media.objects.create(
            titulli=os.path.splitext(f.name)[0][:200],
            skedari=f,
        )
        items.append(_item(m))

    return JsonResponse({"items": items, "errors": errors})