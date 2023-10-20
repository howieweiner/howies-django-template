from crispy_forms.layout import Layout, Div
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from apps.core.forms import CrispyFormMixin

User = get_user_model()


class ProfileForm(CrispyFormMixin, ModelForm):
    cancel_action = "dashboard:home"
    full_width = False

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Div("first_name", "last_name", "email", css_class="w-full md:w-2/3"),
            self.button_holder,
        )
