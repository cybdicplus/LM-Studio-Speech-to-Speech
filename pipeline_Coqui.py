import os
import sounddevice as sd
import numpy as np
import torch
import whisper
from TTS.api import TTS
from termcolor import colored
import pyfiglet
import soundfile as sf
import requests
import threading
import time
import keyboard  # pip install keyboard

# ===============================
# 🎨 Helper functions for banners
# ===============================
def banner(text, color="cyan"):
    print(colored(pyfiglet.figlet_format(text, font="slant"), color))

def section(title, emoji="👉"):
    print(colored("\n" + "=" * 60, "yellow"))
    print(colored(f" {emoji}  {title}", "green", attrs=["bold"]))
    print(colored("=" * 60, "yellow"))

def ask_choice(prompt, options):
    print(colored(prompt, "yellow", attrs=["bold"]))
    for key, val in options.items():
        print(colored(f"  {key}: {val}", "cyan"))
    while True:
        choice = input(colored("\nSelect option: ", "yellow")).strip().upper()
        if choice in options:
            return choice
        print(colored("❌ Invalid option, try again.", "red"))

# ===============================
# 🔧 Configurations
# ===============================
STOP_PHRASE = "stop listening"

# Setup device (GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(colored(f"⚙️ Using device: {device}\n", "magenta", attrs=["bold"]))

# ===============================
# 🎤 Record with Whisper
# ===============================
def record_audio(duration=5, fs=16000):
    print(colored("🎤 Mic active... speak now!\n", "cyan", attrs=["bold"]))
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="float32")
    sd.wait()
    return np.squeeze(audio)

# ===============================
# 🎵 Play back audio with pause/stop
# ===============================
pause_flag = False
stop_flag = False

def play_audio(file_path):
    global pause_flag, stop_flag
    data, fs = sf.read(file_path, dtype="float32")
    stop_flag = False
    pause_flag = False

    def audio_thread():
        global pause_flag, stop_flag
        stream = sd.OutputStream(samplerate=fs, channels=data.shape[1] if data.ndim > 1 else 1)
        stream.start()
        i = 0
        blocksize = 1024

        while i < len(data):
            if stop_flag:
                break
            if pause_flag:
                time.sleep(0.1)
                continue
            end = i + blocksize
            stream.write(data[i:end])
            i = end

        stream.stop()
        stream.close()

    t = threading.Thread(target=audio_thread)
    t.start()

    print("▶️ Playing... Press 'p' to pause/resume, 's' to stop.")
    while t.is_alive():
        if keyboard.is_pressed("p"):
            pause_flag = not pause_flag
            print("⏸ Paused" if pause_flag else "▶️ Resumed")
            time.sleep(0.3)  # debounce
        elif keyboard.is_pressed("s"):
            stop_flag = True
            print("🛑 Stopped")
            break
        time.sleep(0.1)

    t.join()

# ===============================
# ⚙️ Load models
# ===============================
banner("COQUI TTS + WHISPER", "magenta")

# Whisper
section("Loading Whisper model", "🧠")
whisper_model = whisper.load_model("small")
print(colored("Whisper ready!\n", "cyan", attrs=["bold"]))

# ===============================
# 1️⃣ VOICE CHANGE
# ===============================
banner("VOICE SETUP 🎤", "cyan")   
voice_choice = ask_choice("Keep the default voice?", {"Y": "Yes (keep default)", "N": "No (choose another voice)"})

if voice_choice == "N":
    available_voices = [
        "tts_models/en/ljspeech/tacotron2-DDC",
        "tts_models/en/ljspeech/glow-tts",
        "tts_models/en/vctk/vits",
        "tts_models/multilingual/multi-dataset/your_tts"
    ]
    print(colored("\nAvailable Voices:", "magenta", attrs=["bold"]))
    for idx, v in enumerate(available_voices, 1):
        print(colored(f"  {idx}. {v}", "cyan"))
    while True:
        try:
            sel = int(input(colored("\n👉 Select a voice number: ", "yellow")))
            if 1 <= sel <= len(available_voices):
                selected_voice = available_voices[sel-1]
                print(colored(f"✅ Selected voice: {selected_voice}\n", "green", attrs=["bold"]))
                break
        except ValueError:
            pass
        print(colored("❌ Invalid selection, try again!", "red", attrs=["bold"]))
else:
    selected_voice = "tts_models/en/ljspeech/tacotron2-DDC"

section("Loading Coqui TTS", "🎙")
tts = TTS(selected_voice, progress_bar=False, gpu=(device=="cuda"))
print(colored("Coqui TTS ready!\n", "cyan", attrs=["bold"]))

# ===============================
# Multi-Speaker Selection
# ===============================
selected_speaker = None
if tts.speakers is not None:
    section("Multi-Speaker Model Detected", "🗣")
    print(colored("This model supports multiple speakers!\n", "cyan", attrs=["bold"]))
    for i, spk in enumerate(tts.speakers, 1):
        print(colored(f" {i}. {spk}", "green"))
    while True:
        try:
            choice = int(input(colored("\nSelect speaker number: ", "yellow")))
            if 1 <= choice <= len(tts.speakers):
                selected_speaker = tts.speakers[choice - 1]
                print(colored(f"✅ Selected speaker: {selected_speaker}\n", "green", attrs=["bold"]))
                break
        except ValueError:
            pass
        print(colored("❌ Invalid selection, try again!", "red", attrs=["bold"]))

# ===============================
# 🎭 Emotions Menu
# ===============================
emotions = ["Neutral", "Happy", "Sad", "Angry", "Excited"]
section("Voice Emotions", "🎭")
emotion_choice = ask_choice("Would you like to add an emotion?", {"Y": "Yes", "N": "No"})
selected_emotion = None
if emotion_choice == "Y":
    print(colored("\nAvailable emotions:", "cyan", attrs=["bold"]))
    for i, emo in enumerate(emotions, 1):
        print(colored(f" {i}. {emo}", "green"))
    while True:
        try:
            choice = int(input(colored("\nSelect emotion number: ", "yellow")))
            if 1 <= choice <= len(emotions):
                selected_emotion = emotions[choice - 1]
                print(colored(f"✅ Selected emotion: {selected_emotion}\n", "green", attrs=["bold"]))
                break
        except ValueError:
            pass
        print(colored("❌ Invalid selection, try again!", "red", attrs=["bold"]))

# ===============================
# 🧬 Voice Cloning Option
# ===============================
section("Voice Cloning", "🧬")
clone_choice = ask_choice("Would you like to clone a voice?", {"Y": "Yes", "N": "No"})
speaker_wav = None
if clone_choice == "Y":
    print(colored("👉 Enter path to your 6-sec .wav file: ", "yellow"), end="")
    speaker_wav = input().strip()

# ===============================
# 🎤 Main Loop
# ===============================
while True:
    section("Recording", "🎤")
    audio_data = record_audio(duration=5)
    sf.write("input.wav", audio_data, 16000)

    section("Transcribing", "📝")
    result = whisper_model.transcribe("input.wav")
    
    # ===== Modified part for empty speech =====
    transcript = result["text"].strip()
    print(colored("\n--- Transcript ---", "cyan"))
    print(transcript if transcript else "(no speech detected)")
    print(colored("-----------------", "cyan"))

    if not transcript:
        print(colored("⚠️ No speech detected. Skipping LM Studio call.\n", "yellow"))
        continue  # go back to recording
    # ==========================================

    if STOP_PHRASE in transcript.lower():
        print(colored("👋 Stop phrase detected. Exiting pipeline.", "red", attrs=["bold"]))
        break

    # Send to LM Studio
    section("LM Studio", "🤖")
    print("Sending text to LM Studio endpoint...")
    response = requests.post(
        "http://localhost:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "local-model",
            "messages": [{"role": "user", "content": transcript}],
            "temperature": 0.7,
        },
    )
    reply = response.json()["choices"][0]["message"]["content"]
    print(colored("\n--- LM Studio Response ---", "cyan"))
    print(reply)
    print(colored("---------------------------", "cyan"))

    # ===============================
    # 🔊 Generate TTS with GPU monitoring
    # ===============================
    section("Generating Speech", "🔊")
    kwargs = {}
    if selected_emotion: kwargs["emotion"] = selected_emotion
    if selected_speaker: kwargs["speaker"] = selected_speaker
    if speaker_wav: kwargs["speaker_wav"] = speaker_wav

    if device == "cuda":
        print(colored(f"⚡ VRAM Usage Before TTS: {torch.cuda.memory_allocated()/1024**2:.2f} MB", "magenta"))
    
    tts.tts_to_file(text=reply, file_path="output.wav", **kwargs)
    
    if device == "cuda":
        print(colored(f"⚡ VRAM Usage After TTS: {torch.cuda.memory_allocated()/1024**2:.2f} MB", "magenta"))

    play_audio("output.wav")

