import json
import argparse
from supplier import SupplierHandler
from objectClass import Hotel

def fetch_hotels(hotel_ids, destination_ids):
    s = SupplierHandler()
    all_supplier_data = s.process_all_suppliers(hotel_ids, destination_ids)
    return all_supplier_data

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("hotel_ids", type=str, help="Hotel IDs")
    parser.add_argument("destination_ids", type=str, help="Destination IDs")
    
    # Parse the arguments
    args = parser.parse_args()
    
    hotel_ids = args.hotel_ids.split(",") if args.hotel_ids.lower() != "none" else None
    destination_ids = args.destination_ids.split(",") if args.destination_ids.lower() != "none" else None
    if (destination_ids != None):
        destination_ids = [int(destination_id) for destination_id in destination_ids]
    
    hotels = fetch_hotels(hotel_ids, destination_ids)
    
    print(json.dumps(hotels, indent=4))

if __name__ == "__main__":
    main()