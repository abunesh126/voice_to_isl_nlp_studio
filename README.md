# Voice-to-ISL NLP Studio

A local-first educational application that captures microphone audio, converts speech into text using **OpenAI Whisper Base**, performs NLP analysis on the recognized text, and generates an **Indian Sign Language (ISL)-oriented gloss sequence** using transparent, rule-based grammar processing with optional BERT contextual features.

> **Important:** This project provides an educational ISL-oriented gloss baseline. It is not a fully validated Indian Sign Language translation system. Accurate natural ISL translation requires linguistic validation, appropriate sign-language datasets, and further model development.

## Features

- **Interactive Dashboard:** React, TypeScript, and Vite frontend with five functional pages.
- **Audio Input:** Record speech directly through the browser microphone or upload WAV audio files.
- **Speech Recognition:** Local Whisper Base inference through FastAPI without requiring paid APIs.
- **GPU Acceleration:** Automatically uses an NVIDIA CUDA-compatible GPU when available, with CPU fallback.
- **Text Preprocessing:** Text normalization, regex-based cleaning, tokenization, stopword analysis, stemming, and lemmatization.
- **Linguistic Analysis:** POS tagging and dependency analysis using spaCy.
- **BERT Integration:** Optional contextual embeddings using Hugging Face Transformers, with locally cached model files.
- **ISL Gloss Generation:** Rule-based gloss generation with editable grammar rules and sample sentences.
- **NLP Analytics:** TF-IDF, basic sentiment analysis, n-gram analysis, keyword extraction, entity extraction, and text summarization.
- **Speech Analytics:** Audio waveform, duration, sample rate, and spectrogram-related analysis.
- **Evaluation:** Word Error Rate (WER), Character Error Rate (CER), gloss exact-match score, and processing latency using user-provided references.
- **System Monitoring:** Backend health, model availability, GPU information, and API connection status.
- **Data Export:** Export transcripts, generated glosses, and NLP analysis results in JSON or text format.

## System Requirements

- Windows 10 or Windows 11 (64-bit).
- Python 3.12 or Python 3.11.
- Node.js 20 LTS or newer.
- NVIDIA GPU and a compatible driver for CUDA acceleration.
- FFmpeg installed and accessible through the system PATH, or the bundled `imageio-ffmpeg` fallback.
- Internet access for the initial installation and model downloads.

**Offline support:** Once dependencies and the required models have been downloaded, speech recognition and NLP inference can run locally without an internet connection.

## Quick Start – Windows

1. Extract the ZIP archive into a folder with a short path, for example:

   `C:\Projects\voice_to_isl_nlp_studio`

2. Install Python and Node.js if they are not already available.

3. Run `setup.bat` and wait for the dependencies and model downloads to complete.

4. Run `start.bat` to launch the backend and frontend services.

5. Open the frontend URL displayed in the terminal. The default address is:

   `http://localhost:5173`

**Setup details:**

- The setup script prefers Python 3.12 and falls back to Python 3.11.
- PyTorch is installed using CUDA 12.6 wheels by default.
- System FFmpeg is preferred; if it is unavailable, the bundled `imageio-ffmpeg` executable is used automatically. The setup script only attempts `winget` when neither is available.
- Whisper Base is downloaded and cached for local inference.

If the CUDA 12.6 PyTorch build is incompatible with your NVIDIA driver or environment, install a compatible version from the official [PyTorch installation page](https://pytorch.org/get-started/locally/) and rerun the setup.

## Manual Installation

### 1. Backend Setup

Open Command Prompt or PowerShell in the project directory and navigate to the backend folder:

```powershell
cd backend
```

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install PyTorch with CUDA 12.6 support for NVIDIA GPUs:

```powershell
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

Install the backend dependencies:

```powershell
python -m pip install -r requirements.txt
```

Download the spaCy English language model:

```powershell
python -m spacy download en_core_web_sm
```

### 2. Download the Whisper Base Model

Run the following command to download and cache Whisper Base:

```powershell
python -c "import whisper, torch; whisper.load_model('base', device='cuda' if torch.cuda.is_available() else 'cpu')"
```

The model will automatically use CUDA when available and fall back to CPU otherwise.

### 3. Optional BERT Model Setup

To download and cache the BERT model locally, execute:

```powershell
python -c "from transformers import AutoTokenizer, AutoModel; n='bert-base-uncased'; AutoTokenizer.from_pretrained(n); AutoModel.from_pretrained(n)"
```

BERT is optional. The application can still perform gloss generation and its other NLP operations without it.

### 4. Frontend Setup

Open another terminal and navigate to the frontend directory:

```powershell
cd frontend
```

Install the required Node.js packages:

```powershell
npm install
```

Start the frontend development server:

```powershell
npm run dev
```

### 5. Start the Backend Server

In a separate terminal, navigate to the backend directory:

```powershell
cd backend
```

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

Start the FastAPI server:

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend API will be available at:

`http://127.0.0.1:8000`

## Local Model Storage

The application stores downloaded models locally to avoid repeated downloads.

| Model | Default cache location |
|---|---|
| Whisper Base | `%USERPROFILE%\.cache\torch\whisper` |
| Hugging Face BERT | `%USERPROFILE%\.cache\huggingface\hub` |

Model binaries are not included in the ZIP archive to keep the project size manageable. They are downloaded automatically during setup or the first model initialization.

## API Endpoints

The FastAPI backend provides the following endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Check backend health |
| GET | `/api/system` | Retrieve system and hardware information |
| POST | `/api/transcribe` | Transcribe uploaded audio |
| POST | `/api/analyze` | Perform NLP analysis on text |
| POST | `/api/gloss` | Generate ISL-oriented gloss |
| POST | `/api/evaluate` | Evaluate transcription and gloss results |
| GET | `/api/examples` | Retrieve example sentences |
| GET | `/api/gloss-rules` | Retrieve current gloss-generation rules |
| PUT | `/api/gloss-rules` | Update gloss-generation rules |

## Troubleshooting

**1. GPU is not detected**

- Run `nvidia-smi` to check NVIDIA GPU availability.
- Activate the backend virtual environment.
- Execute:

  ```powershell
  python -c "import torch; print(torch.cuda.is_available())"
  ```

- If CUDA is unavailable, verify that your PyTorch installation matches your NVIDIA driver. The application can use CPU as a fallback.

**2. Whisper takes longer during the first run**

Whisper Base must be downloaded and initialized before the first transcription. Subsequent runs can reuse the cached model.

**3. Microphone is not working**

- Allow microphone permissions in Chrome or Microsoft Edge.
- Check Windows microphone privacy settings.
- Use `localhost` for browser microphone access.
- Ensure no other application is exclusively using the microphone.

**4. Port is already in use**

If port `8000` or `5173` is occupied, close the conflicting process or update the port configuration in `start.bat` and `frontend/vite.config.ts`.

**5. BERT is unavailable**

BERT is an optional feature. Other NLP operations and rule-based gloss generation should continue to work. Use the BERT initialization option on the NLP page when you want to load the model.

**6. Transcription or gloss accuracy is low**

- Speak clearly and use a quiet environment.
- Review the recognized transcript before generating gloss.
- Check the generated gloss against appropriate ISL linguistic references.
- Remember that the current gloss generator is a rule-based educational baseline, not a complete ISL translation model.

## Project Structure

```text
voice_to_isl_nlp_studio/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── routes/
│       │   └── api.py
│       └── services/
│           ├── speech.py
│           ├── nlp.py
│           ├── gloss.py
│           └── evaluation.py
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
│           └── api.ts
│
├── setup.bat
├── start.bat
└── README.md
```

## Project Objective

The primary objective of Voice-to-ISL NLP Studio is to demonstrate how speech recognition, natural language processing, contextual language representations, and rule-based gloss generation can work together in an accessibility-focused application.

The project provides an interactive environment for exploring speech processing and NLP concepts while demonstrating a possible foundation for future Indian Sign Language translation research."# voice_to_isl_nlp_studio" 
