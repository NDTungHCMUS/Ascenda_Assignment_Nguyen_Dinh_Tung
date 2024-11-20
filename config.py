# Config API for using LLM
API_CONFIG = {
    "api_key": "09b3ed48-9f69-45ac-8e88-8d64fd5ac320",
    "url": "https://api.awanllm.com/v1/completions",
    "model": "Meta-Llama-3.1-8B-Instruct",
    "default_params": {
        "repetition_penalty": 1.1,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 1024,
        "stream": False,
    },
}

# Prompts for AI 
PROMPTS = {
    "most_appropriate_term": (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        "You are an assistant AI.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
        "Given the list of synonyms: {values}, which is the most appropriate?" 
        "Your output must strictly be a valid Python str type with only one element. "
        "Do not include explanations, lists, or additional text, only return the single value as a Python string."
        "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    ),
    "appropriate_terms": (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        "You are an assistant AI.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
        "Given the list of data: {values}, which are some of the appropriate ones? "
        "Your output must strictly be a valid Python list with cleaned elements only. "
        "Do not include explanations, str data type, or additional text, only return a Python list."
        "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    ),
}

# Config Schema (to convert json to correct form, merge json and lowercase some fields)
SCHEMA_CONFIG = {
    "select": {
        "id": ["id"],
        "destination_id": ["destination_id"], 
        "name": ["name"],
        "location": {
            "lat": ["lat"],
            "lng": ["lng"],
            "address": ["address", "location->address"],
            "city": ["city"],
            "country": ["country", "location->country"]
        },
        "description": ["description"],
        "amenities": {
            "general": ["amenities->general", "facilities"],
            "room": ["amenities", "amenities->room"]
        },
        "images": {
            "rooms": ["images->rooms"],
            "site": ["images->site"],
            "amenities": ["images->amenities"]
        },
        "booking_conditions": ["booking_conditions"]
    },
    "merge": {
        "id": "choose_first",
        "destination_id": "choose_first", 
        "name": "choose_first",
        "location": {
            "lat": "choose_first",
            "lng": "choose_first",
            "address": "choose_suitable_with_ai",
            "city": "choose_suitable_with_ai",
            "country": "choose_suitable_with_ai"
        },
        "description": "choose_suitable_with_ai",
        "amenities": {
            "general": "append_with_ai",
            "room": "append_with_ai"
        },
        "images": {
            "rooms": "append",
            "site": "append",
            "amenities": "append"
        },
        "booking_conditions": "append_with_ai"
    },
    "lowercase": ["amenities->general", "amenities->room"],
    "links_need_verify": ["images->rooms", "images->site", "images->amenities"]
}

# Define all Suppliers
SUPPLIERS = ['acme', 'patagonia', 'paperflies']

# Define rubbish value -> convert to None instead
RUBBISH_VALUES = ["N/A", "null", "NULL", ""]

# Key mapping
KEY_MAPPING = {
    "hotel_id": "id",
    "hotel_name": "name",
    "latitude": "lat",
    "longitude": "lng",
    "caption": "description",
    "info": "description",
    "details": "description",
    "destination": "destination_id",
    "url": "link"
}

