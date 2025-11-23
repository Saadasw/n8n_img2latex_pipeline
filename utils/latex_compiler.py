"""LaTeX compilation utilities."""

import subprocess
import tempfile
import re
from pathlib import Path
from typing import Tuple, Optional
import shutil

from config import LATEX_COMPILER, LATEX_TIMEOUT


class LaTeXCompiler:
    """Handles LaTeX compilation and error parsing."""

    @staticmethod
    def compile_latex(latex_code: str, output_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Compile LaTeX code to PDF.

        Args:
            latex_code: The LaTeX source code
            output_path: Where to save the PDF

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        # Create temporary directory for compilation
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            tex_file = temp_dir / "document.tex"

            # Write LaTeX code to temp file
            tex_file.write_text(latex_code, encoding='utf-8')

            try:
                # Run pdflatex
                result = subprocess.run(
                    [LATEX_COMPILER, "-interaction=nonstopmode", "document.tex"],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=LATEX_TIMEOUT
                )

                # Check if PDF was created
                pdf_file = temp_dir / "document.pdf"
                if pdf_file.exists():
                    # Copy PDF to output location
                    shutil.copy2(pdf_file, output_path)
                    return True, None
                else:
                    # Parse error from log
                    log_file = temp_dir / "document.log"
                    if log_file.exists():
                        error_msg = LaTeXCompiler.parse_latex_errors(log_file.read_text())
                    else:
                        error_msg = result.stderr or "Unknown compilation error"
                    return False, error_msg

            except subprocess.TimeoutExpired:
                return False, f"LaTeX compilation timed out after {LATEX_TIMEOUT} seconds"
            except FileNotFoundError:
                return False, f"LaTeX compiler '{LATEX_COMPILER}' not found. Please install TeX Live or MiKTeX."
            except Exception as e:
                return False, f"Compilation error: {str(e)}"

    @staticmethod
    def parse_latex_errors(log_content: str) -> str:
        """
        Parse LaTeX log file to extract meaningful error messages.

        Args:
            log_content: Content of the .log file

        Returns:
            Formatted error message
        """
        errors = []

        # Common error patterns
        error_patterns = [
            r"! (.+)",  # Error messages starting with !
            r"l\.(\d+) (.+)",  # Line number and context
            r"Missing (.+)",  # Missing characters/braces
            r"Undefined control sequence",
            r"LaTeX Error: (.+)",
        ]

        lines = log_content.split('\n')
        for i, line in enumerate(lines):
            for pattern in error_patterns:
                match = re.search(pattern, line)
                if match:
                    # Get context (few lines before and after)
                    context_start = max(0, i - 2)
                    context_end = min(len(lines), i + 3)
                    context = '\n'.join(lines[context_start:context_end])
                    errors.append(context)
                    break

        if errors:
            return "\n\n".join(errors[:5])  # Return first 5 errors
        else:
            # If no specific errors found, look for the first ! in log
            for line in lines:
                if line.startswith('!'):
                    return line
            return "Compilation failed but no specific error found in log"

    @staticmethod
    def validate_latex(latex_code: str) -> Tuple[bool, Optional[str]]:
        """
        Quick validation of LaTeX code without full compilation.

        Args:
            latex_code: The LaTeX source code

        Returns:
            Tuple of (is_valid: bool, error_message: Optional[str])
        """
        errors = []

        # Check for basic structure
        if r'\documentclass' not in latex_code:
            errors.append("Missing \\documentclass declaration")

        if r'\begin{document}' not in latex_code:
            errors.append("Missing \\begin{document}")

        if r'\end{document}' not in latex_code:
            errors.append("Missing \\end{document}")

        # Check for balanced braces (simple check)
        if latex_code.count('{') != latex_code.count('}'):
            errors.append(f"Unbalanced braces: {latex_code.count('{')} opening, {latex_code.count('}')} closing")

        # Check for balanced begin/end
        begins = re.findall(r'\\begin\{([^}]+)\}', latex_code)
        ends = re.findall(r'\\end\{([^}]+)\}', latex_code)

        if len(begins) != len(ends):
            errors.append(f"Unbalanced environments: {len(begins)} \\begin, {len(ends)} \\end")

        if errors:
            return False, "\n".join(errors)
        return True, None

    @staticmethod
    def create_minimal_latex_template() -> str:
        """Create a minimal LaTeX template."""
        return r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{geometry}
\geometry{a4paper, margin=1in}

\begin{document}

% Content goes here

\end{document}
"""
