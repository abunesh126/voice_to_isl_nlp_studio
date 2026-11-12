
@echo off
setlocal

cd /d "%~dp0"

echo ==================================================
echo       Voice-to-ISL NLP Studio - Setup
echo ==================================================
echo.

REM ------------------------------------------
REM 1. Check Python
REM ------------------------------------------
where python >nul 2>nul

if errorlevel 1 (
    echo ERROR: Python was not found in PATH.
    echo Install Python 3.12 and enable Add Python to PATH.
    pause
    exit /b 1
)

python --version
echo.

REM ------------------------------------------
REM 2. Check Python version
REM ------------------------------------------
python -c "import sys; exit(0 if sys.version_info.major == 3 and sys.version_info.minor in (11,12) else 1)"

if errorlevel 1 (
    echo ERROR: Python 3.11 or 3.12 is required.
    pause
    exit /b 1
)

REM ------------------------------------------
REM 3. Check Node.js
REM ------------------------------------------
where node >nul 2>nul

if errorlevel 1 (
    echo ERROR: Node.js was not found.
    echo Install Node.js 20 LTS or newer.
    pause
    exit /b 1
)

node --version
npm --version
echo.

REM ------------------------------------------
REM 4. Create virtual environment
REM ------------------------------------------
if not exist "backend\.venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    python -m venv backend\.venv

    if errorlevel 1 (
        echo ERROR: Could not create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Existing virtual environment found.
)

call backend\.venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERROR: Could not activate virtual environment.
    pause
    exit /b 1
)

echo.
echo Active Python:
python --version
echo.

REM ------------------------------------------
REM 5. Upgrade pip
REM ------------------------------------------
echo Upgrading pip...
python -m pip install --upgrade pip

REM ------------------------------------------
REM 6. Install PyTorch with CUDA 12.6
REM ------------------------------------------
echo.
echo Checking PyTorch installation...

python -c "import torch; print('PyTorch:',torch.__version__); print('CUDA available:',torch.cuda.is_available())" >nul 2>nul

if errorlevel 1 (
    echo Installing PyTorch with CUDA 12.6 support...
    python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

    if errorlevel 1 (
        echo CUDA installation failed.
        echo Trying standard PyTorch installation...
        python -m pip install torch torchvision torchaudio
    )
) else (
    echo PyTorch is already installed. Skipping installation.
)

REM ------------------------------------------
REM 7. Install backend requirements
REM ------------------------------------------
echo.
echo Installing backend requirements...

python -m pip install -r backend\requirements.txt

if errorlevel 1 (
    echo ERROR: Backend dependency installation failed.
    pause
    exit /b 1
)

REM ------------------------------------------
REM 8. Check spaCy English model
REM ------------------------------------------
echo.
echo Checking spaCy English model...

python -c "import spacy; spacy.load('en_core_web_sm')" >nul 2>nul

if errorlevel 1 (
    echo Downloading spaCy English model...
    python -m spacy download en_core_web_sm

    if errorlevel 1 (
        echo WARNING: spaCy model download failed.
        echo The application may use its fallback NLP processing.
    )
) else (
    echo spaCy English model is already installed.
)

REM ------------------------------------------
REM 9. Check FFmpeg
REM ------------------------------------------
echo.
where ffmpeg >nul 2>nul

if errorlevel 1 (
    echo System FFmpeg was not found. Checking the bundled imageio-ffmpeg fallback...
    python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" >nul 2>nul

    if not errorlevel 1 (
        echo Bundled FFmpeg is available. Whisper will use it automatically.
        goto :ffmpeg_done
    )

    echo WARNING: No usable FFmpeg executable was found.
    echo Whisper needs FFmpeg to process audio files.

    where winget >nul 2>nul

    if not errorlevel 1 (
        echo Attempting FFmpeg installation...
        winget install --id Gyan.FFmpeg.Shared --exact --accept-package-agreements --accept-source-agreements
        echo.
        echo If FFmpeg is still not detected, restart CMD and run setup again.
    ) else (
        echo Install FFmpeg from:
        echo https://ffmpeg.org/download.html
    )
) else (
    echo FFmpeg is installed.
    ffmpeg -version
)

:ffmpeg_done
REM ------------------------------------------
REM 10. Download Whisper Base
REM ------------------------------------------
echo.
echo Checking and downloading Whisper Base model...

python -c "import whisper,torch; d='cuda' if torch.cuda.is_available() else 'cpu'; print('Device:',d); print('GPU:',torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'); whisper.load_model('base',device=d); print('Whisper Base loaded successfully')"

if errorlevel 1 (
    echo WARNING: Whisper download or initialization failed.
    echo The application can retry when the model is loaded.
)

REM ------------------------------------------
REM 11. Install frontend packages
REM ------------------------------------------
echo.
echo Installing frontend dependencies...

cd /d "%~dp0frontend"

if errorlevel 1 (
    echo ERROR: Frontend folder not found.
    pause
    exit /b 1
)

call npm install

if errorlevel 1 (
    echo ERROR: Frontend installation failed.
    pause
    exit /b 1
)

cd /d "%~dp0"

REM ------------------------------------------
REM 12. Setup completed
REM ------------------------------------------
echo.
echo ==================================================
echo             SETUP PROCESS FINISHED
echo ==================================================
echo.
echo Backend environment:
echo backend\.venv
echo.
echo Frontend dependencies:
echo frontend\node_modules
echo.
echo Run start.bat to launch the application.
echo.
pause
