from django.conf import settings


def site(request):
    return {
        "static_url": settings.STATIC_URL,
        "env": settings.ENV,
    }
