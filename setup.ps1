# Check available Python versions using py -0
$availableVersions = & py -0
if ($availableVersions -notmatch "3\.11") {
    Write-Host "Python 3.11 is required. Please install it and try again." -ForegroundColor Red
    exit 1
}

# Use Python 3.11 for the remainder of the script
$python311Path = & py -3.11 --version
if ($?) {
    Write-Host "Python 3.11 is available. Continuing..."
} else {
    Write-Host "Python 3.11 is not available. Please ensure it is installed correctly." -ForegroundColor Red
    exit 1
}

# Check for the existence of 'venv' folder in the current directory
if (-not (Test-Path "./venv")) {
    # Create a virtual environment with Python 3.11
    Write-Host "Creating virtual environment with Python 3.11..."
    & py -3.11 -m venv venv

    if ($?) {
        Write-Host "Virtual environment created successfully."
    } else {
        Write-Host "Failed to create virtual environment." -ForegroundColor Red
        exit 1
    }
}

# Activate the virtual environment
Write-Host "Activating virtual environment..."
& ./venv/Scripts/Activate

# Install required dependencies from requirements.txt
if (Test-Path "./requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    & pip install -r requirements.txt

    if ($?) {
        Write-Host "Dependencies installed successfully."
    } else {
        Write-Host "Failed to install dependencies." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "No requirements.txt file found." -ForegroundColor Yellow
}

Write-Host "Setup complete."
