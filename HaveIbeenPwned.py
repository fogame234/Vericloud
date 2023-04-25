import requests
import json

def get_breaches():
    # Set the API endpoint and parameters
    url = 'https://haveibeenpwned.com/api/v3/breaches'
    params = {'includeUnverified': 'true'}

    # Make the API request and handle the response
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to get breaches: {response.status_code}")
    data = json.loads(response.content)

    # Extract and return the list of breaches and their added date
    return [(breach['Name'], breach['BreachDate'], breach['Suffix']) for breach in data]

# Call the function and print the results
breaches = get_breaches()
for breach in breaches:
    print(f"{breach[0]} - {breach[1] - breach[2]}")
