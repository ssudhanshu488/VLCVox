from wakemyai import listen_for_command
from generate_positive import process_command_with_gemini
from vlc_api_handle import control_vlc, map_to_vlc_action, get_current_time, get_video_path, get_status
import pyttsx3
import subprocess
import os
import urllib.parse

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def auto_sync_subtitles():
    speak("Starting automatic subtitle sync. This may take a moment.")
    print("Auto-syncing subtitles...")

    control_vlc('pl_pause')
    current_time = get_current_time()
    if current_time is None:
        speak("Error getting current time.")
        return

    video_path = get_video_path()
    if not video_path or not os.path.exists(video_path):
        speak("Could not find video file path.")
        print("Video path not found or invalid.")
        return

    # Check if subtitle track exists
    status = get_status()
    has_subtitle = any(stream.get('Type') == 'Subtitle' for stream in status.get('information', {}).get('category', {}).values() if isinstance(stream, dict))
    if not has_subtitle:
        speak("No subtitle track loaded in VLC.")
        print("No subtitles detected.")
        return

    # Assume external .srt (try .en.srt or .srt)
    sub_path = os.path.splitext(video_path)[0] + '.en.srt'
    if not os.path.exists(sub_path):
        sub_path = os.path.splitext(video_path)[0] + '.srt'
    if not os.path.exists(sub_path):
        speak("Subtitle file not found. Ensure it's named like the video with .en.srt or .srt.")
        print(f"Subtitle file not found: {sub_path}")
        return

    synced_sub = os.path.splitext(video_path)[0] + '_synced.srt'

    try:
        result = subprocess.run(['ffsubsync', video_path, '-i', sub_path, '-o', synced_sub], capture_output=True, text=True)
        if result.returncode != 0:
            speak("Sync failed. Check console for errors.")
            print(f"ffsubsync error: {result.stderr}")
            return
        print(f"ffsubsync output: {result.stdout}")
    except FileNotFoundError:
        speak("ffsubsync or ffmpeg not installed or not in PATH.")
        print("Install ffsubsync: pip install ffsubsync; ensure ffmpeg is in PATH.")
        return

    synced_uri = 'file:///' + urllib.parse.quote(synced_sub.replace('\\', '/'))
    control_vlc('addsubtitle', synced_uri)
    control_vlc('seek', str(current_time))
    control_vlc('pl_play')
    speak("Subtitles synced automatically.")

if __name__ == "__main__":
    while True:
        command = listen_for_command()
        if not command:
            continue

        parsed = process_command_with_gemini(command)
        print(f"Parsed: {parsed}")

        if parsed["action"] != "unknown":
            if parsed["action"] == "subtitle_sync":
                auto_sync_subtitles()
            elif parsed["action"] == "subtitle_delay":
                control_vlc("subtitle_delay", parsed.get("value"))
                speak("Subtitle delay adjusted.")
            else:
                vlc_action = map_to_vlc_action(parsed["action"])
                if vlc_action:
                    control_vlc(vlc_action, parsed.get("value"))
                else:
                    print("Unknown VLC action.")
        else:
            print("Command unclear.")


