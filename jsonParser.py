from jsonCleaner import JsonCleaner

# A static class to transform a list of JSON objects based on a unified schema.
class JsonToJsonConverter:
    
    # Evaluate individual placeholders, supporting nested keys with '->' (return the corresponding value or None)
    @staticmethod
    def resolve_placeholder(placeholder, data):
        try:
            if "->" in placeholder:
                keys = placeholder.split("->")
                result = data
                for key in keys:
                    result = result.get(key, None)
                    if result is None:
                        return None
                return result
            else:
                return data.get(placeholder, None)
        except Exception:
            return None

    # Resolve a list of fallback placeholders and return the first non-empty result (with the type different from dictionary).
    @staticmethod
    def resolve_placeholders(values, data):
        if isinstance(values, list):
            for value in values:
                resolved = JsonToJsonConverter.resolve_placeholder(value, data)
                if resolved is not None and not isinstance(resolved, dict):
                    return resolved
        return None

    # Recursively process each node of the schema.
    @staticmethod
    def process_node(node, data):
        # If type of node is dictionary -> recursion
        if isinstance(node, dict):
            result = {key: JsonToJsonConverter.process_node(value, data) for key, value in node.items()}
            return {k: v for k, v in result.items()}
        
        # If type of node is list -> call resolve_placeholders function
        elif isinstance(node, list):
            return JsonToJsonConverter.resolve_placeholders(node, data)
        
        # If the node is not a dict or list, raise an exception (incorrect design in select schema)
        raise TypeError(f"Unsupported schema node type: {type(node)}")

    # Transform a JSON object based on the schema.
    @staticmethod
    def transform(schema, data):
        return JsonToJsonConverter.process_node(schema, data)