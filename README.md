# Image to LaTeX Test Pipeline 🏭

A three-agent AI pipeline that converts test images (with Bengali/English text and math formulas) into professionally formatted LaTeX PDFs.

## 🎯 How It Works

Think of this pipeline as a factory line with three robot workers passing jobs to each other:

### 1. **Agent 1: The Smart Reader** 📖
- Reads Bengali and English text from the image
- Understands mathematical formulas
- Solves test questions
- Provides explanations for answers

### 2. **Agent 2: The Coder** 💻
- Takes output from the Smart Reader
- Formats everything into professional LaTeX code
- Organizes content into columns
- Creates beautiful, structured documents

### 3. **Agent 3: The Quality Checker** ✅
- Compiles LaTeX to PDF
- **If successful**: Provides download link
- **If error**: Sends error message back to Agent 2
- **Retry loop**: Agent 2 fixes code and resubmits (up to 3 attempts)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python pipeline.py --image path/to/test_image.jpg
```

## 📋 Requirements

- Python 3.8+
- OpenAI API key (for vision and text processing)
- LaTeX distribution (TexLive or MiKTeX)
- Required Python packages (see requirements.txt)

## 🏗️ Architecture

```
Image Upload
    ↓
[Agent 1: Smart Reader]
    ↓ (Text + Solutions)
[Agent 2: LaTeX Coder]
    ↓ (LaTeX Code)
[Agent 3: Quality Checker]
    ↓
  PDF Compile?
    ├─ ✅ Success → Download PDF
    └─ ❌ Error → Send back to Agent 2 (max 3 retries)
```

## 📁 Project Structure

```
.
├── agents/
│   ├── agent1_smart_reader.py    # OCR + Test solving
│   ├── agent2_coder.py            # LaTeX formatting
│   └── agent3_quality_checker.py  # PDF compilation + retry
├── utils/
│   ├── image_processor.py         # Image preprocessing
│   └── latex_compiler.py          # LaTeX utilities
├── examples/
│   └── sample_test.jpg            # Example test image
├── output/                        # Generated PDFs
├── pipeline.py                    # Main orchestrator
├── config.py                      # Configuration
└── requirements.txt               # Dependencies
```

## 🔧 Configuration

Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key-here
MAX_RETRIES=3
```

## 📝 Example Output

Input: Image of a Bengali/English math test
Output: Professional LaTeX PDF with:
- Formatted questions
- Solved answers
- Step-by-step explanations
- Multi-column layout

## 🛠️ Development

```bash
# Run tests
python -m pytest tests/

# Debug mode
python pipeline.py --image test.jpg --debug
```

## 🧪 Testing

The pipeline has been tested for:
- ✅ Module imports and syntax
- ✅ CLI interface
- ✅ LaTeX validation logic
- ✅ Image preprocessing
- ⏸️ Full pipeline (requires OpenAI API key + LaTeX installation)

**See [TEST_REPORT.md](TEST_REPORT.md) for detailed test results and coverage.**

To test yourself:
```bash
# Quick test (no external dependencies)
python -c "from pipeline import ImageToLaTeXPipeline; print('✅ OK')"

# Full test (requires API key + LaTeX)
python pipeline.py --image examples/test.jpg --debug
```

## 📚 Documentation

- **[README.md](README.md)** - This file, project overview
- **[INSTALL.md](INSTALL.md)** - Detailed installation instructions
- **[USAGE.md](USAGE.md)** - Complete usage guide with examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and technical details
- **[TEST_REPORT.md](TEST_REPORT.md)** - Test results and coverage

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.
