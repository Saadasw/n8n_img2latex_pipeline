# Installation Guide

## Prerequisites

Before installing the Image to LaTeX Pipeline, ensure you have:

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **LaTeX distribution** (TexLive, MiKTeX, or MacTeX)
- **OpenAI API key**

---

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd n8n_img2latex_pipeline
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or if you prefer using a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install LaTeX Distribution

Choose based on your operating system:

#### Ubuntu/Debian Linux

```bash
sudo apt-get update
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

For full TeX Live installation (larger, but more complete):
```bash
sudo apt-get install texlive-full
```

#### macOS

Using Homebrew:
```bash
brew install --cask mactex
```

Or download from [https://tug.org/mactex/](https://tug.org/mactex/)

After installation, update your PATH:
```bash
export PATH="/Library/TeX/texbin:$PATH"
```

#### Windows

**Option 1: MiKTeX** (Recommended for Windows)
1. Download from [https://miktex.org/download](https://miktex.org/download)
2. Run the installer
3. Choose "Install missing packages automatically" during setup

**Option 2: TeX Live**
1. Download from [https://tug.org/texlive/windows.html](https://tug.org/texlive/windows.html)
2. Run the installer
3. Add to PATH if needed

#### Verify LaTeX Installation

```bash
pdflatex --version
```

You should see version information if installed correctly.

### 4. Set Up OpenAI API Key

#### Get Your API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Create a new API key
4. Copy the key (you won't be able to see it again!)

#### Configure Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
MAX_RETRIES=3
```

**Important**: Never commit `.env` to version control!

### 5. Verify Installation

Run a quick test:

```bash
# Check if all imports work
python -c "from pipeline import ImageToLaTeXPipeline; print('✅ Installation successful!')"
```

---

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError"

```bash
# Make sure you installed dependencies
pip install -r requirements.txt

# Check if you're in the right environment
which python
```

#### "LaTeX compiler not found"

```bash
# Check if pdflatex is in PATH
which pdflatex  # Linux/Mac
where pdflatex  # Windows

# If not found, add LaTeX to PATH or reinstall
```

#### "OPENAI_API_KEY not found"

```bash
# Check if .env file exists
ls -la .env

# Verify it contains your key
cat .env

# Make sure python-dotenv is installed
pip install python-dotenv
```

#### Permission Issues (Linux)

```bash
# If you get permission errors
sudo chmod +x pipeline.py

# Or run with python explicitly
python pipeline.py --image test.jpg
```

#### Import Errors

```bash
# If you see "cannot import name X"
# Make sure you're in the project root directory
cd /path/to/n8n_img2latex_pipeline

# Try reinstalling dependencies
pip install --upgrade -r requirements.txt
```

---

## Optional: System-wide Installation

If you want to use the pipeline from anywhere:

```bash
# Install in development mode
pip install -e .
```

Note: You'll need to create a `setup.py` file for this (not included by default).

---

## Updating

To update the pipeline:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt
```

---

## Uninstallation

To completely remove the pipeline:

```bash
# Deactivate virtual environment (if using one)
deactivate

# Remove the directory
cd ..
rm -rf n8n_img2latex_pipeline

# Remove virtual environment (if created outside project)
rm -rf venv
```

---

## Development Setup

For contributors:

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests (once test suite is created)
pytest tests/

# Format code
black .

# Lint code
flake8 .
```

---

## Docker Installation (Future)

Coming soon: Docker container for easy deployment.

```bash
# Future command
docker pull your-registry/img2latex-pipeline
docker run -it -v $(pwd)/input:/input -v $(pwd)/output:/output img2latex-pipeline
```

---

## Next Steps

After installation:

1. Read [USAGE.md](USAGE.md) for usage instructions
2. Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
3. Try the examples: `python examples/demo.py`
4. Process your first image: `python pipeline.py --image examples/sample_test.jpg`

---

## Getting Help

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review error messages carefully
3. Check the [README.md](README.md) for more information
4. Search existing GitHub issues
5. Create a new issue with:
   - Your OS and Python version
   - Full error message
   - Steps to reproduce

---

## Requirements Summary

**Minimum**:
- Python 3.8+
- 500 MB disk space
- Internet connection (for OpenAI API)
- OpenAI API credits

**Recommended**:
- Python 3.10+
- 2 GB disk space (for LaTeX packages)
- Fast internet connection
- OpenAI API Plus account (for higher rate limits)

---

## Platform-Specific Notes

### Linux
- Tested on Ubuntu 20.04, 22.04
- Works on Debian, Fedora, Arch with appropriate package manager

### macOS
- Tested on macOS 12+
- Apple Silicon (M1/M2) fully supported
- Rosetta not required

### Windows
- Tested on Windows 10, 11
- WSL2 supported (recommended for developers)
- PowerShell and CMD both work

---

## Quick Start (TL;DR)

```bash
# 1. Install
git clone <repo-url>
cd n8n_img2latex_pipeline
pip install -r requirements.txt

# 2. Install LaTeX (Ubuntu example)
sudo apt-get install texlive-latex-extra

# 3. Configure
cp .env.example .env
# Edit .env and add your OpenAI API key

# 4. Run
python pipeline.py --image your_test.jpg

# Done! 🎉
```

---

**Congratulations!** You're ready to convert test images to beautiful LaTeX PDFs! 🚀
