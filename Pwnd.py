import requests

# Set the API endpoint and breach name to check
url = 'https://haveibeenpwned.com/api/v3/breach'
breach_name = '<Breach Name>'

# Set the API headers with your API key
api_key = '<API-KEY>'
headers = {
    'hibp-api-key': api_key
}

# Send a GET request to the API endpoint with the breach name
response = requests.get(f"{url}/{breach_name}", headers=headers)
if response.status_code != 200:
    raise Exception(f"Failed to retrieve data: {response.status_code}")
breach_data = response.json()
print(breach_data)

# Print the data for the specified breach
print(f"Data for '{breach_name}' breach:")

print(f"Title: {breach_data['Title']}")
print(f"Breach date: {breach_data['BreachDate']}")
print(f"Pwn count: {breach_data['PwnCount']}")
