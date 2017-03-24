import googlemaps, requests, json
from datetime import datetime

# Reads the Google API key safely
google_API_key_file = open('googleAPI-key.txt', 'r')
google_API_key = google_API_key_file.read()
google_API_key_file.close()

# Set up the Google API
gmaps = googlemaps.Client(key=google_API_key)

# Makes a simple request
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Saves result
response_file = open('response.json', 'w')
response = json.dump(geocode_result, response_file)
response_file.close()