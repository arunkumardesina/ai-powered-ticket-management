from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    return JsonResponse({"status": "ok", "service": "AI Ticket Management API"})


urlpatterns = [path("admin/", admin.site.urls), path("api/health/", health_check, name="health"), path("api/auth/", include("accounts.urls"))]
