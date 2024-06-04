from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai
import json

openai.api_key_path = 'config/OpenAPI_Key.txt'
#MODEL = 'gpt-3.5-turbo'
MODEL = 'gpt-3.5-turbo-1106'
function_descriptions = [
        {
            "name":"get_user_preference",
            "description": "Get the user preference and fill in the values for the required fields",
            "parameters": {
                "type": "object",
                "properties": {
                    "City":{
                        "type": "string",
                        "description": "The requirement of the user in City. It should be a proper location field that matches the database"
                    },
                    "RestaurantType":{
                        "type": "string",
                        "description": "The requirement of the user in RestaurantType should be one of 'Casual Dining'/'QuickBites'/'Buffet'/'NA'. If the user enters any other value for this field, show these options to the user and get the user input again. if the user has no preference, set the value as 'NA'"
                    },
                    "ApproxCost":{
                        "type": "integer",
                        "description": "The value should be numeric. If the user has no constraint, set the value to 0"
                    },
                    "Cuisine":{
                        "type": "string",
                        "description": "The requirement of the user in Cuisine should be one of 'North Indian'/'South Indian'/'Chinese'/'NA'. If the user enters any other value for this field, show these options to the user and get the user input again. if the user has no preference, set the value as 'NA'"
                    },
                    "Votes":{
                        "type": "string",
                        "description": "The requirement of the hotel preference should be classified as either high/medium/low. If the user is looking a best hotel, set the value as high"
                    }
                },
                "required": ['City', 'RestaurantType', 'ApproxCost', 'Cuisine', 'Votes']
            }
        }
    ];

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def chat_completions_function_call(input, json_format = False):
    chat_response = openai.ChatCompletion.create(
            model = MODEL,
            messages = input,
            temperature=0,
            max_tokens=500,
            function = function_descriptions,
            function_call = 'auto'
            )
    return response.choices[0].message;
    
    
# Define a Chat Completions API call
# Retry up to 6 times with exponential backoff, starting at 1 second and maxing out at 20 seconds delay
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_chat_completions(input, json_format = False):
    system_message_json_output = """<<. Return output in JSON format to the key output.>>"""

    # If the output is required to be in JSON format
    if json_format == True:
        # Append the input prompt to include JSON response as specified by OpenAI
        input[0]['content'] += system_message_json_output

        # JSON return type specified
        chat_completion_json = openai.ChatCompletion.create(
            model = MODEL,
            messages = input,
            response_format = { "type": "json_object"},
            seed = 1234)

        output = json.loads(chat_completion_json.choices[0].message.content)

    # No JSON return type specified
    else:
        chat_completion = openai.ChatCompletion.create(
            model = MODEL,
            messages = input,
            seed = 2345)

        output = chat_completion.choices[0].message.content

    return output