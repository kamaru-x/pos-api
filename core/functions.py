def generalize_errors(serializers=[], general_errors=[]):
    if not isinstance(serializers, list):
        serializers = [serializers]

    errors = {
        "form_errors": {},
        "general_errors": general_errors
    }

    def process_errors(error_dict, parent_key=""):
        """
        Recursively process errors to handle nested structures.
        """
        for field, messages in error_dict.items():
            # If the field contains a list of errors, process each one
            if isinstance(messages, list):
                for index, item in enumerate(messages):
                    if isinstance(item, dict):  # Nested serializer errors
                        process_errors(item, f"{parent_key}{field}[{index}]")
                    else:
                        key = f"{parent_key}{field}"
                        errors["form_errors"].setdefault(key, []).append(str(item))
            elif isinstance(messages, dict):  # Handle nested dictionary
                process_errors(messages, f"{parent_key}{field}.")

    for serializer in serializers:
        if not serializer.is_valid():
            process_errors(serializer.errors)

    return errors