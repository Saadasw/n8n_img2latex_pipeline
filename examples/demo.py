"""
Demo script showing how to use the pipeline programmatically.
"""

from pathlib import Path
import sys

# Add parent directory to path to import pipeline
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline import ImageToLaTeXPipeline
from rich.console import Console

console = Console()


def demo_basic_usage():
    """Basic usage example."""
    console.print("\n[bold cyan]Demo 1: Basic Usage[/bold cyan]")

    # Initialize pipeline
    pipeline = ImageToLaTeXPipeline(debug=False)

    # Process an image
    image_path = Path("examples/sample_test.jpg")

    if not image_path.exists():
        console.print(f"[yellow]Image not found: {image_path}[/yellow]")
        console.print("[yellow]Please add a test image to examples/sample_test.jpg[/yellow]")
        return

    try:
        result_pdf = pipeline.run(image_path)
        console.print(f"[green]✅ Success! PDF: {result_pdf}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


def demo_custom_output():
    """Demo with custom output name."""
    console.print("\n[bold cyan]Demo 2: Custom Output Name[/bold cyan]")

    pipeline = ImageToLaTeXPipeline(debug=True)

    image_path = Path("examples/sample_test.jpg")

    if not image_path.exists():
        console.print(f"[yellow]Image not found: {image_path}[/yellow]")
        return

    try:
        result_pdf = pipeline.run(
            image_path=image_path,
            output_name="custom_solution"
        )
        console.print(f"[green]✅ PDF saved as: {result_pdf}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


def demo_batch_processing():
    """Demo batch processing multiple images."""
    console.print("\n[bold cyan]Demo 3: Batch Processing[/bold cyan]")

    examples_dir = Path("examples")
    image_files = list(examples_dir.glob("*.jpg")) + list(examples_dir.glob("*.png"))

    if not image_files:
        console.print("[yellow]No images found in examples/ directory[/yellow]")
        return

    pipeline = ImageToLaTeXPipeline(debug=False)

    results = []
    for img_path in image_files:
        console.print(f"\n[cyan]Processing: {img_path.name}[/cyan]")
        try:
            result = pipeline.run(img_path)
            results.append((img_path.name, result, "Success"))
            console.print(f"[green]✅ Done[/green]")
        except Exception as e:
            results.append((img_path.name, None, f"Error: {e}"))
            console.print(f"[red]❌ Failed: {e}[/red]")

    # Summary
    console.print("\n[bold]Summary:[/bold]")
    for img_name, result, status in results:
        console.print(f"  {img_name}: {status}")


def demo_individual_agents():
    """Demo running individual agents."""
    console.print("\n[bold cyan]Demo 4: Individual Agent Testing[/bold cyan]")

    from agents.agent1_smart_reader import SmartReader
    from agents.agent2_coder import LaTeXCoder
    import json

    image_path = Path("examples/sample_test.jpg")
    if not image_path.exists():
        console.print(f"[yellow]Image not found: {image_path}[/yellow]")
        return

    # Test Agent 1
    console.print("\n[yellow]Testing Agent 1 (Smart Reader)...[/yellow]")
    reader = SmartReader()
    try:
        analysis = reader.analyze_image(image_path)
        console.print(f"[green]✅ Found {analysis['metadata']['total_questions']} questions[/green]")

        # Test Agent 2
        console.print("\n[yellow]Testing Agent 2 (LaTeX Coder)...[/yellow]")
        coder = LaTeXCoder()
        latex_code = coder.generate_latex(analysis)
        console.print(f"[green]✅ Generated {len(latex_code)} characters of LaTeX[/green]")

        # Show preview
        console.print("\n[bold]LaTeX Preview (first 500 chars):[/bold]")
        console.print(latex_code[:500] + "...")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


def main():
    """Run all demos."""
    console.print(Panel.fit(
        "[bold magenta]Image to LaTeX Pipeline - Demo Suite[/bold magenta]",
        border_style="magenta"
    ))

    # Uncomment the demos you want to run
    demo_basic_usage()
    # demo_custom_output()
    # demo_batch_processing()
    # demo_individual_agents()

    console.print("\n[bold green]Demo complete![/bold green]")


if __name__ == "__main__":
    from rich.panel import Panel
    main()
