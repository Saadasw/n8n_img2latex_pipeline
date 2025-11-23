"""Agent 2: LaTeX Coder - Formats content into professional LaTeX."""

import json
from typing import Dict, Any, Optional
from openai import OpenAI

from config import OPENAI_API_KEY, TEXT_MODEL, AGENT_2_SYSTEM_PROMPT


class LaTeXCoder:
    """
    Agent 2: The LaTeX Coder
    - Takes structured content from Agent 1
    - Formats it into professional LaTeX code
    - Creates beautiful, multi-column layouts
    - Ensures proper mathematical notation
    """

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_latex(self, analysis_data: Dict[str, Any], error_feedback: Optional[str] = None) -> str:
        """
        Generate LaTeX code from the analyzed test data.

        Args:
            analysis_data: Structured data from Agent 1
            error_feedback: If provided, this is a retry with error feedback from Agent 3

        Returns:
            Complete LaTeX document as string
        """
        if error_feedback:
            print(f"🔧 Agent 2 (Coder): Fixing LaTeX based on error feedback...")
        else:
            print("🤖 Agent 2 (Coder): Generating LaTeX code...")

        # Prepare the prompt
        user_prompt = f"""
        Generate a professional LaTeX document from this test analysis data:

        {json.dumps(analysis_data, indent=2, ensure_ascii=False)}

        Requirements:
        1. Create a COMPLETE, COMPILABLE LaTeX document
        2. Use multi-column layout (2 columns) for better presentation
        3. Include all necessary packages (amsmath, amssymb, multicol, etc.)
        4. For Bengali text, use appropriate font packages (if detected)
        5. Format mathematical formulas properly using LaTeX math mode
        6. Create sections for:
           - Questions (with numbering)
           - Solutions (with answers and explanations)
        7. Make it visually appealing with proper spacing and formatting
        8. Ensure ALL braces, environments, and brackets are properly closed
        9. Include a title like "Test Solutions" or similar

        CRITICAL:
        - Return ONLY the LaTeX code, no explanations
        - The code must be ready to compile with pdflatex
        - Double-check all closing braces and environments
        """

        # Add error feedback if this is a retry
        if error_feedback:
            user_prompt += f"""

        IMPORTANT - PREVIOUS ATTEMPT FAILED:
        The previous LaTeX code had these errors:
        {error_feedback}

        Please fix these specific errors and regenerate the complete document.
        Pay special attention to:
        - Missing or extra braces
        - Unclosed environments
        - Undefined commands
        - Package conflicts
        """

        try:
            response = self.client.chat.completions.create(
                model=TEXT_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": AGENT_2_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                max_tokens=4096,
                temperature=0.3  # Slightly higher for creative formatting
            )

            latex_code = response.choices[0].message.content

            # Clean up the response (remove markdown code blocks if present)
            if "```latex" in latex_code:
                latex_start = latex_code.find("```latex") + 8
                latex_end = latex_code.find("```", latex_start)
                latex_code = latex_code[latex_start:latex_end].strip()
            elif "```" in latex_code:
                latex_start = latex_code.find("```") + 3
                latex_end = latex_code.find("```", latex_start)
                latex_code = latex_code[latex_start:latex_end].strip()

            print(f"✅ Generated LaTeX code ({len(latex_code)} characters)")
            return latex_code

        except Exception as e:
            print(f"❌ Error in Agent 2: {str(e)}")
            raise

    def fix_latex(self, original_latex: str, error_message: str) -> str:
        """
        Fix LaTeX code based on compilation error.

        Args:
            original_latex: The LaTeX code that failed
            error_message: Error message from compiler

        Returns:
            Fixed LaTeX code
        """
        print("🔧 Agent 2 (Coder): Fixing LaTeX errors...")

        user_prompt = f"""
        The following LaTeX code failed to compile with this error:

        ERROR:
        {error_message}

        ORIGINAL CODE:
        {original_latex}

        Please fix the error and return the complete, corrected LaTeX code.

        CRITICAL:
        - Return ONLY the fixed LaTeX code, no explanations
        - Make minimal changes to fix the specific error
        - Ensure the code will compile successfully
        - Double-check all braces and environments are balanced
        """

        try:
            response = self.client.chat.completions.create(
                model=TEXT_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": AGENT_2_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                max_tokens=4096,
                temperature=0.2  # Lower temperature for precise fixes
            )

            fixed_latex = response.choices[0].message.content

            # Clean up the response
            if "```latex" in fixed_latex:
                latex_start = fixed_latex.find("```latex") + 8
                latex_end = fixed_latex.find("```", latex_start)
                fixed_latex = fixed_latex[latex_start:latex_end].strip()
            elif "```" in fixed_latex:
                latex_start = fixed_latex.find("```") + 3
                latex_end = fixed_latex.find("```", latex_start)
                fixed_latex = fixed_latex[latex_start:latex_end].strip()

            print(f"✅ Fixed LaTeX code ({len(fixed_latex)} characters)")
            return fixed_latex

        except Exception as e:
            print(f"❌ Error in Agent 2 fix: {str(e)}")
            raise


if __name__ == "__main__":
    # Test the LaTeX Coder
    sample_data = {
        "questions": [
            {
                "number": 1,
                "text": "What is 2 + 2?",
                "type": "open_ended"
            },
            {
                "number": 2,
                "text": "Solve: $x^2 - 5x + 6 = 0$",
                "type": "open_ended"
            }
        ],
        "solutions": [
            {
                "question_number": 1,
                "answer": "4",
                "explanation": "Basic arithmetic: 2 + 2 = 4"
            },
            {
                "question_number": 2,
                "answer": "x = 2 or x = 3",
                "explanation": "Factoring: (x-2)(x-3) = 0",
                "work_shown": "x^2 - 5x + 6 = (x-2)(x-3) = 0, so x = 2 or x = 3"
            }
        ],
        "metadata": {
            "total_questions": 2,
            "languages_detected": ["English"]
        }
    }

    coder = LaTeXCoder()
    latex_code = coder.generate_latex(sample_data)

    print("\n" + "="*50)
    print("GENERATED LATEX:")
    print("="*50)
    print(latex_code)
