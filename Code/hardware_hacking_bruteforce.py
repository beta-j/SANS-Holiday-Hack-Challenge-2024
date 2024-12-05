import requests
#import uuid
import time

url = 'https://hhc24-hardwarehacking.holidayhackchallenge.com/api/v1/complete'

def submit_data():
  data = {
    "requestID": "db2fdd08-247f-4e4e-9a1f-a642bf90a72b",
    "serial":[3, 9, 2, 2, 0, 3],
    "voltage":3
    }

  try:
      # Make the POST request
      response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})

    # Check the response status
      if response.status_code == 200:
        print("Data submitted successfully!")
      else:
        print(f"Failed to submit data. Status code: {response.status_code}")
        print(response.text)
  except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
  
submit_data()
