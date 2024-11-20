import re
import requests
from config import RUBBISH_VALUES

# Static class to clean data values (easily extensible by adding new static methods)
class DataCleaner:

    # Remove leading and trailing spaces from the value. (For example: "    car   " -> "car")
    @staticmethod
    def strip_whitespace(value):
        if isinstance(value, str):
            return value.strip()
        return value
    
    # Normalize text formatting (e.g., convert multiple spaces to a single space, For example: "car   and toy" -> "car and toy").
    @staticmethod
    def normalize_text(value):
        if isinstance(value, str):
            return re.sub(r'\s+', ' ', value)
        return value

    # Remove surrounding quotes (For example: ""car"" -> "car")
    @staticmethod
    def remove_surrouding_quotes(value):
        if isinstance(value, str):
            return re.sub(r'^["\']|["\']$', '', value)
        return value

    # Replace values with None if they are in RUBBISH_VALUES list in config.
    @staticmethod
    def fix_special_cases(value):
        if value in RUBBISH_VALUES:
            return None
        return value
    
    # Convert strings to lowercase (For example: "Wifi" -> "wifi").
    @staticmethod
    def to_lowercase(value):
        if isinstance(value, str):
            return value.lower()
        return value
    
    # Separate concatenated or camel-cased words with spaces (For example: "WiFi" -> "wi fi")
    @staticmethod
    def separate_letters(value):
        if isinstance(value, str):
            # Replace camelCase or PascalCase with spaced words
            value = re.sub(r'(?<!^)(?=[A-Z])', ' ', value)
            # Replace any remaining concatenations or multiple spaces
            return re.sub(r'\s+', ' ', value).strip()
        return value
    
    # Lowercase and return approriate elements in a list (For example: "WiFi" and "wi fi", we keep only one)
    @staticmethod
    def list_to_lowercase(values):
        if isinstance(values, list):
            # Step 1: Normalize strings
            normalized_values = [
                DataCleaner.to_lowercase(DataCleaner.separate_letters(item))
                for item in values if isinstance(item, str)
            ]

            # Step 2: Resolve conflicts using a set for no-space versions
            unique_values = set()
            result = []
            for item in normalized_values:
                no_space_version = item.replace(" ", "")
                if no_space_version not in unique_values:
                    unique_values.add(no_space_version)
                    result.append(item)

            # Return the cleaned list
            return result

        return values 
    
    # Returns True if the URL is accessible (HTTP 200)
    @staticmethod
    def check_url(url):
        try:
            response = requests.head(url, timeout=5) 
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error checking URL {url}: {e}")
            return False
    
    # Clean a single value by applying all transformations.
    @staticmethod
    def clean_value(value):
        value = DataCleaner.strip_whitespace(value)
        value = DataCleaner.normalize_text(value)
        value = DataCleaner.fix_special_cases(value)
        value = DataCleaner.remove_surrouding_quotes(value)
        return value