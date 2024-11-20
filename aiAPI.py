import requests
import json
import time
from config import API_CONFIG, PROMPTS

# Static class to handle interactions with AI API.
class AIAPI:
    @staticmethod
    def call_awanllm_api(prompt):
        """
        Sends a request to the AI API with the given prompt and returns the response.
        """
        # API endpoint and headers
        url = API_CONFIG["url"]
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {API_CONFIG['api_key']}"
        }

        # Payload
        payload = {
            "model": API_CONFIG["model"],
            "prompt": prompt,
            **API_CONFIG["default_params"]
        }

        # Send the request
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                result = response.json()
                return result.get('choices', [{}])[0].get('text', '').strip()
            else:
                # Log the error with the status code and reason
                error_message = f"API Error: {response.status_code} - {response.reason}"
                return {"error": error_message}
        except requests.RequestException as e:
            # Handle network or request errors
            return {"error": f"Request error: {str(e)}"}
        except Exception as e:
            # Handle unexpected errors
            return {"error": f"Unexpected error: {str(e)}"}

    @staticmethod
    def choose_most_appropriate(values):
        """
        Uses AI to choose the most appropriate single value from a list.
        """
        try:
            prompt = PROMPTS["most_appropriate_term"].format(values=json.dumps(values))
            response = AIAPI.call_awanllm_api(prompt)

            if isinstance(response, dict) and "error" in response:
                raise ValueError(response["error"])  # Raise error if the response contains an error key

            # Parse response into a single value
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI response as JSON"}
        except ValueError as e:
            # Return the error message as a dictionary for further handling
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Unexpected error in choose_most_appropriate: {str(e)}"}

    @staticmethod
    def choose_appropriate_terms(values):
        """
        Uses AI to refine a list of values into the most appropriate terms.
        """
        try:
            prompt = PROMPTS["appropriate_terms"].format(values=json.dumps(values))
            response = AIAPI.call_awanllm_api(prompt)

            if isinstance(response, dict) and "error" in response:
                raise ValueError(response["error"])  # Raise error if the response contains an error key

            # Parse response into a list of appropriate terms
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI response as JSON"}
        except ValueError as e:
            # Return the error message as a dictionary for further handling
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Unexpected error in choose_appropriate_terms: {str(e)}"}
