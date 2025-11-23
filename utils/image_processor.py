"""Image preprocessing utilities."""

import base64
from pathlib import Path
from typing import Union
from PIL import Image
import io


class ImageProcessor:
    """Handles image preprocessing and encoding."""

    @staticmethod
    def load_image(image_path: Union[str, Path]) -> Image.Image:
        """Load an image from path."""
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        img = Image.open(image_path)
        return img

    @staticmethod
    def encode_image_to_base64(image_path: Union[str, Path]) -> str:
        """Encode image to base64 string for API calls."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @staticmethod
    def preprocess_image(img: Image.Image, max_size: int = 2048) -> Image.Image:
        """
        Preprocess image for better OCR results.
        - Resize if too large
        - Convert to RGB if needed
        """
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Resize if too large
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        return img

    @staticmethod
    def save_image(img: Image.Image, output_path: Union[str, Path]) -> None:
        """Save image to disk."""
        img.save(output_path)

    @staticmethod
    def get_image_data_url(image_path: Union[str, Path]) -> str:
        """Get data URL for image (for OpenAI Vision API)."""
        image_path = Path(image_path)
        base64_image = ImageProcessor.encode_image_to_base64(image_path)

        # Determine image type from extension
        ext = image_path.suffix.lower()
        mime_type = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }.get(ext, 'image/jpeg')

        return f"data:{mime_type};base64,{base64_image}"
