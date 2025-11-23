"""Agent 3: Quality Checker - Compiles LaTeX and manages retry loop."""

from pathlib import Path
from typing import Tuple, Optional
import time

from config import MAX_RETRIES, RETRY_DELAY
from utils.latex_compiler import LaTeXCompiler
from agents.agent2_coder import LaTeXCoder


class QualityChecker:
    """
    Agent 3: The Quality Checker
    - Compiles LaTeX code to PDF
    - Checks for errors
    - Manages retry loop with Agent 2
    - Returns final PDF or error report
    """

    def __init__(self):
        self.compiler = LaTeXCompiler()
        self.coder = LaTeXCoder()

    def check_and_compile(
        self,
        latex_code: str,
        output_path: Path,
        max_retries: int = MAX_RETRIES
    ) -> Tuple[bool, Optional[str]]:
        """
        Attempt to compile LaTeX with automatic retry loop.

        This is the core "Quality Checker" logic:
        1. Try to compile LaTeX to PDF
        2. If it fails, send error back to Agent 2
        3. Agent 2 fixes the code
        4. Retry compilation (up to max_retries times)

        Args:
            latex_code: The LaTeX code to compile
            output_path: Where to save the final PDF
            max_retries: Maximum number of retry attempts

        Returns:
            Tuple of (success: bool, message: str)
        """
        print("🤖 Agent 3 (Quality Checker): Starting compilation check...")

        current_latex = latex_code
        attempt = 0

        while attempt <= max_retries:
            attempt += 1

            if attempt > 1:
                print(f"🔄 Retry attempt {attempt - 1}/{max_retries}...")
                time.sleep(RETRY_DELAY)

            # Quick validation before compilation
            is_valid, validation_error = self.compiler.validate_latex(current_latex)
            if not is_valid:
                print(f"⚠️  Pre-compilation validation failed: {validation_error}")

                if attempt <= max_retries:
                    # Send back to Agent 2 for fixing
                    print("📤 Sending validation errors back to Agent 2...")
                    current_latex = self.coder.fix_latex(current_latex, validation_error)
                    continue
                else:
                    return False, f"Validation failed after {max_retries} retries: {validation_error}"

            # Attempt compilation
            print(f"⚙️  Compiling LaTeX (attempt {attempt})...")
            success, error_message = self.compiler.compile_latex(current_latex, output_path)

            if success:
                print(f"✅ Compilation successful on attempt {attempt}!")
                return True, f"PDF generated successfully at {output_path}"
            else:
                print(f"❌ Compilation failed: {error_message}")

                if attempt <= max_retries:
                    # Send error back to Agent 2 for fixing
                    print("📤 Sending compilation errors back to Agent 2...")
                    current_latex = self.coder.fix_latex(current_latex, error_message)
                else:
                    return False, f"Compilation failed after {max_retries} retries. Last error: {error_message}"

        return False, f"Failed after {max_retries} retry attempts"

    def save_latex_source(self, latex_code: str, output_path: Path) -> None:
        """
        Save the LaTeX source code for debugging.

        Args:
            latex_code: The LaTeX code
            output_path: Where to save the .tex file
        """
        output_path.write_text(latex_code, encoding='utf-8')
        print(f"💾 LaTeX source saved to {output_path}")


if __name__ == "__main__":
    # Test the Quality Checker
    sample_latex = r"""
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section{Test Solutions}

\textbf{Question 1:} What is $2 + 2$?

\textbf{Answer:} 4

\textbf{Explanation:} Basic arithmetic.

\end{document}
"""

    checker = QualityChecker()
    output_pdf = Path("test_output.pdf")

    success, message = checker.check_and_compile(sample_latex, output_pdf)

    print("\n" + "="*50)
    print("RESULT:")
    print("="*50)
    print(f"Success: {success}")
    print(f"Message: {message}")

    if output_pdf.exists():
        print(f"PDF created: {output_pdf}")
