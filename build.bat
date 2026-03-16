@echo off
echo ============================================================
echo   CursorPicker — build script
echo ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

:: Install / upgrade PyInstaller
echo [1/3] Installing PyInstaller...
pip install pyinstaller --quiet --upgrade
if errorlevel 1 (
    echo [ERROR] Could not install PyInstaller.
    pause
    exit /b 1
)

:: Build the exe
echo.
echo [2/3] Building CursorPicker.exe  (this takes ~30 seconds)...
pyinstaller --onefile --windowed --name CursorPicker cursor_picker.py
if errorlevel 1 (
    echo [ERROR] Build failed — check output above.
    pause
    exit /b 1
)

:: Copy to current folder for convenience
echo.
echo [3/3] Copying CursorPicker.exe here...
copy /Y dist\CursorPicker.exe CursorPicker.exe >nul

echo.
echo ============================================================
echo   Done!  CursorPicker.exe is ready in this folder.
echo ============================================================
echo.
pause
