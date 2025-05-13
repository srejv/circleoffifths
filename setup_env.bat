@echo off

echo Setting up the Python environment for Circle of Fifths...

:: Step 1: Create a virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

:: Step 2: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Step 3: Upgrade pip
echo Upgrading pip...
pip install --upgrade pip

:: Step 4: Install dependencies
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo No requirements.txt found. Skipping dependency installation.
)

echo Environment setup complete. To activate the virtual environment, run:
echo venv\Scripts\activate