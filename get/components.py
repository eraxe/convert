import requests

def download_file(url: str, local_path: str):
    response = requests.get(url)
    with open(local_path, 'wb') as f:
        f.write(response.content)
