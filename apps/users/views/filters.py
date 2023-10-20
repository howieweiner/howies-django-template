import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.users.forms.user_filter import (
    UserFilterFormHelper,
    UserFilterForm,
    ACTIVE_STATE_CHOICES,
)

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="omni_filter", label="Search")
    is_active = django_filters.ChoiceFilter(
        choices=ACTIVE_STATE_CHOICES,
        label="Status",
        empty_label="All",
    )

    class Meta:
        model = User
        fields = ["q", "is_active"]
        form = UserFilterForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = UserFilterFormHelper()

    def omni_filter(self, queryset, name, value):
        return queryset.filter(
            Q(email__icontains=value)
            | Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
        )
