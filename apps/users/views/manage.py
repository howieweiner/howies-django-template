from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from apps.core.views.auth_mixins import IsAdminMixin
from apps.core.views.base import BaseAppMixin
from apps.core.views.mixins import (
    PaginationMixin,
    CrispyFormArgsMixin,
    FilterParamsMixin,
)
from apps.core.views.utils import add_page_context_data
from apps.users.forms.user import UserForm
from apps.users.views.filters import UserFilter

User = get_user_model()


class BaseUserMixin(IsAdminMixin, BaseAppMixin):
    model = User
    success_url = reverse_lazy("users:user-list")


class UserListView(BaseUserMixin, PaginationMixin, FilterParamsMixin, FilterView):
    template_name = "users/user_list.html"
    context_object_name = "users"
    filterset_class = UserFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_url"] = reverse_lazy("users:user-create")
        return add_page_context_data(context, "users:user-list", _("Users"), _("User"))


class UserCreateView(
    BaseUserMixin, CrispyFormArgsMixin, SuccessMessageMixin, CreateView
):
    form_class = UserForm
    template_name = "users/user_details.html"
    success_message = _("User created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_user_password"] = settings.NEW_USER_PASSWORD
        context["show_sales_staff_fields"] = False
        return add_page_context_data(context, "users:user-list", _("Create User"))

    def get_form_kwargs(self):
        """
        Add flag to send email to form kwargs
        :return:
        """
        kw = super(UserCreateView, self).get_form_kwargs()
        kw["send_email"] = True
        return kw


class UserUpdateView(
    BaseUserMixin, CrispyFormArgsMixin, SuccessMessageMixin, UpdateView
):
    form_class = UserForm
    template_name = "users/user_details.html"
    success_message = _("User details updated successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_editing_own_account"] = self.request.user == self.get_object()
        context["show_sales_staff_fields"] = self.object.is_sales

        return add_page_context_data(
            context=context,
            section="users:user-list",
            heading=_("User Details"),
            model_name=_("User"),
            delete_action=reverse("users:user-delete", args=[self.object.pk]),
        )


class UserDeleteView(BaseUserMixin, SuccessMessageMixin, DeleteView):
    success_message = _("User successfully deleted")

    def form_valid(self, form):
        """Check that user is not attempting to delete themselves."""
        if self.request.user == self.get_object():
            raise PermissionDenied()
        return super().form_valid(form)
