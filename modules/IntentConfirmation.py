import openai
import json
"""
This function serves as an intent confirmation layer for a laptop recommendation system using OpenAI LLM API.

Parameters:
- response_assistant (str): The input text containing user requirements captured through 6 keys:
    'GPU intensity', 'Display quality', 'Portability', 'Multitasking', 'Processing speed', and 'Budget'.

Returns:
- str: A one-word string in JSON format indicating if the values for the specified keys are correctly filled.
    - 'Yes' if the values are correctly filled for all keys ('GPU intensity', 'Display quality', 'Portability',
      'Multitasking', 'Processing speed') based on the importance as stated by the user.
    - 'No' otherwise.

Note:
- The values for all keys, except 'Budget', should be 'low', 'medium', or 'high' based on their importance as stated by the user.
- The input text should be structured such that it contains the necessary keys and their corresponding values.
- The function uses OpenAI's Chat Completion API to evaluate the correctness of the input values.
"""

def intent_confirmation_layer(response_assistant):

    delimiter = "####"
    
    prompt = f"""
    You are a senior evaluator who has an eye for detail. The input text will contain a user requirement captured through 5 keys.
    You are provided an input. You need to evaluate if the input text has the following keys:
    {{'City':'values', 'RestaurantType':'values', 'ApproximateCost':'values', 'Cuisine':'values', 'Votes':'values'}}
    The values for the RestaurantType should be one of 'Casual Dining'/'QuickBites'/'Buffet'/'NA'
    The values for the Cuisine should be one of 'North Indian'/'South Indian'/'Chinese'/'NA'
    The values for the Votes should be one of 'high'/'medium'/'low'
    The values for the City should be a string in 1 or 2 words.
    The 'ApproximateCost' key can take only a numerical value.
    Next you need to evaluate if the keys have the the values filled correctly.
    Only output a one-word string in JSON format at the key 'result' - Yes/No.
    Thought 1 - Output a string 'Yes' if the values are correctly filled for all keys, otherwise output 'No'.
    Thought 2 - If the answer is No, mention the reason in the key 'reason'.
    THought 3 - Think carefully before answering.
    """

    messages=[{"role": "system", "content":prompt },
              {"role": "user", "content":f"""Here is the input: {response_assistant}""" }]

    response = openai.ChatCompletion.create(
                                    model="gpt-3.5-turbo",
                                    messages = messages,
                                    response_format={ "type": "json_object" },
                                    seed = 1234
                                    # n = 5
                                    )

    json_output = json.loads(response.choices[0].message.content)

    return json_output