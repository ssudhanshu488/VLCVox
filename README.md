# VLCVox

VoiceVLC is a Python-based project that integrates VLC Media Player with a voice-activated AI agent. It allows users to control VLC playback using voice commands, such as "play," "pause," "fast forward 10 seconds," or "set volume to 50%," triggered by a wake word ("Hello Media Player"). The system uses speech recognition, natural language processing (NLP) via Google's Gemini API, and VLC's HTTP interface to provide a seamless, hands-free media control experience.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ssudhanshu488/VoiceVLC.git
   cd VoiceVLC
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create a `.env` file in the project root:
     ```bash
     echo "GEMINI_API_KEY=your_gemini_api_key" > .env
     ```
   - Replace `your_gemini_api_key` with your Google Gemini API key.
   - Ensure the Picovoice access key is set in `wakemyai.py` (variable `ACCESS_KEY`).

5. **Set Up VLC HTTP Interface**:
   - Open VLC Media Player.
   - Go to Tools > Preferences > Show settings: All.
   - Under Interface > Main interfaces, enable "Web" to activate the Lua HTTP interface.
   - Under Interface > Main interfaces > Lua, set a password (default: "1234" in the code, change in `vlc_api_handle.py` if needed).
   - Save and restart VLC.
   - Verify by accessing `http://localhost:8080` in a browser (login with blank username and your password).


