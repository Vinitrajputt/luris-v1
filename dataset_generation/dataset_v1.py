import json
import time
from tqdm import tqdm
from groq import Groq

# Initialize Groq client dynamically with API key
api_keys = [
    'API_KEY_1_HERE', 
    'API_KEY_2_HERE', 
    'API_KEY_3_HERE'  # Add as many API keys as necessary or you can use only one
]

def initialize_client(api_key):
    return Groq(api_key=api_key)

client = initialize_client(api_keys[0])  # Start with the first key
api_key_index = 0  # Index to track current API key

# Model details for rate limiting and token handling
models = [
    {"id": "llama-3.1-70b-versatile", "requests_per_minute": 30, "tokens_per_minute": 20000, "max_tokens": 8000},
    {"id": "llama-3.2-90b-text-preview", "requests_per_minute": 30, "tokens_per_minute": 7000, "max_tokens": 8000},
    # Add more models as needed
]

# Function to interact with Groq API, sending one instruction/input pair at a time
def generate_response_with_groq(model_id, instruction, input_text):
    global client, api_key_index  # Access the client and API key index globally
    try:
        # Prepare the input messages for the model
        messages = [
            {
                "role": "system",
                "content": """
                You are a helpful assistant that thinks step-by-step to generate high-quality responses. First, use the Collection of Thoughts (COT) approach to think about the answer within <[COT]></[COT]> tags. After completing the reasoning, generate the corresponding HTML output inside <[HTML]><[/HTML]> tags. Try to make beautiful and interactive UI. Make sure to only use internal CSS and JS without referencing any local images or resources. The entire response, including both <[COT]> and <[HTML]> sections, should be in a single message.
                """
            },
            {
                "role": "user",
                "content": f"<[COT]> Think step-by-step about how to respond to the instruction below. <[/COT]> After that, generate the HTML response in the <[HTML]> tags. Instruction: {instruction}"
            },
            {
                "role": "user",
                "content": input_text
            }
        ]
        
        # Call Groq API to generate a response
        completion = client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=1,
            max_tokens=models[0]['max_tokens'],  # Ensure we stay within the token limit
            top_p=1,
            stream=False,
            stop=None
        )
        
        return completion.choices[0].message.content
    
    except Exception as e:
        print(f"Error with model {model_id}: {e}")
        # Rotate API key if an error occurs and retry
        api_key_index += 1
        if api_key_index < len(api_keys):
            print(f"Switching to next API key: {api_keys[api_key_index]}")
            client = initialize_client(api_keys[api_key_index])
            return generate_response_with_groq(model_id, instruction, input_text)
        else:
            print("All API keys have been exhausted.")
            return None

# Function to update the JSON file on the go after each response
def update_json_on_the_go(output_file, row_data):
    try:
        # Read existing data if the file exists
        try:
            with open(output_file, 'r') as outfile:
                data = json.load(outfile)
        except FileNotFoundError:
            data = []  # Create an empty list if the file doesn't exist
        
        # Append new row data
        data.append(row_data)
        
        # Write updated data to the JSON file
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile, indent=4)
    
    except Exception as e:
        print(f"Error updating JSON file: {e}")

# Function to process the dataset row by row and update JSON in real-time
def process_dataset(input_file, output_file):
    with open(input_file, 'r') as infile:
        dataset = json.load(infile)
    
    for i, row in enumerate(tqdm(dataset, desc="Processing rows")):
        instruction = row['instruction']
        input_text = row['input']
        
        # Try the primary model first
        model_id = models[0]['id']
        result = generate_response_with_groq(model_id, instruction, input_text)
        
        # If the primary model fails, try the backup model
        if not result:
            print(f"Model {model_id} failed, switching to backup model...")
            model_id = models[1]['id']
            result = generate_response_with_groq(model_id, instruction, input_text)
        
        # If both models fail, skip the row and continue
        if not result:
            print(f"Both models failed for row {i}. Skipping to the next one.")
            continue
        
        # Add the generated response to the row
        row['response'] = result
        
        # Update the JSON file after each row is processed
        update_json_on_the_go(output_file, row)

        # Respect rate limits: requests per minute and token limits
        time.sleep(60 / models[0]['requests_per_minute'])  # Delay to prevent hitting rate limits
    
    print(f"Processing complete! Results saved to {output_file}")

# Run the processing on the dataset
input_json_file = "dataset_generation/alpaca_dataset_full.json"
output_json_file = "alpaca_responses_groq.json"

process_dataset(input_json_file, output_json_file)
