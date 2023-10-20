from distutils.util import strtobool

from crispy_forms.layout import Layout, ButtonHolder, Submit, Field, Fieldset, HTML
from django import forms

from apps.core.forms.filters import BaseFilterFormHelper

INACTIVE = "0"
ACTIVE = "1"

ACTIVE_STATE_CHOICES = (
    (ACTIVE, "Active"),
    (INACTIVE, "Inactive"),
)


class UserFilterForm(forms.Form):
    q = forms.CharField()
    is_active = forms.TypedChoiceField(
        required=True,
        choices=ACTIVE_STATE_CHOICES,
        coerce=strtobool,
    )


class UserFilterFormHelper(BaseFilterFormHelper):
    field_class = "mb-0"

    layout = Layout(
        Fieldset(
            "",
            Field(
                "q",
                data_lpignore="true",
                placeholder="Search by email, first name or last name",
                css_class="w-48 sm:w-96",
            ),
            Field(
                "is_active",
                wrapper_class="w-48",
            ),
            ButtonHolder(
                Submit("submit", "Filter", css_class="btn-primary"),
                HTML('<a href=".?q=" class="form-link">Clear</a>'),
                css_class="flex space-x-4",
            ),
            css_class="flex justify-start gap-4 items-end mb-4 mx-4 sm:mx-0",
        )
    )
