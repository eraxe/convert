import requests

def send_file_to_server(file_path: str, server_url: str):
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(server_url, files=files)
    return response.status_code
