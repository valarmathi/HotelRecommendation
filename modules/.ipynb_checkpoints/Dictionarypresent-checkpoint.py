import openai

def dictionary_present(response):
    delimiter = "####"
    user_req = {
                      "City":"Banashankari", "RestaurantType":"Casual Dining", "ApproximateCost":"NA", "Cuisine":"South Indian", "Votes":"high"
                }
    
    prompt = f"""You are a python expert. You are provided an input.
            You have to check if the python dictionary is present in the string is valid and all the values are filled in as expected by user.
            It will have the following format {user_req}.
            Your task is to just extract and return only the python dictionary from the input.
            The output should match the format as {user_req}.
            The output should contain the exact keys and values as present in the input.
            Do not add currency in ApproximateCost instead it should be just a numerical value.
            Double-check the output before displaying it to the user.

            Here are some sample input output pairs for better understanding:
            {delimiter}
            input: - City: Banashankari - RestaurantType: Casual Dining - ApproximateCost: NA - Cuisine: South Indian - Votes: high
            output: {{"City":"Banashankari", "RestaurantType":"Casual Dining", "ApproximateCost":0, "Cuisine":"South Indian", "Votes":"high"}}

            input: {{"City":"Banashankari", "RestaurantType":"Casual Dining", "ApproximateCost":"8,000 Rs", "Cuisine":"South Indian", "Votes":'high'}}
            output: {{"City":"Banashankari", "RestaurantType":"Casual Dining", "ApproximateCost":8000, "Cuisine":"South Indian", "Votes":"high"}}

            input: Here is your user profile "City":"Banashankari", "RestaurantType":"Casual Dining", "ApproximateCost":"700 INR", "Cuisine":"South Indian", "Votes":'high'
            output: {{"City":"Banashankari", "RestaurantType":"Casual Dining", "ApproximateCost":700, "Cuisine":"South Indian", "Votes":"high"}}
            {delimiter}

            Here is the input {response}
            Please reconfirm that you are returning only Json string as output to the user.
            """

    conversation = [{"role": "system", "content": prompt}]
    #print(conversation)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages = conversation
    )
    return response.choices[0].message.content