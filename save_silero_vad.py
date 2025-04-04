import torch

# Download the Silero VAD model using Torch Hub
print("Downloading Silero VAD model...")
vad_model, utils = torch.hub.load("snakers4/silero-vad", "silero_vad", trust_repo=True)

# Extract only the actual model
model_path = "silero_vad.jit"
torch.jit.save(torch.jit.script(vad_model), model_path)

print(f"Silero VAD model saved as '{model_path}'")
