import os
import requests
import time
import logging
import datetime
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define Reddit user and destination folder
user = "RailScales"
folder = "reddit_images"
base_url = f"https://www.reddit.com/user/{user}/submitted/.json"

# Create folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

# Initialize session with retries and backoff factor
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# Set headers
headers = {'User-Agent': 'Mozilla/5.0'}

# Set initial 'after' parameter
after = None

while True:
    # Construct URL with 'after' parameter if it exists
    url = base_url if after is None else f"{base_url}?after={after}"

    # Request user submissions in json format
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        break
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection Error: {e}")
        break
    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout Error: {e}")
        break
    except requests.exceptions.RequestException as e:
        logging.error(f"Request Exception: {e}")
        break

    # Parse the JSON
    data = response.json()

    # Go through each post made by the user
    for child in data['data']['children']:
        submission = child['data']
        # If it's an image
        if submission['url'].endswith(('.jpg', '.png', '.gif', '.jpeg')):
            image_url = submission['url']
            image_name = os.path.basename(urlparse(image_url).path)

            # Get the current date and format it
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            # Append the date to the image name
            image_name_with_date = f"{current_date}_{image_name}"

            image_path = os.path.join(folder, image_name_with_date)

            if not os.path.exists(image_path):
                try:
                    image_response = session.get(image_url, headers=headers)
                    image_response.raise_for_status()
                    with open(image_path, 'wb') as f:
                        f.write(image_response.content)
                        logging.info(f"Downloaded {image_name_with_date}")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Failed to download {image_url}: {e}")
    
    # Get 'after' field from the response for the next page
    after = data['data']['after']

    # If 'after' is None, we've reached the last page, so break the loop
    if after is None:
        break

    # Respect Reddit's rate limit
    time.sleep(1)
