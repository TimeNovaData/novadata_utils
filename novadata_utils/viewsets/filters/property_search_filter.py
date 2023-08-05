from rest_framework import filters


class PropertySearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        """Filtra a queryset de acordo com os parâmetros de busca."""
        search_param = request.query_params.get(self.search_param, None)
        has_search_properties = hasattr(view, "search_properties")

        not_filtered_query = view.get_queryset()

        if search_param and has_search_properties:
            for property in view.search_properties:
                ids = [
                    obj.id
                    for obj in not_filtered_query
                    if search_param in str(getattr(obj, property))
                ]
                queryset |= not_filtered_query.filter(id__in=ids)

        return queryset
