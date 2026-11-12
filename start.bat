
@echo off
setlocal

cd /d "%~dp0"

echo ==================================================
echo       Voice-to-ISL NLP Studio - Launcher
echo ==================================================
echo.

REM ------------------------------------------
REM 1. Check backend environment
REM ------------------------------------------
if not exist "backend\.venv\Scripts\python.exe" (
    echo ERROR: Python virtual environment not found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM ------------------------------------------
REM 2. Check frontend dependencies
REM ------------------------------------------
if not exist "frontend\node_modules" (
    echo ERROR: Frontend dependencies not found.
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM ------------------------------------------
REM 3. Start backend
REM ------------------------------------------
echo Starting FastAPI backend...

start "Voice-to-ISL Backend" /D "%~dp0backend" cmd /k ".venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

REM Wait for backend startup
timeout /t 3 /nobreak >nul

REM ------------------------------------------
REM 4. Start frontend
REM ------------------------------------------
echo Starting React frontend...

start "Voice-to-ISL Frontend" /D "%~dp0frontend" cmd /k "npm run dev -- --host 127.0.0.1"

REM Wait for frontend startup
timeout /t 5 /nobreak >nul

REM ------------------------------------------
REM 5. Open browser
REM ------------------------------------------
echo Opening application...

start "" "http://localhost:5173"

echo.
echo ==================================================
echo          APPLICATION LAUNCH COMMANDS SENT
echo ==================================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Keep both terminal windows open.
echo Close them to stop the application.
echo.
pause
