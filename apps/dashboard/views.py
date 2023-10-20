from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from apps.core.views.utils import add_page_context_data


@login_required(login_url=reverse_lazy("login"))
@require_http_methods(["GET"])
def dashboard_view(request):
    return TemplateResponse(
        request,
        "dashboard/dashboard.html",
        context=add_page_context_data({}, "dashboard:home", "Dashboard"),
    )
