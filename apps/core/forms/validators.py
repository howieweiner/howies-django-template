from django.core.exceptions import ValidationError


def percentage_validator(value):
    """
    Validate that the value is between 0 and 100
    """
    if value < 0 or value > 100:
        raise ValidationError(
            _("%(value)s is not a valid percentage"), params={"value": value}
        )
