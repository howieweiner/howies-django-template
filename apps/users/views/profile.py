from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from apps.core.views.base import BaseAppMixin
from apps.core.views.mixins import CrispyFormArgsMixin
from apps.core.views.utils import add_page_context_data
from apps.users.forms.profile import ProfileForm

User = get_user_model()


class ProfileUpdateView(
    BaseAppMixin, CrispyFormArgsMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = ProfileForm
    template_name = "generic_details.html"
    success_message = _("Your details have been updated successfully")
    context_object_name = "users"
    success_url = reverse_lazy("users:profile-update")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return add_page_context_data(
            context=context,
            section="users:profile-update",
            heading=_("Your Details"),
        )
