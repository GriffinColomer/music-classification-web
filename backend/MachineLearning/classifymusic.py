import os
import uuid
import torch
import librosa
import librosa.display
import noisereduce as nr
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from pydub import AudioSegment
import torchvision.transforms as transforms

# Load the TorchScript model
model_path = os.path.join(os.path.dirname(__file__), "cnn_scripted.pt")
model = torch.jit.load(model_path, map_location=torch.device("cpu"))
model.eval()

# Define your genre classes
class_names = ['classical', 'jazz', 'rock', 'pop', 'metal', 'blues', 'reggae', 'hiphop', 'country', 'disco']

# Transform to prepare spectrogram for model
image_transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

def preprocess_audio_to_spectrogram(audio_path, gain_db=5, output_image_path="spectrogram.png"):
    # Boost volume 
    audio = AudioSegment.from_file(audio_path)
    louder = audio + gain_db
    boosted_path = os.path.splitext(audio_path)[0] + f"_boosted_{str(uuid.uuid4())}.wav"
    print(boosted_path)
    louder.export(boosted_path, format="wav")

    # Load and reduce noise
    y, sr = librosa.load(boosted_path, sr=48000)
    y_denoised = nr.reduce_noise(y=y, sr=sr, stationary=True, prop_decrease=0.2)

    # Generate spectrogram
    mel_spec = librosa.feature.melspectrogram(y=y_denoised, sr=sr, n_mels=128)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    
    # Save spectrogram image
    plt.figure(figsize=(2, 2))
    librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    return output_image_path

def audio_to_spectrogram(audio_path, output_image_path="non_blob_spectrogram.png"):
    
    
    # Save spectrogram image
    plt.figure(figsize=(2, 2))
    librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def get_genre_from_audio(audio_path, blob=False):
    print(audio_path)
    if blob:
        spectrogram_path = preprocess_audio_to_spectrogram(audio_path)
    else:
        spectrogram_path = audio_to_spectrogram(audio_path)
    image = Image.open(spectrogram_path).convert("RGB")
    input_tensor = image_transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        predicted_class = output.argmax(dim=1).item()
    
    return class_names[predicted_class]
