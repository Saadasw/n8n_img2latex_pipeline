# Architecture Documentation

## 🏗️ System Overview

The Image to LaTeX Pipeline is a multi-agent system designed with the **Factory Pattern** approach, where each agent has a specific responsibility and passes work to the next agent in the chain.

## 🎯 Design Principles

1. **Separation of Concerns**: Each agent handles one specific task
2. **Retry Logic**: Automatic error correction loop between Agent 2 and 3
3. **Modularity**: Agents can be tested and modified independently
4. **Observability**: Rich logging and debug modes for transparency
5. **Fault Tolerance**: Graceful error handling with user-friendly messages

## 📊 System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                               │
│                      (Test Image File)                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────────┐
        │         Pipeline Orchestrator             │
        │      (pipeline.py)                       │
        └──────────────────┬───────────────────────┘
                           │
        ┌──────────────────┴───────────────────────┐
        │                                          │
        ▼                                          ▼
┌──────────────┐                         ┌──────────────┐
│   Utils      │                         │   Config     │
│              │                         │              │
│ • Image      │                         │ • API Keys   │
│   Processor  │                         │ • Settings   │
│ • LaTeX      │                         │ • Prompts    │
│   Compiler   │                         │              │
└──────────────┘                         └──────────────┘
        │
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│                    AGENT CHAIN                          │
│                                                         │
│  ┌───────────┐      ┌───────────┐      ┌───────────┐  │
│  │ AGENT 1   │─────▶│ AGENT 2   │─────▶│ AGENT 3   │  │
│  │           │      │           │      │           │  │
│  │ Smart     │      │ LaTeX     │      │ Quality   │  │
│  │ Reader    │      │ Coder     │      │ Checker   │  │
│  │           │      │           │      │           │  │
│  │ 📖 Vision │      │ 💻 Format │      │ ✅ Compile│  │
│  │   + OCR   │      │   + Style │      │   + Retry │  │
│  └───────────┘      └─────┬─────┘      └─────┬─────┘  │
│                           │                   │        │
│                           │    ┌──────────────┘        │
│                           │    │ (on error)            │
│                           │    │                       │
│                           └────┘                       │
│                        Retry Loop                      │
│                      (Max 3 attempts)                  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │  OUTPUT FILES   │
                  │                │
                  │  • PDF         │
                  │  • LaTeX (.tex)│
                  │  • Debug JSON  │
                  └────────────────┘
```

## 🤖 Agent Details

### Agent 1: Smart Reader (`agent1_smart_reader.py`)

**Purpose**: Understand the test image and solve the questions

**Technology Stack**:
- OpenAI Vision API (GPT-4o)
- PIL for image handling
- Base64 encoding for API transmission

**Input**:
- Image file (JPG, PNG, etc.)

**Processing**:
1. Load and preprocess image
2. Encode to base64
3. Send to GPT-4o with vision capabilities
4. Parse mathematical formulas
5. Solve questions
6. Extract explanations

**Output**:
```json
{
  "questions": [
    {
      "number": 1,
      "text": "Question text",
      "type": "multiple_choice",
      "options": ["A", "B", "C", "D"]
    }
  ],
  "solutions": [
    {
      "question_number": 1,
      "answer": "B",
      "explanation": "Brief explanation",
      "work_shown": "Step-by-step solution"
    }
  ],
  "metadata": {
    "total_questions": 5,
    "languages_detected": ["English", "Bengali"],
    "difficulty": "medium"
  }
}
```

**Error Handling**:
- Image not found: FileNotFoundError
- API errors: Logged and re-raised
- JSON parsing errors: Fallback to raw text

---

### Agent 2: LaTeX Coder (`agent2_coder.py`)

**Purpose**: Convert structured data into professional LaTeX code

**Technology Stack**:
- OpenAI GPT-4o for intelligent formatting
- LaTeX templating

**Input**:
- Structured JSON from Agent 1
- (Optional) Error feedback from Agent 3

**Processing**:
1. Receive structured test data
2. Generate LaTeX with:
   - Document class and packages
   - Multi-column layout
   - Mathematical notation
   - Proper formatting
   - Bengali font support (if needed)
3. If error feedback received:
   - Parse error message
   - Identify specific issues
   - Generate corrected code

**Output**:
```latex
\documentclass[12pt]{article}
\usepackage{amsmath}
\usepackage{multicol}
\begin{document}
% ... formatted content ...
\end{document}
```

**Key Features**:
- Intelligent formatting based on content type
- Automatic package inclusion
- Error correction capabilities
- Syntax validation

**Error Handling**:
- API errors: Logged and re-raised
- Markdown cleanup (removes ```latex blocks)
- Ensures complete document structure

---

### Agent 3: Quality Checker (`agent3_quality_checker.py`)

**Purpose**: Compile LaTeX to PDF with automatic error correction

**Technology Stack**:
- LaTeXCompiler utility
- Subprocess for pdflatex
- Error parsing from LaTeX logs

**Input**:
- LaTeX code from Agent 2

**Processing Flow**:
```
1. Receive LaTeX code
2. Quick validation:
   - Check for \documentclass
   - Check for \begin{document}
   - Check balanced braces
   - Check balanced environments
3. If validation fails:
   - Send errors to Agent 2
   - Receive fixed code
   - Retry (up to MAX_RETRIES)
4. Attempt compilation:
   - Run pdflatex
   - Check for PDF output
5. If compilation fails:
   - Parse error logs
   - Extract meaningful errors
   - Send to Agent 2
   - Retry (up to MAX_RETRIES)
6. If successful:
   - Return PDF path
7. If all retries exhausted:
   - Return error report
```

**Output**:
- Success: Path to PDF file
- Failure: Detailed error message

**Retry Logic**:
```python
attempt = 0
while attempt <= MAX_RETRIES:
    if validate(latex_code):
        success, error = compile(latex_code)
        if success:
            return pdf_path
        else:
            latex_code = agent2.fix(latex_code, error)
    attempt += 1
return failure_message
```

**Error Types Handled**:
- Missing braces
- Undefined commands
- Package errors
- Syntax errors
- Environment mismatches

---

## 🔧 Utility Modules

### Image Processor (`utils/image_processor.py`)

**Responsibilities**:
- Load images from disk
- Preprocess (resize, convert)
- Encode to base64
- Generate data URLs

**Key Methods**:
- `load_image(path)`: Load PIL Image
- `encode_image_to_base64(path)`: Base64 encoding
- `preprocess_image(img)`: Resize and convert
- `get_image_data_url(path)`: Create data URL

### LaTeX Compiler (`utils/latex_compiler.py`)

**Responsibilities**:
- Compile LaTeX to PDF
- Parse error logs
- Validate LaTeX syntax
- Generate templates

**Key Methods**:
- `compile_latex(code, output)`: Main compilation
- `parse_latex_errors(log)`: Extract errors
- `validate_latex(code)`: Quick validation
- `create_minimal_latex_template()`: Template generator

---

## 📝 Configuration (`config.py`)

**Environment Variables**:
```python
OPENAI_API_KEY       # Required: OpenAI API access
MAX_RETRIES          # Default: 3
RETRY_DELAY          # Default: 2 seconds
LOG_LEVEL            # Default: INFO
DEBUG_MODE           # Default: false
```

**Model Selection**:
- Vision tasks: `gpt-4o`
- Text tasks: `gpt-4o`

**Paths**:
- `OUTPUT_DIR`: Final PDFs
- `TEMP_DIR`: Intermediate files
- `EXAMPLES_DIR`: Sample images

**System Prompts**:
Each agent has a specialized system prompt defining:
- Role and responsibilities
- Output format requirements
- Quality standards

---

## 🔄 Data Flow

### Complete Pipeline Flow

```
1. User provides image
   └─> pipeline.py receives image path

2. Image → Agent 1 (Smart Reader)
   ├─> Load image
   ├─> Encode to base64
   ├─> Call OpenAI Vision API
   ├─> Parse response
   └─> Return structured JSON

3. JSON → Agent 2 (LaTeX Coder)
   ├─> Analyze content structure
   ├─> Generate LaTeX code
   ├─> Format with proper packages
   └─> Return complete LaTeX document

4. LaTeX → Agent 3 (Quality Checker)
   ├─> Quick validation
   ├─> Attempt compilation
   ├─> Check for PDF output
   └─> If failed:
       ├─> Parse errors
       ├─> Send back to Agent 2
       ├─> Agent 2 fixes code
       ├─> Return to step 4
       └─> (Repeat up to MAX_RETRIES)

5. Success: Return PDF path
   Failure: Return error report
```

### Error Recovery Flow

```
Agent 3 detects error
    │
    ├─> Parse error log
    │   ├─> Extract line numbers
    │   ├─> Identify error type
    │   └─> Format error message
    │
    └─> Send to Agent 2
        │
        ├─> Agent 2 analyzes error
        ├─> Identifies fix needed
        ├─> Generates corrected code
        └─> Returns to Agent 3
            │
            └─> Retry compilation
```

---

## 🎨 Design Patterns Used

### 1. **Chain of Responsibility**
- Each agent handles specific responsibility
- Passes result to next agent
- Clear handoff points

### 2. **Retry Pattern**
- Automatic retry with exponential backoff
- Maximum retry limit
- Error feedback loop

### 3. **Factory Pattern**
- Pipeline orchestrator creates agents
- Centralized configuration
- Consistent initialization

### 4. **Strategy Pattern**
- Different processing strategies per agent
- Pluggable error handling
- Configurable retry logic

---

## 🔒 Security Considerations

1. **API Key Management**
   - Environment variables only
   - Never committed to version control
   - .env.example for template

2. **Input Validation**
   - File existence checks
   - Image format validation
   - Path sanitization

3. **Resource Limits**
   - Compilation timeout (30s)
   - Maximum retries (3)
   - Image size limits (2048px)

4. **Error Information**
   - No sensitive data in logs
   - Sanitized error messages
   - Debug mode optional

---

## 🚀 Performance Optimization

1. **Caching**
   - Could add: Image preprocessing cache
   - Could add: LaTeX template cache

2. **Parallel Processing**
   - Current: Sequential agents
   - Potential: Batch image processing

3. **Resource Management**
   - Temporary file cleanup
   - Memory-efficient image handling
   - Stream-based PDF generation

---

## 🧪 Testing Strategy

### Unit Tests (Future)
```
tests/
├── test_agent1.py       # Smart Reader tests
├── test_agent2.py       # LaTeX Coder tests
├── test_agent3.py       # Quality Checker tests
├── test_image_processor.py
└── test_latex_compiler.py
```

### Integration Tests (Future)
- Full pipeline with sample images
- Error recovery scenarios
- Edge cases

### Manual Testing
- Use `examples/demo.py`
- Individual agent testing scripts
- Debug mode for inspection

---

## 📈 Monitoring & Observability

**Current Logging**:
- Rich console output
- Step-by-step progress
- Error messages with context

**Future Enhancements**:
- Metrics collection (processing time, success rate)
- Error rate tracking
- Performance profiling

---

## 🔮 Future Enhancements

1. **n8n Integration**
   - REST API wrapper
   - Webhook support
   - Status callbacks

2. **Advanced Features**
   - Multiple image support
   - PDF input (convert to images)
   - Custom LaTeX templates
   - Batch processing API

3. **Performance**
   - Caching layer
   - Async processing
   - Queue system

4. **Quality**
   - Confidence scores
   - Manual review flags
   - Quality metrics

---

## 📚 Dependencies

**Core**:
- `openai`: AI capabilities
- `Pillow`: Image processing
- `python-dotenv`: Configuration

**LaTeX**:
- External: TexLive or MiKTeX
- Python: subprocess for compilation

**UI**:
- `rich`: Beautiful console output
- `tenacity`: Retry logic

**Utilities**:
- `pydantic`: Data validation
- `requests`: HTTP requests

---

## 🏁 Conclusion

This architecture provides:
- ✅ Modular, maintainable code
- ✅ Clear separation of concerns
- ✅ Robust error handling
- ✅ User-friendly interface
- ✅ Extensible design
- ✅ Production-ready foundation

The three-agent design makes it easy to:
- Test components independently
- Replace or upgrade individual agents
- Add new features without breaking existing functionality
- Scale horizontally if needed
