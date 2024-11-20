from jsonCleaner import JsonCleaner
from jsonParser import JsonToJsonConverter
from jsonMerger import JsonMerger
from config import SCHEMA_CONFIG, SUPPLIERS
import requests

# Class to fetch data from url, conver
class Supplier:
    def __init__(self, supplier_name):
        self.supplier_url = f'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/{supplier_name}'
        raw_data = self.fetch_data()
        cleaned_data = [self.clean_and_transform(dto) for dto in raw_data]

        # Save the cleaned data after fetching and sanitizing
        self.cleaned_data = cleaned_data
        
        # Save list of hotel_ids and destination_ids of the supplier
        self.hotel_ids = [item['id'] for item in self.cleaned_data if 'id' in item]
        self.destination_ids = [item['destination_id'] for item in self.cleaned_data if 'destination_id' in item]

    # Fetch json response
    def fetch_data(self):
        response = requests.get(self.supplier_url)
        response.raise_for_status()
        return response.json()

    # Clean data and then transform to correct format that we need to return 
    def clean_and_transform(self, dto):
        # Clean the JSON data (remove extra spaces, normalize, etc.)
        cleaned_item = JsonCleaner.clean_json(dto)

        # Transform the JSON data using the schema
        transformed_item = JsonToJsonConverter.transform(SCHEMA_CONFIG['select'], cleaned_item)

        return transformed_item
    
    # Filter all hotel_id and destination_id
    def filter_dtos(self, dtos, hotel_id, destination_id):
        filtered_data = []
        for item in dtos:
            if (item['id'] == hotel_id) and \
               (item['destination_id'] == destination_id):
                filtered_data.append(item)
        return filtered_data

    # Return list of json objects that match hotel_id and destination_id
    def process_dtos(self, hotel_id = None, destination_id = None):
        return self.filter_dtos(self.cleaned_data, hotel_id, destination_id)
    

class SupplierHandler:
    def __init__(self):
        self.suppliers = [Supplier(name) for name in SUPPLIERS]

        # Combine all unique hotel_ids and destination_ids across all suppliers
        self.hotel_ids = set()
        self.destination_ids = set()

        for supplier in self.suppliers:
            self.hotel_ids.update(supplier.hotel_ids)
            self.destination_ids.update(supplier.destination_ids)

    # Return list of json objects satisfies hotel_ids and destination_ids in input
    def process_all_suppliers(self, hotel_ids=None, destination_ids=None):
        all_dtos = []

        # If both hotel_ids and destination_ids are provided, process their combinations
        if hotel_ids and destination_ids:
            for hotel_id in hotel_ids:
                for destination_id in destination_ids:
                    dtos = []
                    for supplier in self.suppliers:
                        # Process only for the specific pair
                        supplier_data = supplier.process_dtos(hotel_id, destination_id)
                        if (len(supplier_data) > 0):
                            dtos.extend(supplier_data)
                    
                    # Merge data for the current pair
                    if (len(dtos) > 0):
                        merged_dtos = JsonMerger.merge(SCHEMA_CONFIG['merge'], dtos)
                        merged_dtos = JsonCleaner.clean_final_json(merged_dtos)
                        all_dtos.append(merged_dtos)
        
        # In other cases
        else:
            for hotel_id in self.hotel_ids:
                for destination_id in self.destination_ids:
                    dtos = []
                    for supplier in self.suppliers:
                        # Process only for the specific pair
                        supplier_data = supplier.process_dtos(hotel_id, destination_id)
                        if (len(supplier_data) > 0):
                            dtos.extend(supplier_data)
                    # Merge data for the current pair
                    if (len(dtos) > 0):
                        merged_dtos = JsonMerger.merge(SCHEMA_CONFIG['merge'], dtos)
                        merged_dtos = JsonCleaner.clean_final_json(merged_dtos)
                        all_dtos.append(merged_dtos)

        # Return the combined result for all processed pairs
        return all_dtos