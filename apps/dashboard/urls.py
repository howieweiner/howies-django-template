from django.urls import path

from apps.dashboard.views import dashboard_view

app_name = "dashboard"

urlpatterns = [
    path("", dashboard_view, name="home"),
]
