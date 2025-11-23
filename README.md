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
├── n8n_workflows/                 # n8n workflow configurations
│   ├── README.md                  # n8n setup guide
│   └── image_to_latex_workflow.json
├── test_images/                   # Sample test images for testing
│   └── README.md                  # Image guidelines
├── latex_samples/                 # Sample LaTeX outputs
│   ├── README.md                  # How to test on Overleaf
│   ├── sample_basic_math.tex      # Basic math examples
│   ├── sample_advanced_math.tex   # Advanced topics
│   ├── sample_two_column.tex      # Two-column layout
│   ├── sample_mcq_format.tex      # MCQ format
│   └── sample_bengali_mixed.tex   # Bengali-English mixed
├── examples/
│   ├── demo.py                    # Demo scripts
│   └── README.md
├── output/                        # Generated PDFs
├── temp/                          # Temporary files
├── pipeline.py                    # Main orchestrator
├── config.py                      # Configuration
├── requirements.txt               # Dependencies
├── README.md                      # This file
├── INSTALL.md                     # Installation guide
├── USAGE.md                       # Usage documentation
├── ARCHITECTURE.md                # Technical design
└── TEST_REPORT.md                 # Test results
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

## 📦 Additional Resources

### 🔗 n8n Workflows
Pre-configured n8n workflows for easy integration:
- **[n8n_workflows/](n8n_workflows/)** - Ready-to-import workflow files
- Webhook-based image processing
- Batch processing workflows
- See [n8n_workflows/README.md](n8n_workflows/README.md) for setup

### 🖼️ Test Images
Sample test images for testing the pipeline:
- **[test_images/](test_images/)** - Folder for your test images
- Guidelines for image quality
- See [test_images/README.md](test_images/README.md) for tips

### 📝 LaTeX Samples
Ready-to-test LaTeX code for Overleaf:
- **[latex_samples/](latex_samples/)** - Copy-paste ready LaTeX files
- `sample_basic_math.tex` - Basic math examples
- `sample_advanced_math.tex` - Complex formulas
- `sample_two_column.tex` - Two-column layout
- `sample_mcq_format.tex` - Multiple choice format
- `sample_bengali_mixed.tex` - Bengali-English mixed

**To test on Overleaf:**
1. Go to [Overleaf](https://www.overleaf.com)
2. Create new project
3. Copy content from any `.tex` file in `latex_samples/`
4. Paste and compile!

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

### Core Documentation
- **[README.md](README.md)** - This file, project overview
- **[INSTALL.md](INSTALL.md)** - Detailed installation instructions
- **[USAGE.md](USAGE.md)** - Complete usage guide with examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and technical details
- **[TEST_REPORT.md](TEST_REPORT.md)** - Test results and coverage

### Resource Folders
- **[n8n_workflows/](n8n_workflows/)** - n8n workflow configurations and setup
- **[test_images/](test_images/)** - Test image folder with guidelines
- **[latex_samples/](latex_samples/)** - Sample LaTeX files for Overleaf testing
- **[examples/](examples/)** - Demo scripts and examples

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.
