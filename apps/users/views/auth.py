import logging

from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import (
    LoginView,
    PasswordResetConfirmView,
    PasswordChangeView,
)
from django.http import HttpResponseRedirect
from django.urls import reverse

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    def form_valid(self, form):
        """
        Check that password has not expired. If, so log user out and redirect to
         password change form
        """
        user = form.get_user()

        logger.debug("checking if user password has expired..")
        if user.password_expired:
            logger.debug(
                "user password has expired, redirecting to password change form"
            )
            login(self.request, user)
            return HttpResponseRedirect(reverse("password_change"))
        logger.debug("user password has not expired, logging in")
        return super(CustomLoginView, self).form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Override view to also reset password_expired flag on user
    """

    def form_valid(self, form):
        user = form.save()
        user.password_expired = False
        user.save()
        return super().form_valid(form)


class CustomPasswordChangeView(PasswordChangeView):
    """
    Override view to also reset password_expired flag on user
    """

    def form_valid(self, form):
        form.save()
        form.user.password_expired = False
        form.user.save()

        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)
