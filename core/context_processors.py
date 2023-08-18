from core.models import Hospital


def footer_hospitals(request):
    return {"footer_hospitals": Hospital.objects.all()}
