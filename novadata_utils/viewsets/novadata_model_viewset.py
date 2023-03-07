from django_filters.rest_framework import DjangoFilterBackend
from novadata_utils.functions import get_prop
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class NovadataModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    filterset_fields: list = None

    ordering_fields: list = None

    search_fields: list = None

    auto_search_fields: bool = False

    relation_fields = [
        "OneToOneField",
        "ForeignKey",
    ]

    def get_filterset_fields(self):
        model = self.serializer_class().Meta.model
        filterset_fields = get_prop(
            model,
            "filterset_fields",
            str=False,
        )

        return filterset_fields

    def get_ordering_fields(self):
        model = self.serializer_class().Meta.model
        ordering_fields = get_prop(
            model,
            "ordering_fields",
            str=False,
        )

        return ordering_fields

    def get_search_fields(self):
        model = self.serializer_class().Meta.model
        search_fields = get_prop(
            model,
            "search_fields",
            str=False,
        )

        return search_fields

    def get_fk_fields(self):
        model = self.serializer_class().Meta.model
        fields = model._meta.get_fields()
        fk_fields = [
            (field.name, field.remote_field.model)
            for field in fields
            if field.get_internal_type() in self.relation_fields
        ]

        return fk_fields

    def get_data(self, request):
        data = request.data.copy()
        for fk_field in self.get_fk_fields():
            field_name = fk_field[0]
            try:
                if isinstance(data[field_name], dict):
                    data[field_name] = data[field_name].get(
                        "id",
                        None,
                    )
            except KeyError:
                print(f"Não passou {field_name}")

        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.get_data(request))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data.copy()

        obj_datas = {}
        for field in self.get_fk_fields():
            field_name = field[0]
            obj_datas[field_name] = data.pop(
                field_name,
                [None],
            )[0]

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        for field in self.get_fk_fields():
            field_name = field[0]

            try:
                model = field[1]
                obj_data = obj_datas[field_name]
                if obj_data:
                    if isinstance(obj_data, dict):
                        fk_instance = model.objects.get(
                            pk=obj_data.get("id", None)
                        )
                    else:
                        fk_instance = model.objects.get(pk=obj_data)

                    setattr(serializer.instance, field_name, fk_instance)
            except model.DoesNotExist:
                print(f"Não passou {field_name}")

        self.perform_update(serializer)
        serializer.instance.save()

        return Response(serializer.data)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if not self.filterset_fields:
            self.filterset_fields = self.get_filterset_fields()

        if not self.ordering_fields:
            self.ordering_fields = self.get_ordering_fields()

        if self.auto_search_fields and not self.search_fields:
            self.search_fields = self.get_search_fields()
