import deepspeech
import numpy as np
import base64
import wave
import os
import ffmpeg
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")


model_path = "models/deepspeech-0.9.3-models.pbmm"
scorer_path = "models/deepspeech-0.9.3-models.scorer"
model = deepspeech.Model(model_path)
model.enableExternalScorer(scorer_path)

AUDIO_FILE = "recorded_audio.wav"

def save_audio(audio_bytes):
    """Save received audio to a WAV file with correct format."""
    raw_file = "recorded_audio.webm"

    with open(raw_file, "wb") as f:
        f.write(audio_bytes)

    
    try:
        (
            ffmpeg
            .input(raw_file)
            .output(AUDIO_FILE, format="wav", acodec="pcm_s16le", ar="16k", ac=1)
            .run(overwrite_output=True, quiet=True)
        )
        print("✅ Audio converted to WAV format successfully!")
    except Exception as e:
        print(f"❌ Audio conversion failed: {e}")

def transcribe_audio():
    """Convert saved audio file to text using DeepSpeech."""
    if not os.path.exists(AUDIO_FILE):
        print("❌ No recorded audio found")
        return ""

    print(f"🔍 Processing {AUDIO_FILE} for transcription...")

    with wave.open(AUDIO_FILE, "rb") as wf:
        sample_rate = wf.getframerate()
        num_frames = wf.getnframes()
        audio_data = wf.readframes(num_frames)

    audio_np = np.frombuffer(audio_data, dtype=np.int16)

    print(f"🔍 Sending {len(audio_np)} samples to DeepSpeech")

    try:
        text = model.stt(audio_np)
        print(f"📝 Transcribed Text: {text}")
        return text
    except Exception as e:
        print(f"❌ DeepSpeech Error: {str(e)}")
        return ""

@socketio.on("stop_recording")
def handle_stop_recording(data):
    """Handle the stop recording event and process the saved audio."""
    print("🛑 Recording stopped. Processing audio...")

    audio_bytes = base64.b64decode(data["audio"])
    save_audio(audio_bytes)

    transcription = transcribe_audio()
    socketio.emit("update_text", {"transcription": transcription})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
