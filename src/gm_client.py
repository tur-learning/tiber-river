import requests

# Construct the URL with the necessary parameters
url = "https://maps.googleapis.com/maps/api/staticmap"
params = {
    "center": "40.714728,-73.998672",
    "zoom": "13",
    "size": "600x300",
    "format": "png",
    "key": "**************"
}

# Send a GET request to the API and save the response as a PNG image
response = requests.get(url, params=params)
with open("map.png", "wb") as f:
    f.write(response.content)
