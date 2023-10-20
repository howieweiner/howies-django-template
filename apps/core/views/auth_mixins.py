from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


def is_admin(user):
    return hasattr(user, "is_admin") and user.is_admin


def is_sales(user):
    return hasattr(user, "is_sales") and user.is_sales


class IsAdminMixin(object):
    @method_decorator(user_passes_test(is_admin, login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(IsAdminMixin, self).dispatch(request, *args, **kwargs)


class IsSalesMixin(object):
    @method_decorator(user_passes_test(is_sales, login_url=reverse_lazy("login")))
    def dispatch(self, request, *args, **kwargs):
        return super(IsSalesMixin, self).dispatch(request, *args, **kwargs)
