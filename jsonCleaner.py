from dataCleaner import DataCleaner
from keyNormalizer import KeyNormalizer
from config import SCHEMA_CONFIG

# Static class for JSON cleaning, combining key normalization and data value cleaning
class JsonCleaner:

    # Clean a json object (by normalize all keys and clean all values)
    @staticmethod
    def clean_json(json_data):
        if isinstance(json_data, dict):
            return JsonCleaner.process_dict(json_data)
        elif isinstance(json_data, list):
            return [JsonCleaner.clean_json(item) for item in json_data]
        return DataCleaner.clean_value(json_data)

    # Process a dictionary by normalizing its keys and cleaning its values recursively
    @staticmethod
    def process_dict(data):
        cleaned_data = {}
        for key, value in data.items():
            # Normalize the key
            normalized_key = KeyNormalizer.normalize_key(key)
            # Recursively clean the value
            cleaned_data[normalized_key] = JsonCleaner.clean_json(value)
        return cleaned_data
    
    # Clean final json object
    @staticmethod
    def clean_final_json(json_data):
        for field_path in SCHEMA_CONFIG['lowercase']:
            JsonCleaner.apply_lowercase(json_data, field_path)
        for field_path in SCHEMA_CONFIG['links_need_verify']:
            JsonCleaner.remove_invalid_urls(json_data, field_path)
        return json_data
    
    # Traverse the nested structure of json_data to find and lowercase the specified field.
    @staticmethod
    def apply_lowercase(data, field_path):
        keys = field_path.split("->")
        for i, key in enumerate(keys):
            if i == len(keys) - 1:  # Last key in the path
                if key in data:
                    # Apply lowercase to string or list of strings
                    list_value = data[key]
                    data[key] = DataCleaner.list_to_lowercase(list_value)
            else:
                # Navigate deeper into the nested dictionary
                if key in data and isinstance(data[key], dict):
                    data = data[key]
                else:
                    return  # Exit if the path does not exist or is invalid
                
    # Remove dictionaries that the link is not accesible
    @staticmethod
    def remove_invalid_urls(data, field_path):
        keys = field_path.split("->")
        for i, key in enumerate(keys):
            if i == len(keys) - 1:  # Last key in the path
                if (key in data and isinstance(data[key], list)):
                    data[key] = [
                        item for item in data[key]
                        if (isinstance(item, dict) and DataCleaner.check_url(item.get("link", ""))) or
                        (isinstance(item, str) and DataCleaner.check_url(item))
                    ]
            else:
                # Navigate deeper into the nested dictionary
                if key in data and isinstance(data[key], dict):
                    data = data[key]
                else:
                    return  # Exit if the path does not exist or is invalid