import logging

from crispy_forms.layout import Layout, Div, Fieldset, Field
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from apps.core.forms import CrispyFormMixin
from apps.users.tasks import send_new_user_email

User = get_user_model()
logger = logging.getLogger(__name__)


class UserForm(CrispyFormMixin, ModelForm):
    cancel_action = "users:user-list"

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_admin",
            "is_sales",
            "pipedrive_user_id",
            "sales_commission_percentage",
        )

    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.send_email = kwargs.pop("send_email", False)
        super(UserForm, self).__init__(*args, **kwargs)

        # add x-data attribute for  AlpineJS support
        self.helper.attrs = {
            "autocomplete": "off",
            "x-data": "staffDetails",
        }

        # if the logged-in user is an admin user, we don't allow them to unset themselves as admin, nor deactivate
        # themselves
        if self.request.user.is_admin and self.instance == self.request.user:
            self.fields["is_admin"].disabled = True
            self.fields["is_active"].disabled = True

        self.helper.layout = Layout(
            Div(
                Div(
                    Field("first_name", data_lpignore="true"),
                    Field("last_name", data_lpignore="true"),
                    Field("email", data_lpignore="true"),
                    Fieldset(
                        _("Sales Staff Details"),
                        "pipedrive_user_id",
                        Field("sales_commission_percentage", min=0, max=100, step=0.5),
                        css_class="my-16",
                        x_cloak="true",
                        x_show="showSalesStaffFields",
                    ),
                    "is_active",
                ),
                Div(
                    Fieldset(
                        "Roles",
                        "is_admin",
                        Field(
                            "is_sales", id="is_sales"
                        ),  # needed as toggle field wraps underlying checkbox
                    )
                ),
                css_class="grid grid-cols-2 gap-16",
            ),
            self.button_holder,
        )

    def save(self, commit=True):
        """
        Save the user, and send invite email if requested (create, not update)
        """
        model = super().save(commit=False)
        if commit:
            model.save()

            if self.send_email:
                logger.info(f"Sending new user email for user id { model.id }")
                send_new_user_email.delay(model.id)

        return model

    def clean_is_admin(self):
        """Check that user is not attempting to disable their own admin status"""
        if (
            self.request.user == self.instance
            and self.request.user.is_admin != self.cleaned_data["is_admin"]
        ):
            raise ValidationError(
                {"is_admin", "You cannot remove the admin role from yourself"}
            )
        return self.cleaned_data["is_admin"]

    def clean_is_active(self):
        """Check that user is not attempting to disable their own account"""
        if (
            self.request.user == self.instance
            and self.request.user.is_active != self.cleaned_data["is_active"]
        ):
            raise ValidationError(
                {"is_active", "You cannot deactivate your own account"}
            )
        return self.cleaned_data["is_active"]
