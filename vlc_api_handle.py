import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import os

VLC_PASSWORD = "1234"
VLC_URL = "http://localhost:8080/requests/status.json"
AUTH = HTTPBasicAuth('', VLC_PASSWORD)

def get_status():
    response = requests.get(VLC_URL, auth=AUTH)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error getting status:", response.text)
        return None

def get_video_path():
    status = get_status()
    print("Status JSON:", status)  # Debug
    if status:
        meta = status.get('information', {}).get('category', {}).get('meta', {})
        # Try 'uri' first
        uri = meta.get('uri')
        if uri and uri.startswith('file://'):
            path = urllib.parse.unquote(uri[7:])
            if os.name == 'nt':
                path = path.lstrip('/')
            print("Path from URI:", path, "Exists:", os.path.exists(path))
            return path if os.path.exists(path) else None
        # Fallback to 'filename'
        filename = meta.get('filename')
        if filename:
            # Assume file is in T:/VLC with AI Integration/ (adjust if needed)
            base_dir = r"C:\Users\ssudh\Downloads\New folder (2)"
            path = os.path.join(base_dir, filename)
            print("Path from filename:", path, "Exists:", os.path.exists(path))
            return path if os.path.exists(path) else None
    print("No valid path found.")
    return None

def get_current_time():
    status = get_status()
    if status:
        return status.get('time', 0)
    return None

def control_vlc(action, value=None):
    params = {"command": action}
    if value:
        params["val"] = value
    response = requests.get(VLC_URL, auth=AUTH, params=params)
    if response.status_code == 200:
        print(f"Command executed: {action} {value if value else ''}")
    else:
        print("Error:", response.text)

def map_to_vlc_action(parsed_action):
    mapping = {
        "play": "pl_play",
        "pause": "pl_pause",
        "next": "pl_next",
        "previous": "pl_previous",
        "stop": "pl_stop",
        "seek": "seek",
        "volume": "volume",
        "subtitle_delay": "subtitle_delay",
        "fullscreen": "fullscreen"
    }
    return mapping.get(parsed_action, None)