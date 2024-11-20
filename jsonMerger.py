from mergeStrategy import ChooseFirstStrategy, ChooseSuitableStrategy, AppendStrategy

# A class to merge JSON data using different strategies.
class JsonMerger:
    
    # Define all mapping of merging strategies (tuple: (mergeStrategy, use_ai))
    STRATEGIES = {
        "choose_first": (ChooseFirstStrategy, False),
        "choose_suitable": (ChooseSuitableStrategy, False),
        "choose_suitable_with_ai": (ChooseSuitableStrategy, True),
        "append": (AppendStrategy, False),
        "append_with_ai": (AppendStrategy, True),
    }

    # Merge values with the corresponding strategy
    @staticmethod
    def merge_values(strategy_name, values):
        if strategy_name not in JsonMerger.STRATEGIES:
            raise ValueError(f"Unknown merge strategy: {strategy_name}")
        
        strategy_class, use_ai = JsonMerger.STRATEGIES[strategy_name]
        return strategy_class.merge(values, use_ai=use_ai)

    # Helper Recusion function to merge list of dictionaries bases on schema
    @staticmethod
    def merge_dicts(schema, json_list):
        merged_result = {}
        for key, strategy in schema.items():
            # Collect all values for the current key from all JSON objects
            values = [json_obj.get(key, None) for json_obj in json_list]

            if isinstance(strategy, dict):
                # If strategy is a nested schema, recurse
                nested_json_list = [v for v in values if isinstance(v, dict)]
                merged_result[key] = JsonMerger.merge_dicts(strategy, nested_json_list)
            else:
                # Merge values based on the strategy
                merged_result[key] = JsonMerger.merge_values(strategy, values)
        return merged_result

    # Merge list of dictionaries bases on schema
    @staticmethod
    def merge(schema, json_list):
        return JsonMerger.merge_dicts(schema, json_list)
