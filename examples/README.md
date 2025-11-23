# Examples

This directory contains example images and demo scripts.

## Demo Script

Run the demo to see the pipeline in action:

```bash
python examples/demo.py
```

## Sample Images

Add your test images here:
- `sample_test.jpg` - Your sample test image
- `bengali_test.jpg` - Example with Bengali text
- `math_test.png` - Example with complex math

## Creating Test Images

You can:
1. Take a photo of a real test paper
2. Create a digital test document and screenshot it
3. Use existing test PDFs and convert to images

### Tips for Best Quality:
- Use good lighting
- Keep the camera steady
- Ensure text is readable
- Crop to just the test content
- Use PNG or high-quality JPG

## Running Examples

```bash
# Process a single image
python pipeline.py --image examples/sample_test.jpg

# Run demo script with all examples
python examples/demo.py
```
