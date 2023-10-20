from django.utils.http import urlencode


class PaginationMixin(object):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """
        Add page number to context
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context["page"] = self.request.GET.get("page", 1)
        return context


class CrispyFormArgsMixin(object):
    """
    Mixin that adds request to form kwargs
    """

    def get_form_kwargs(self):
        kw = super(CrispyFormArgsMixin, self).get_form_kwargs()
        kw["request"] = self.request
        return kw


class FilterParamsMixin(object):
    """
    Mixin that  supports filter functionality. It places the query params back
    in context for appending to urls
    """

    filter_params = {}

    def get_context_data(self, **kwargs):
        context = super(FilterParamsMixin, self).get_context_data(**kwargs)
        params = self.request.GET

        for key in params.keys():
            # store params so we can place them back in page scope/context
            if key not in ["page", "submit"]:
                self.filter_params[key] = params[key]

        if self.filter_params:
            # encode values individually
            params = {}
            for k, v in self.filter_params.items():
                params[k] = v
            context["form_filter_query"] = urlencode(params)
        else:
            context["form_filter_query"] = ""
        return context
