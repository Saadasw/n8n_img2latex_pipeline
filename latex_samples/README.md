# LaTeX Samples

This folder contains sample LaTeX files that demonstrate the output format of the pipeline.

## 📄 Files

1. **sample_basic_math.tex** - Simple math test with solutions
2. **sample_advanced_math.tex** - Advanced math with complex formulas
3. **sample_bengali_mixed.tex** - Bengali + English mixed content
4. **sample_mcq_format.tex** - Multiple choice questions layout
5. **sample_two_column.tex** - Two-column layout example

## 🧪 How to Test on Overleaf

### Quick Test
1. Go to [Overleaf](https://www.overleaf.com)
2. Create a new blank project
3. Copy the content from any `.tex` file here
4. Paste into Overleaf's main.tex
5. Click "Recompile"
6. View the PDF output

### Step-by-Step
1. Open Overleaf: https://www.overleaf.com
2. Click **New Project** → **Blank Project**
3. Give it a name (e.g., "Test LaTeX Pipeline")
4. Delete the default content in `main.tex`
5. Copy content from one of these sample files
6. Paste into the editor
7. The PDF will compile automatically

## 📚 Sample Files Overview

### 1. sample_basic_math.tex
**What it shows:**
- Basic document structure
- Math equations
- Question/answer format
- Simple formatting

**Good for:** Testing basic compilation

---

### 2. sample_advanced_math.tex
**What it shows:**
- Complex mathematical notation
- Multiple equation environments
- Advanced LaTeX packages
- Professional formatting

**Good for:** Testing advanced features

---

### 3. sample_bengali_mixed.tex
**What it shows:**
- Bengali font support
- Mixed language content
- UTF-8 encoding
- Language switching

**Good for:** Testing multilingual support

---

### 4. sample_mcq_format.tex
**What it shows:**
- Multiple choice layout
- Enumeration
- Answer key section
- Explanation formatting

**Good for:** Testing MCQ format

---

### 5. sample_two_column.tex
**What it shows:**
- Two-column layout
- Space efficiency
- Professional appearance
- Page organization

**Good for:** Testing layout options

## 🎯 What to Check

When testing on Overleaf:

✅ **Compilation**: Does it compile without errors?
✅ **Math Formulas**: Are equations rendering correctly?
✅ **Formatting**: Does it look professional?
✅ **Layout**: Is the spacing and alignment good?
✅ **Fonts**: Are all characters displaying?

## 🐛 Common Issues on Overleaf

### Issue: "Missing package"
**Solution:** Overleaf has most packages. If missing, add:
```latex
\usepackage{package-name}
```

### Issue: "Font not found"
**Solution:** For Bengali, Overleaf uses XeLaTeX compiler:
1. Click **Menu** (top left)
2. Change **Compiler** to **XeLaTeX**
3. Recompile

### Issue: "Unicode character error"
**Solution:** Ensure UTF-8 encoding:
```latex
\usepackage[utf8]{inputenc}
```

## 📝 Modifying Samples

Feel free to modify these samples:
- Change questions
- Add more content
- Adjust formatting
- Test different layouts

## 🔗 Resources

- **Overleaf**: https://www.overleaf.com
- **LaTeX Documentation**: https://www.latex-project.org/help/documentation/
- **Math Symbols**: https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols
- **Package Documentation**: https://www.ctan.org/

## 💡 Tips

1. **Start Simple**: Test `sample_basic_math.tex` first
2. **Check Errors**: Look at the error log if compilation fails
3. **Iterate**: Make small changes and recompile
4. **Save**: Download working PDFs for reference

## 🎨 Customization Ideas

Try customizing:
- Colors (use `xcolor` package)
- Page size (A4, Letter)
- Margins (use `geometry` package)
- Font sizes
- Header/footer (use `fancyhdr` package)
