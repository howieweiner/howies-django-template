from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from ..core.forms import percentage_validator


class User(AbstractUser):
    username = None
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email Address"),
        help_text=_("The email address is used as the username to log in"),
    )
    password_expired = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name=_("Administrator"))
    is_sales = models.BooleanField(default=False, verbose_name=_("Sales Staff"))
    pipedrive_user_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("Pipedrive User ID"),
        help_text=_("Sales Staff must also have an associated Pipedrive User ID"),
    )
    sales_commission_percentage = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
        verbose_name=_("Sales Commission (%)"),
        help_text=_("Sales Staff may have a non-standard sales commission"),
        validators=[percentage_validator],
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        """
        When we create a User, we set an expired temporary password
        """
        if not self.pk:
            self.set_password(settings.NEW_USER_PASSWORD)
            self.password_expired = True
            self.is_staff = True
        super(User, self).save(*args, **kwargs)

    def clean(self):
        """If the user is a sales user, then we validate that they also have a pipedrive user id
        If the user has been updated to remove their sales role, then also remove their pipedrive user id
        and sales commission percentage
        """
        if self.is_sales and not self.pipedrive_user_id:
            raise ValidationError(
                _("Sales users must also have a pipedrive user id"),
                code="sales_user_no_pipedrive_user_id",
            )

        #
        if not self.is_sales and self.pipedrive_user_id:
            self.pipedrive_user_id = None
            self.sales_commission_percentage = None

    def __str__(self):
        return self.email

    def full_name(self):
        return self.first_name + " " + self.last_name

    def initials(self):
        return (self.first_name[0] + self.last_name[0]).upper()

    def is_disabled(self):
        return not self.is_active

    def get_absolute_url(self):
        return reverse("users:user-update", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = "User"
