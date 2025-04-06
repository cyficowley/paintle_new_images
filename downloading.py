import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# Your list of image URLs
image_urls = [...]  # replace with your list
output_dir = "downloaded_images"
os.makedirs(output_dir, exist_ok=True)



with open('urls.json') as json_data:
    urls = json.load(json_data)

print(len(urls))


# Function to download a single image
def download_image(url, index):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        ext = url.split('.')[-1].split('?')[0][:4]  # crude way to get extension
        filename = f"image_{index:04d}.{ext}"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filename
    except Exception as e:
        return f"Failed to download {url}: {e}"

# Download images in parallel
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(download_image, url, i) for i, url in enumerate(image_urls)]
    for future in as_completed(futures):
        print(future.result())
