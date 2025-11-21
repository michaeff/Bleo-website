# Flask Server Setup Instructions for Windows (VS Code)

This guide will help you set up and run the Lung Fibrosis Flask web application on Windows using Visual Studio Code.

## Prerequisites

Before starting, ensure you have the following installed

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"
   - Verify installation by opening Command Prompt and running: `python --version`

2. **Visual Studio Code**
   - Download from [code.visualstudio.com](https://code.visualstudio.com/)

3. **Python Extension for VS Code**
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Python" and install the official Python extension by Microsoft

## Step-by-Step Setup

### 1. 

- File → Open Folder → Select your project folder

### 2. Set up Python Environment

#### Option A: Using Virtual Environment (Recommended)
1. Open VS Code Terminal (Terminal → New Terminal or Ctrl+`)
2. Create a virtual environment:

   python -m venv venv

You might need to use 'python3' instead if this doesn't work
3. Activate the virtual environment:

   venv\Scripts\activate

   You should see `(venv)` at the beginning of your command prompt

### 3. Install Required Packages

With your terminal open in VS Code (and virtual environment activated if using one):

pip install -r requirements.txt

(might need to use pip3 instead)

This will install all required packages:
- Flask (web framework)
- OpenCV-Python (image processing)
- czifile (CZI file handling)
- scipy (scientific computing)
- Pillow (image processing)
- numpy (numerical operations)

### 4. Configure VS Code Python Interpreter

1. Press `Ctrl+Shift+P` to open Command Palette
2. Type "Python: Select Interpreter"
3. Choose the interpreter from your virtual environment:
   - If using venv: `.\venv\Scripts\python.exe`
   - If using system Python: Select your main Python installation

### 5. Run the Flask Server

1. Make sure your virtual environment is activated (if using one)
2. In the terminal, run:

   python app.py
 


### 6. Access the Application

Once the server is running, you should see output like:
```
 * Running on http://127.0.0.1:8080
 * Debug mode: on
```

Open your web browser and navigate to:
- `http://localhost:8080` or
- `http://127.0.0.1:8080`


## Troubleshooting

### Common Issues and Solutions

**1. "python is not recognized as an internal or external command"**
- Python is not in your PATH. Reinstall Python and check "Add Python to PATH"

**2. "No module named 'flask'"**
- Run `pip install -r requirements.txt` again
- Make sure you're using the correct Python interpreter in VS Code

**3. "Permission denied" errors**
- Run VS Code as Administrator
- Check that your antivirus isn't blocking the files

**4. Virtual environment activation fails**
- Make sure you're in the project directory
- Try using PowerShell instead of Command Prompt
- For PowerShell, you might need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**5. Port 8080 already in use**
- Change the port in `app.py`: `app.run(debug=True, port=8081)`
- Or find and stop the process using port 8080

**6. OpenCV installation issues**
- Try: `pip install opencv-python-headless` instead
- Or install Microsoft Visual C++ Redistributable

### VS Code Specific Tips

1. **Auto-restart on changes**: The Flask server runs in debug mode, so it will automatically restart when you make changes to Python files.

2. **Debugging**: You can set breakpoints in VS Code by clicking in the left margin of your code.

3. **Terminal management**: You can have multiple terminals open in VS Code (Terminal → New Terminal).

4. **Extensions**: Consider installing these helpful extensions:
   - Python Docstring Generator
   - HTML CSS Support
   - Live Server (for static file development)

