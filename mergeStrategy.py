import json
from aiAPI import AIAPI 

# Base class for merge strategies. Specific strategies inherit from this.
class MergeStrategy:

    @staticmethod
    def merge(values):
        raise NotImplementedError("Merge method must be implemented by subclasses")

# Merge strategy that takes the first non-None value (Return None if not exist non-None value).
class ChooseFirstStrategy(MergeStrategy):

    @staticmethod
    def merge(values, use_ai = False):
        return next((v for v in values if v is not None), None)

# Merge strategy that choose the suitable value among all values (can use LLM to evaluate -> if failed: take the first non-None value) (Return None if not exist non-None value).
class ChooseSuitableStrategy(MergeStrategy):

    @staticmethod
    def merge(values, use_ai=False):
        # Filter out None values
        non_none_values = [v for v in values if v is not None]

        if not non_none_values:
            return None  # Return None if no non-None values exist

        if use_ai:
            try:
                ai_result = AIAPI.choose_most_appropriate(non_none_values)
                if not (isinstance(ai_result, dict) and "error" in ai_result):
                    return ai_result
            except Exception as e:
                print(f"Unexpected error during AI evaluation: {e}")

        # Default behavior: Return the first non-None value
        return non_none_values[0]

# Merge strategy that appends values into a list, avoiding duplicates (can use AI to choose and clean some elements from this list)
class AppendStrategy(MergeStrategy):
    
    @staticmethod
    def merge(values, use_ai=False):
        merged = []
        seen = set()  # Track hashable items
        seen_unhashable = set()  # Track serialized unhashable items (like dicts)

        for value in values:
            if value is None:
                continue
            if isinstance(value, list):
                for item in value:
                    AppendStrategy.add_item(item, merged, seen, seen_unhashable)
            else:
                AppendStrategy.add_item(value, merged, seen, seen_unhashable)

        if use_ai:
            try:
                # Attempt to use AI to filter or choose appropriate terms
                ai_result = AIAPI.choose_appropriate_terms(merged)
                if isinstance(ai_result, list):  # Ensure the result is a list
                    return ai_result
            except Exception as e:
                # Log the error and return the original merged list
                print(f"AI evaluation failed: {e}")

        # Default behavior: return the merged list
        return merged

    # Helper method to add an item to the merged list, avoiding duplicates.
    @staticmethod
    def add_item(item, merged, seen, seen_unhashable):
        if isinstance(item, dict):
            # Avoid duplicate dicts by using serialized JSON strings for comparison
            serialized = json.dumps(item, sort_keys=True)
            if serialized not in seen_unhashable:
                merged.append(item)
                seen_unhashable.add(serialized)
        elif isinstance(item, (str, int, float, bool, tuple)):
            # Add hashable types directly
            if item not in seen:
                merged.append(item)
                seen.add(item)
        else:
            # Handle unhashable types that are not dicts (fallback)
            if item not in merged:
                merged.append(item)