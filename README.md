                        ReadMe 

🎙️ CoquiPipeline

A fully local **speech-to-text + AI reply + text-to-speech** system using **Whisper**, **LM Studio**, and **CoquiTTS**.  
No cloud, no API keys — 100% offline.

---

🛠 Requirements
<img width="1920" height="1080" alt="logo with name on them 1" src="https://github.com/user-attachments/assets/d6ed8502-fb96-4ed7-ac80-b0864d406397" />
- Python **3.10+**
- Git  
- Conda (recommended)
- LM Studio installed
- OpenAI Whisper
- Coqui TTS
- GPU with CUDA *(optional but much faster)*

✨ Features

- 💻 100% offline — runs locally on your PC  
- 🔒 No API keys or cloud services needed  
- 🧠 Works with any model in LM Studio  
- 🧩 Modular — swap in different STT/TTS engines  
- ⚡ Lightweight and GPU-accelerated (CUDA supported)  
- 🎭 Choose voice models, speakers, emotions, and even do **voice cloning**  

---

📦 Setup

1️⃣ Clone this repo
git clone https://github.com/cybdicplus/LM-Studio-Speech-to-Speech.git
cd LM-Studio-Speech-to-Speech

2️⃣ Install Whisper (Speech-to-Text)
conda create -n whisper python=3.10.11 -y
conda activate whisper
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -U openai-whisper

3️⃣ Install CoquiTTS (Text-to-Speech)

1. Create a folder named CoquiTTS.

2. Open it in CMD:

Click the path bar
Delete the path
Type cmd
Press Enter

Then run:
conda create -n coqui python=3.10 -y
conda activate coqui
git clone https://github.com/coqui-ai/TTS.git
cd TTS
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install TTS
pip install sounddevice numpy openai-whisper requests termcolor pyfiglet keyboard

Then create another folder named CoquiPipeline and place inside it:
CoquiPipeline/
├─ pipeline_Coqui.py
└─ start_sts.bat

▶️ Starting the Pipeline

You can start the voice pipeline in **two ways**:

🧠 1. Run it manually (no `.bat` file)

Open your terminal or Anaconda Prompt and run:
conda activate coqui
cd C:\Users\<YOUR_USERNAME>\CoquiPipeline
python pipeline_Coqui.py
Replace <YOUR_USERNAME> with your Windows username.

⚙️ 2. Create your own start_sts.bat file (optional)
If you want to start it by double-clicking, make your own .bat file:

1. Open Notepad

2. Paste the following:
@echo off
echo ========================================
echo   🚀 Starting Whisper + LM Studio + Coqui TTS Pipeline
echo ========================================

:: Activate your Conda environment
call conda activate coqui

:: Go to your CoquiPipeline folder
cd /d C:\Users\<YOUR_USERNAME>\CoquiPipeline

:: Run the Python script
python pipeline_Coqui.py

pause

3. Replace <YOUR_USERNAME> with your actual username

4. Save the file as: start_sts.bat

5. Double-click it to start your voice pipeline automatically 🎯


To start, just double-click start_sts.bat ✅
4️⃣ LM Studio Setup

1. Download LM Studio → https://lmstudio.ai

2. Install and run a local model (Qwen, Llama, Mistral, etc.)

3. Enable the Local Server API (default:
   http://localhost:1234/v1/chat/completions)

Switching models:
Just switch models inside LM Studio — your Python script automatically uses the active one.

Recommended uncensored models:

uncensoredai_UncensoredLM-DeepSeek-R1-Distill-Qwen-14B
Dolphin3.0-Llama3.1-8B


🚀 Usage
<img width="1920" height="1080" alt="pipeline workflow with icons" src="https://github.com/user-attachments/assets/95bc1bce-f3c3-4c0d-b61c-eb8324327112" />
1. Speak into your mic 🎤
2. Whisper → converts speech to text
3. LM Studio → generates AI reply
4. CoquiTTS → speaks the reply back 🔊

🔘 Optional Features:

Type Y for Yes or N for No

Choose by typing the number next to your option

🎙 Choose a Voice Model
| # | Model                                            | Description                                     |
| - | ------------------------------------------------ | ----------------------------------------------- |
| 1 | `tts_models/en/ljspeech/tacotron2-DDC`           | Default female voice                            |
| 2 | `tts_models/en/ljspeech/glow-tts`                | Slightly robotic                                |
| 3 | `tts_models/en/vctk/vits`                        | 109 voices available                            |
| 4 | `tts_models/multilingual/multi-dataset/your_tts` | 6 voices (3 male / 3 female) across 4 languages |


🎭 Voice Emotions
1. Neutral
2. Happy
3. Sad
4. Angry
5. Excited

🧬 Voice Cloning
When asked for a .wav file path:

Record or use your 6-second voice sample
Right-click → Copy as path
Paste it when prompted


🛑 Stop / Pause Controls
Say “stop listening” → to stop the model
Press P → pause/resume
Press S → stop speaking mid-sentence


🎬 **Demo Video**

[![Watch the video](https://img.youtube.com/vi/r3UFkIF_Hmw/0.jpg)](https://youtu.be/r3UFkIF_Hmw)



🔄 Updating
To update to the latest version:
Go to the cybdic GitHub page
Download the new pipeline_Coqui.py
Replace your old one inside CoquiPipeline


📢 Credits to:

- [Python](https://www.python.org/)
- [Git](https://git-scm.com/)
- [Conda](https://docs.conda.io/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Coqui TTS](https://github.com/coqui-ai/TTS)
- [LM Studio](https://lmstudio.ai/)
  
Thanks for making this possible 🙏😁





















                     





