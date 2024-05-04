import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Define Reddit user and destination folder
user = "RailScales"
folder = "reddit_images"
base_url = f"https://www.reddit.com/user/{user}/submitted/.json"

# Create folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

# Set headers
headers = {'User-Agent': 'Mozilla/5.0'}

# Set initial 'after' parameter
after = None

while True:
    # Construct URL with 'after' parameter if it exists
    url = base_url if after is None else f"{base_url}?after={after}"

    # Request user submissions in json format
    response = requests.get(url, headers=headers)

    # Ensure we got a successful response
    if response.status_code != 200:
        print(f"Failed to get page: {response.status_code}")
        break

    # Parse the JSON
    data = response.json()

    # Go through each post made by the user
    for child in data['data']['children']:
        submission = child['data']
        # If it's an image
        if submission['url'].endswith(('.jpg', '.png', '.gif', '.jpeg')):
            # Download image
            image_response = requests.get(submission['url'], headers=headers)
            # Parse the URL to get the image's name
            image_name = os.path.basename(urlparse(submission['url']).path)
            # Save the image to the destination folder
            with open(os.path.join(folder, image_name), 'wb') as f:
                f.write(image_response.content)
    
    # Get 'after' field from the response for the next page
    after = data['data']['after']

    # If 'after' is None, we've reached the last page, so break the loop
    if after is None:
        break