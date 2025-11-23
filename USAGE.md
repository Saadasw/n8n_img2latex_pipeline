# Usage Guide

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd n8n_img2latex_pipeline

# Install dependencies
pip install -r requirements.txt

# Install LaTeX (if not already installed)
# On Ubuntu/Debian:
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra

# On macOS:
brew install --cask mactex

# On Windows:
# Download and install MiKTeX from https://miktex.org/download
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# You can get one from: https://platform.openai.com/api-keys
```

### 3. Run the Pipeline

```bash
# Basic usage
python pipeline.py --image path/to/your/test_image.jpg

# With custom output name
python pipeline.py --image test.jpg --output my_solution

# With debug mode (saves intermediate files)
python pipeline.py --image test.jpg --debug
```

## 📖 How It Works

### The Three-Agent Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR TEST IMAGE                       │
│        (Bengali/English text + Math formulas)            │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   AGENT 1: Smart Reader │
         │  📖 Reads & Solves Test │
         └────────────┬───────────┘
                      │ (Questions + Solutions)
                      ▼
         ┌────────────────────────┐
         │  AGENT 2: LaTeX Coder   │
         │  💻 Formats to LaTeX    │
         └────────────┬───────────┘
                      │ (LaTeX Code)
                      ▼
         ┌────────────────────────┐
         │ AGENT 3: Quality Checker│
         │  ✅ Compiles to PDF     │
         └────────────┬───────────┘
                      │
              ┌───────┴────────┐
              │                │
            ✅ OK            ❌ ERROR
              │                │
         ┌────▼───┐       ┌────▼─────┐
         │  PDF   │       │ Fix Code │
         │Download│       │ (retry)  │
         └────────┘       └────┬─────┘
                               │
                               └──────┐
                                      │
                            (up to 3 retries)
```

### Agent Details

#### 🤖 Agent 1: Smart Reader
**What it does:**
- Uses OpenAI's Vision API (GPT-4o) to analyze the image
- Reads Bengali and English text
- Understands mathematical formulas
- Solves each question
- Provides explanations

**Input:** Image file
**Output:** Structured JSON with questions, answers, and explanations

#### 💻 Agent 2: LaTeX Coder
**What it does:**
- Takes structured data from Agent 1
- Generates professional LaTeX code
- Creates multi-column layouts
- Formats mathematical notation properly
- Ensures document is compilable

**Input:** JSON from Agent 1
**Output:** Complete LaTeX document

#### ✅ Agent 3: Quality Checker
**What it does:**
- Validates LaTeX code
- Compiles to PDF using pdflatex
- If compilation fails:
  1. Extracts error message
  2. Sends back to Agent 2 for fixing
  3. Retries compilation (up to 3 times)
- Returns final PDF or error report

**Input:** LaTeX code from Agent 2
**Output:** PDF file or error message

## 📁 Output Files

After running the pipeline, you'll find:

```
output/
├── test_solution_20241123_143022.pdf    # Your final PDF!

temp/
├── test_solution_20241123_143022.tex    # LaTeX source
└── test_solution_20241123_143022_analysis.json  # (if --debug)
```

## 🔧 Advanced Usage

### Testing Individual Agents

You can test each agent independently:

```bash
# Test Agent 1 (Smart Reader)
python agents/agent1_smart_reader.py path/to/image.jpg

# Test Agent 2 (LaTeX Coder)
python agents/agent2_coder.py

# Test Agent 3 (Quality Checker)
python agents/agent3_quality_checker.py
```

### Customizing Retry Behavior

Edit `.env`:
```bash
MAX_RETRIES=5  # Increase retry attempts
RETRY_DELAY=3  # Wait 3 seconds between retries
```

### Debug Mode

Enable debug mode to see intermediate outputs:
```bash
python pipeline.py --image test.jpg --debug
```

This saves:
- Analysis JSON from Agent 1
- LaTeX source from Agent 2
- Compilation logs from Agent 3

## 🐛 Troubleshooting

### "LaTeX compiler not found"
Install TeX Live or MiKTeX (see Installation section)

### "OPENAI_API_KEY not found"
Make sure you've created `.env` file with your API key

### PDF compilation fails repeatedly
- Check the LaTeX source in `temp/` folder
- Try compiling manually: `pdflatex temp/your_file.tex`
- Look for specific errors in the output

### Image not being read correctly
- Ensure image is clear and readable
- Supported formats: JPG, PNG, WEBP
- Image should not be too large (will be resized to 2048px max)

## 💡 Tips for Best Results

1. **Image Quality**: Use clear, high-resolution images
2. **Lighting**: Ensure good lighting and contrast
3. **Orientation**: Keep text horizontal
4. **Language**: Clearly mention if using Bengali or mixed languages
5. **Math Formulas**: Write them clearly and use standard notation

## 📊 Example Workflows

### Workflow 1: Single Test
```bash
python pipeline.py --image my_test.jpg
# Wait for processing...
# Open output/test_solution_*.pdf
```

### Workflow 2: Batch Processing
```bash
for img in tests/*.jpg; do
    python pipeline.py --image "$img"
done
```

### Workflow 3: Custom Processing with Debug
```bash
python pipeline.py --image complex_test.jpg --output final_exam --debug
# Review temp/final_exam_analysis.json
# Review temp/final_exam.tex
# Get output/final_exam.pdf
```

## 🤝 Integration

### Using as a Module

```python
from pipeline import ImageToLaTeXPipeline
from pathlib import Path

# Create pipeline
pipeline = ImageToLaTeXPipeline(debug=True)

# Process image
result_pdf = pipeline.run(
    image_path=Path("test.jpg"),
    output_name="my_solution"
)

print(f"PDF created: {result_pdf}")
```

### API Wrapper (Future)

Coming soon: REST API wrapper for easy integration with n8n workflows.

## 📞 Support

For issues and questions:
- Check the [README.md](README.md)
- Review error messages in debug mode
- Check LaTeX source files for compilation errors
