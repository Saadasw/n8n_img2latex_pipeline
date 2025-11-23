# Test Images

This folder contains sample test images for testing the pipeline.

## 📸 Image Categories

### 1. Math Tests
- `math_test_simple.jpg` - Basic arithmetic and algebra
- `math_test_advanced.jpg` - Calculus and advanced topics
- `math_test_mixed.jpg` - Multiple choice with explanations

### 2. Bengali Tests
- `bengali_test_basic.jpg` - Bengali text with simple math
- `bengali_test_mixed.jpg` - Bengali + English mixed
- `bengali_math_advanced.jpg` - Complex Bengali math problems

### 3. English Tests
- `english_test_mcq.jpg` - Multiple choice questions
- `english_test_essay.jpg` - Essay-type questions
- `english_math_combo.jpg` - English text with math formulas

## 🎯 How to Add Test Images

### Method 1: Take a Photo
1. Use your phone camera
2. Ensure good lighting
3. Keep text horizontal
4. Avoid shadows and glare
5. Save as JPG or PNG

### Method 2: Screenshot
1. Open a test document
2. Take a screenshot
3. Crop to show only the test
4. Save here

### Method 3: Scan
1. Use a scanner or scanning app
2. Save at 300 DPI or higher
3. Export as JPG or PNG

## 📏 Image Requirements

- **Format**: JPG, PNG, WEBP
- **Resolution**: Minimum 800x600, recommended 1920x1080+
- **Size**: Will be auto-resized to max 2048px if larger
- **Clarity**: Text should be clearly readable

## 🧪 Testing Workflow

```bash
# Test with a single image
python pipeline.py --image test_images/math_test_simple.jpg

# Test with debug mode
python pipeline.py --image test_images/bengali_test_basic.jpg --debug

# Test with custom output name
python pipeline.py --image test_images/english_test_mcq.jpg --output my_test
```

## 📊 Sample Test Structure

A good test image should have:
- Clear question numbering (1, 2, 3...)
- Readable text (not blurry)
- Well-formatted math formulas
- Options for MCQs (A, B, C, D)

## 🌟 Example

Here's what a good test image looks like:

```
Question 1: Solve for x: 2x + 5 = 15
A) x = 5
B) x = 10
C) x = 7.5
D) x = 20

Question 2: What is the derivative of x²?
A) 2x
B) x
C) 2
D) x²
```

## 📝 Creating Test Images

If you don't have real test images, you can:

1. **Use LaTeX to create them**:
   - Write test in LaTeX
   - Compile to PDF
   - Screenshot or convert to image

2. **Use Google Docs**:
   - Create test in Google Docs
   - Insert math equations
   - Screenshot

3. **Use Microsoft Word**:
   - Create test with equation editor
   - Export as PDF
   - Convert to image

## 🎨 Tips for Best Results

1. **High Contrast**: Dark text on white background
2. **Good Lighting**: No shadows or glare
3. **Straight Alignment**: Keep paper/screen level
4. **Clear Focus**: No blur or distortion
5. **Full Frame**: Include all questions

## 🚫 What to Avoid

- ❌ Blurry images
- ❌ Dark or poor lighting
- ❌ Rotated text
- ❌ Handwritten text (may not work well)
- ❌ Very small font sizes
- ❌ Low contrast (gray text on white)

## 📂 Folder Organization

```
test_images/
├── math/           # Math-only tests
├── bengali/        # Bengali language tests
├── english/        # English language tests
├── mixed/          # Mixed content tests
└── samples/        # Sample outputs (for reference)
```

## 🔗 Related

- See [USAGE.md](../USAGE.md) for how to process images
- See [examples/](../examples/) for demo scripts
- See [output/](../output/) for generated PDFs
