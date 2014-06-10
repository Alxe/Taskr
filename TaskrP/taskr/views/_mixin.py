from django.views.generic.base import ContextMixin

__author__ = 'Alex'


class FilterMultipleObjectMixin(ContextMixin):
    """ Mixin that populates context with filtered data from a queryset """
    filter = None

    offset = None
    limit = None

    context_object_name = None

    def get_offset(self):
        return self.offset if self.offset  else 0

    def get_limit(self):
        return self.limit if self.limit  else self.get_queryset().count()

    def get_filter(self):
        return self.filter if self.filter else {}

    def get_context_object_name(self):
        return self.context_object_name if self.context_object_name else 'object_list'

    def get_filtered_queryset(self):
        queryset = self.get_queryset()

        # Compose filter
        filter = self.get_filter()

        # Calculate offset and limit
        offset = self.get_offset()
        limit = self.get_limit()

        return queryset.filter(**filter)[offset:limit]

    def get_context_data(self, **kwargs):
        """ Returns context data with filtered object list  """
        queryset = self.get_filtered_queryset()

        # Create context
        context = {
            self.get_context_object_name(): queryset
        }
        context.update(**kwargs)

        # Follow up grand-parent's implementation
        return super(FilterMultipleObjectMixin, self).get_context_data(**context)


class UserFilterMultipleObjectMixin(FilterMultipleObjectMixin):
    """ Mixin that populates context with filtered data, with the currently logged user as value, from a queryset """

    attr = None

    def get_filter(self):
        filter = {}
        if self.attr:
            filter[self.attr] = self.request.user
        return filter




