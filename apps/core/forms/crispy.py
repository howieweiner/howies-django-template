from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, HTML
from crispy_tailwind.layout import Submit
from django.urls import reverse_lazy


class CrispyFormMixin(object):
    submit_button_text = "Save"
    cancel_action = None
    full_width = True
    button_holder_css = "mt-8 h-24 border-t border-gray-900/10 flex justify-end items-center space-x-8 w_full"
    button_holder_width = ""

    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.request = kwargs.pop("request", None)
        super(CrispyFormMixin, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_action = self.request.path if self.request else ""

        # if page is in context, add to the form action
        if self.request and "page" in self.request.GET:
            self.helper.form_action += f"?page={self.request.GET['page']}"

        self.helper.label_class = "text-gray-500 text-md font-medium mb-2 inline-block"

        if not self.full_width:
            self.button_holder_width = " md:w-2/3"

        self.button_holder = Layout(
            ButtonHolder(
                HTML(
                    f'<a href="{self._get_cancel_action()}" class="form-link" id="cancel-btn">Cancel</a>'
                ),
                Submit(
                    "submit",
                    self.get_submit_button_text(),
                    css_class="btn-primary",
                ),
                css_class=self.button_holder_css + self.button_holder_width,
            )
        )

    def get_submit_button_text(self):
        return self.submit_button_text

    def _get_cancel_action(self):
        if self.request is None:
            return

        """Return the cancel action, with the page number and any query params"""
        action = (
            reverse_lazy(self.cancel_action)
            if self.cancel_action
            else "javascript:history.back()"
        )

        for k, v in self.request.GET.items():
            if k != "submit":
                delimiter = "&" if "?" in action else "?"
                action += f"{delimiter}{k}={v}"

        return action
