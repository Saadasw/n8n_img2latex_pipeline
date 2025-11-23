"""
Main Pipeline Orchestrator

This is the factory line that coordinates all three agents:
1. Smart Reader → 2. LaTeX Coder → 3. Quality Checker (with retry loop)
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from agents.agent1_smart_reader import SmartReader
from agents.agent2_coder import LaTeXCoder
from agents.agent3_quality_checker import QualityChecker
from config import OUTPUT_DIR, TEMP_DIR


console = Console()


class ImageToLaTeXPipeline:
    """
    The main pipeline orchestrator.

    Flow:
    Image → Agent 1 (Smart Reader) → Agent 2 (LaTeX Coder) → Agent 3 (Quality Checker) → PDF
                                                                     ↑                ↓
                                                                     └─── (retry) ────┘
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.smart_reader = SmartReader()
        self.latex_coder = LaTeXCoder()
        self.quality_checker = QualityChecker()

    def run(self, image_path: Path, output_name: Optional[str] = None) -> Path:
        """
        Run the complete pipeline.

        Args:
            image_path: Path to the input test image
            output_name: Optional custom name for output files

        Returns:
            Path to the generated PDF

        Raises:
            Exception if pipeline fails
        """
        console.print(Panel.fit(
            "🏭 [bold cyan]Image to LaTeX Pipeline[/bold cyan]\n"
            "Three-Agent Factory Line: Smart Reader → Coder → Quality Checker",
            border_style="cyan"
        ))

        # Validate input
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Generate output filename
        if output_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"test_solution_{timestamp}"

        output_pdf = OUTPUT_DIR / f"{output_name}.pdf"
        output_tex = TEMP_DIR / f"{output_name}.tex"

        try:
            # ===== AGENT 1: Smart Reader =====
            console.print("\n[bold green]━━━ Step 1: Smart Reader ━━━[/bold green]")
            console.print("📖 Reading image, understanding questions, solving test...")

            analysis_result = self.smart_reader.analyze_image(image_path)

            if self.debug:
                debug_file = TEMP_DIR / f"{output_name}_analysis.json"
                debug_file.write_text(
                    json.dumps(analysis_result, indent=2, ensure_ascii=False),
                    encoding='utf-8'
                )
                console.print(f"[dim]Debug: Analysis saved to {debug_file}[/dim]")

            total_questions = analysis_result.get('metadata', {}).get('total_questions', 0)
            console.print(f"✅ [green]Found and solved {total_questions} questions[/green]")

            # ===== AGENT 2: LaTeX Coder =====
            console.print("\n[bold blue]━━━ Step 2: LaTeX Coder ━━━[/bold blue]")
            console.print("💻 Formatting into professional LaTeX code...")

            latex_code = self.latex_coder.generate_latex(analysis_result)

            # Save LaTeX source for debugging
            self.quality_checker.save_latex_source(latex_code, output_tex)
            console.print(f"✅ [blue]LaTeX code generated ({len(latex_code)} chars)[/blue]")

            # ===== AGENT 3: Quality Checker (with retry loop) =====
            console.print("\n[bold magenta]━━━ Step 3: Quality Checker ━━━[/bold magenta]")
            console.print("✅ Compiling to PDF (with automatic error fixing)...")

            success, message = self.quality_checker.check_and_compile(
                latex_code,
                output_pdf
            )

            if success:
                console.print(Panel.fit(
                    f"[bold green]✅ SUCCESS![/bold green]\n\n"
                    f"📄 PDF: {output_pdf}\n"
                    f"📝 LaTeX: {output_tex}\n\n"
                    f"{message}",
                    border_style="green",
                    title="Pipeline Complete"
                ))
                return output_pdf
            else:
                console.print(Panel.fit(
                    f"[bold red]❌ FAILED[/bold red]\n\n"
                    f"{message}\n\n"
                    f"LaTeX source saved at: {output_tex}\n"
                    f"You can try to compile it manually or check for errors.",
                    border_style="red",
                    title="Pipeline Failed"
                ))
                raise Exception(f"Pipeline failed: {message}")

        except Exception as e:
            console.print(f"\n[bold red]❌ Pipeline error: {str(e)}[/bold red]")
            raise


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Image to LaTeX Test Pipeline - Convert test images to professional PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pipeline.py --image test_image.jpg
  python pipeline.py --image my_test.png --output my_solution
  python pipeline.py --image test.jpg --debug

The pipeline will:
  1. Read and solve the test (Agent 1: Smart Reader)
  2. Format into LaTeX (Agent 2: LaTeX Coder)
  3. Compile to PDF with auto-fixing (Agent 3: Quality Checker)
        """
    )

    parser.add_argument(
        "--image",
        type=Path,
        required=True,
        help="Path to the test image (JPG, PNG, etc.)"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output filename (without extension). Default: auto-generated with timestamp"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode (saves intermediate files)"
    )

    args = parser.parse_args()

    # Run pipeline
    pipeline = ImageToLaTeXPipeline(debug=args.debug)

    try:
        result_pdf = pipeline.run(args.image, args.output)
        console.print(f"\n[bold green]🎉 Done! Your PDF is ready: {result_pdf}[/bold green]")
        return 0
    except Exception as e:
        console.print(f"\n[bold red]💥 Error: {e}[/bold red]")
        return 1


if __name__ == "__main__":
    exit(main())
