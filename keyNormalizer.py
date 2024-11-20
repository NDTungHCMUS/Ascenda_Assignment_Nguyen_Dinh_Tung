import re
from config import KEY_MAPPING

# Static class to normalize keys (easily extensible by adding new static methods)
class KeyNormalizer:

    # Remove leading and trailing whitespace from the key (For example: "   id   " -> "id").
    @staticmethod
    def strip_key(key):
        return key.strip()

    # Convert a key from camelCase or PascalCase to snake_case. (For example: "DestinationId" -> "destination_id")
    @staticmethod
    def convert_to_snake_case(key):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()

    # Replace the key with special case mappings, if applicable.
    @staticmethod
    def apply_special_cases(key):
        return KEY_MAPPING.get(key, key)

    # Normalize a key by applying all transformations.
    @staticmethod
    def normalize_key(key):
        key = KeyNormalizer.strip_key(key)
        key = KeyNormalizer.convert_to_snake_case(key)
        key = KeyNormalizer.apply_special_cases(key)
        return key