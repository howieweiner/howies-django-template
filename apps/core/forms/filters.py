from crispy_forms.helper import FormHelper


class BaseFilterFormHelper(FormHelper):
    form_tag = True
    form_action = "."
    form_method = "GET"
    label_class = "text-gray-500 text-md font-medium mb-2 inline-block"

    def __init__(self):
        super().__init__()
        self.attrs = {"autocomplete": "off"}


ARCHIVE_STATE_ACTIVE = "0"
ARCHIVE_STATE_ARCHIVED = "1"

ARCHIVE_STATE_CHOICES = (
    (ARCHIVE_STATE_ACTIVE, "In Use"),
    (ARCHIVE_STATE_ARCHIVED, "Archived"),
)
