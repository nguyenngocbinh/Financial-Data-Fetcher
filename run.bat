@echo off
echo =====================================================
echo    Financial Data Fetcher - Quick Start
echo =====================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

:: Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not installed
    echo Please install pip
    pause
    exit /b 1
)

echo Python and pip are installed.
echo.

:: Install requirements
echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo.

:: Menu
:menu
echo What would you like to do?
echo 1. Run example demo
echo 2. Start web dashboard
echo 3. Run scheduler
echo 4. Run comprehensive tests
echo 5. Clean up cache and temp files
echo 6. Build package
echo 7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto demo
if "%choice%"=="2" goto dashboard
if "%choice%"=="3" goto scheduler
if "%choice%"=="4" goto test_all
if "%choice%"=="5" goto clean
if "%choice%"=="6" goto build
if "%choice%"=="7" goto exit
echo Invalid choice. Please try again.
goto menu

:demo
echo.
echo Running example demo...
python scripts\example.py
pause
goto menu

:dashboard
echo.
echo Starting web dashboard...
echo You can access the dashboard at: http://127.0.0.1:8050
echo Press Ctrl+C to stop the dashboard
python -m financial_data_fetcher.dashboard
pause
goto menu

:scheduler
echo.
echo Starting scheduler...
echo Press Ctrl+C to stop the scheduler
python -m financial_data_fetcher.scheduler
pause
goto menu

:test_all
echo.
echo Running comprehensive tests...
python -m pytest tests/ -v
pause
goto menu

:clean
echo.
echo Cleaning up cache and temp files...
python scripts\clean.py
pause
goto menu

:build
echo.
echo Building package...
python -m build
echo Package built successfully! Check dist/ folder.
pause
goto menu

:exit
echo.
echo Thank you for using Financial Data Fetcher!
pause
exit /b 0
