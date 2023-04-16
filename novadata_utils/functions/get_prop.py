from novadata_utils.models import NovadataModel

# ChoicesField é um CharField com choices
props_dict = {
    # Admin props
    "list_display": [
        "BigAutoField",
        "BooleanField",
        "CharField",
        "DateField",
        "DateTimeField",
        "DecimalField",
        "ForeignKey",
        "IntegerField",
        "PositiveIntegerField",
        "ChoicesField",
    ],
    "search_fields": [
        "BigAutoField",
        "CharField",
        "DateField",
        "DateTimeField",
        "DecimalField",
        "IntegerField",
        "PositiveIntegerField",
        "ChoicesField",
    ],
    "list_filter": [
        "BooleanField",
        "DateField",
        "DateTimeField",
        "ForeignKey",
        "ChoicesField",
    ],
    "autocomplete_fields": [
        "ForeignKey",
    ],
    "list_select_related": [
        "ForeignKey",
    ],
    "filter_horizontal": [
        "ManyToManyField",
    ],
    # Generic props
    "foreign_keys": [
        "ForeignKey",
    ],
    "many_to_many": [
        "ManyToManyField",
    ],
    # Viewset props
    "filterset_fields": [
        "BigAutoField",
        "CharField",
        "DecimalField",
        "IntegerField",
        "PositiveIntegerField",
        "ChoicesField",
        "BooleanField",
        "DateField",
        "DateTimeField",
        "ForeignKey",
    ],
    "ordering_fields": [
        "BigAutoField",
        "CharField",
        "DateField",
        "DateTimeField",
        "DecimalField",
        "IntegerField",
        "PositiveIntegerField",
        "BooleanField",
        "ForeignKey",
        "ChoicesField",
    ],
    # Viewset sub props
    "BigAutoField": [
        "exact",
        "in",
        "gt",
        "gte",
        "lt",
        "lte",
        "range",
    ],
    "CharField": [
        "exact",
        "in",
        "icontains",
        "isnull",
    ],
    "DateField": [
        "exact",
        "in",
        "gt",
        "gte",
        "lt",
        "lte",
        "range",
        "isnull",
    ],
    "DateTimeField": [
        "exact",
        "in",
        "gt",
        "gte",
        "lt",
        "lte",
        "range",
        "isnull",
    ],
    "DecimalField": [
        "exact",
        "in",
        "gt",
        "gte",
        "lt",
        "lte",
        "range",
        "isnull",
    ],
    "IntegerField": [
        "exact",
        "in",
        "gt",
        "gte",
        "lt",
        "lte",
        "range",
        "isnull",
    ],
    "PositiveIntegerField": [
        "exact",
        "in",
        "gt",
        "gte",
        "lt",
        "lte",
        "range",
        "isnull",
    ],
    "ChoicesField": [
        "exact",
        "in",
        "icontains",
        "isnull",
    ],
    "BooleanField": [
        "exact",
    ],
    "ForeignKey": [
        "exact",
        "isnull",
    ],
    "ManyToManyField": [
        "exact",
        "in",
        "isnull",
    ],
    # Especific props
    "choices_fields": [
        "ChoicesField",
    ],
}


def get_fields(model):
    """get_fields personalizado."""
    parents = model._meta.parents
    if parents:
        first_parent = next(iter(parents))
        is_subclass = issubclass(NovadataModel, first_parent)

        if is_subclass:
            super_fields_whinout_id = list(first_parent._meta.fields)[1:]
            fields = list(model._meta.get_fields())
            duplicated_fields = filter(
                lambda field: field in super_fields_whinout_id,
                super_fields_whinout_id,
            )
            list(map(lambda field: fields.remove(field), duplicated_fields))

            new_fields = fields + super_fields_whinout_id
            return new_fields

    return model._meta.get_fields()


def get_field_type(field):
    """Retorna o tipo de um campo."""
    field_type = field.get_internal_type()
    is_choices = (
        hasattr(field, "choices")
        and field.choices
        and field_type == "CharField"
    )

    if is_choices:
        field_type = "ChoicesField"

    return field_type


def get_prop(model, prop, str=False, annotate_type=False):
    """
    Retorna uma lista de campos de um model baseado em uma propriedade.

    Exemplo:
        get_prop(model, "list_display") retorna todos os campos que podem ser
        exibidos na listagem do admin. Que são:
            "BigAutoField",
            "BooleanField",
            "CharField",
            "DateField",
            "DateTimeField",
            "DecimalField",
            "ForeignKey",
            "IntegerField" e
            "PositiveIntegerField".
    """
    props = []
    fields = get_fields(model)
    for field in fields:
        field_type = get_field_type(field)

        is_original_field = not hasattr(field, "field")
        if field_type in props_dict[prop] and is_original_field:
            if str:
                name = f'"{field.name}",'
            else:
                name = field.name

            if annotate_type:
                props.append({"name": name, "type": field_type})
            else:
                props.append(name)

    return props
