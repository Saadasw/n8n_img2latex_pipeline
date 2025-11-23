"""Configuration for the Image to LaTeX Pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Model Configuration
VISION_MODEL = "gpt-4o"  # For image analysis
TEXT_MODEL = "gpt-4o"  # For LaTeX generation and fixing

# Pipeline Configuration
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = 2  # seconds between retries

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"
EXAMPLES_DIR = BASE_DIR / "examples"

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
EXAMPLES_DIR.mkdir(exist_ok=True)

# LaTeX Configuration
LATEX_COMPILER = "pdflatex"
LATEX_TIMEOUT = 30  # seconds

# Agent Configuration
AGENT_1_SYSTEM_PROMPT = """You are a Smart Reader AI. Your job is to:
1. Read and understand Bengali and English text from images
2. Identify and parse mathematical formulas
3. Solve test questions accurately
4. Provide clear, concise explanations for your answers

Output format should be structured JSON with:
- questions: list of questions found
- answers: your solutions
- explanations: brief explanations for each answer
"""

AGENT_2_SYSTEM_PROMPT = """You are a LaTeX Coding Expert. Your job is to:
1. Take structured content (questions, answers, explanations)
2. Format it into professional LaTeX code
3. Use multi-column layouts for better presentation
4. Ensure proper mathematical notation using LaTeX math mode
5. Make the document beautiful and well-organized

IMPORTANT:
- Generate COMPLETE, compilable LaTeX documents
- Include all necessary packages
- Use proper Bengali font support if needed
- Ensure all braces, environments are properly closed
"""

AGENT_3_SYSTEM_PROMPT = """You are a Quality Checker. Your job is to:
1. Compile LaTeX code to PDF
2. Identify compilation errors
3. Extract specific error messages with line numbers
4. Provide clear feedback for fixes

If compilation fails, return detailed error information.
"""

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
