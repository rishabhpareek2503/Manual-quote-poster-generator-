@echo off
REM Run script for Quote Poster Generator

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Running setup...
    call setup.bat
    if %ERRORLEVEL% NEQ 0 (
        echo Setup failed. Please check the error messages above.
        pause
        exit /b 1
    )
)

REM Activate virtual environment and run the application
call venv\Scripts\activate
python -m app.main %*

REM Keep the window open if there was an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo The application exited with an error (Code: %ERRORLEVEL%)
    pause
)
