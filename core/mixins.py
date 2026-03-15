from rest_framework import serializers

class RepMixin(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        self.display_fields = kwargs.pop("display_fields", None)
        super().__init__(*args, **kwargs)

    def get_fields(self):
        fields = super().get_fields()

        if self.display_fields:
            allowed = set(self.display_fields)
            fields = {k: v for k, v in fields.items() if k in allowed}

        return fields

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Convert choice fields to {id, name}
        for field_name, field in self.fields.items():
            if hasattr(field, "choices") and field.choices:
                value = getattr(instance, field_name, None)
                if value is not None:
                    display = getattr(
                        instance,
                        f"get_{field_name}_display",
                        None
                    )
                    if callable(display):
                        data[field_name] = {
                            "id": value,
                            "name": display(),
                        }

        return data