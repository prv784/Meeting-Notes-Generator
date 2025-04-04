import deepspeech
import numpy as np
import wave

# Load DeepSpeech model
model_path = "models/deepspeech-0.9.3-models.pbmm"
scorer_path = "models/deepspeech-0.9.3-models.scorer"
model = deepspeech.Model(model_path)
model.enableExternalScorer(scorer_path)

def transcribe_audio(filename="test.wav"):
    with wave.open(filename, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(frames, dtype=np.int16)
        text = model.stt(audio_data)
        print("Manual Transcription:", text)

# Run transcription
transcribe_audio("test.wav")
