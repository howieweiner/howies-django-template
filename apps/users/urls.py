from django.urls import path

from .views.manage import UserListView, UserCreateView, UserUpdateView, UserDeleteView
from .views.profile import ProfileUpdateView

app_name = "users"

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("create", UserCreateView.as_view(), name="user-create"),
    path("edit/<int:pk>", UserUpdateView.as_view(), name="user-update"),
    path("<int:pk>/delete", UserDeleteView.as_view(), name="user-delete"),
    path("profile", ProfileUpdateView.as_view(), name="profile-update"),
]
