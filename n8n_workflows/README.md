# n8n Workflows

This folder contains n8n workflow configurations for the Image to LaTeX Pipeline.

## 📁 Contents

- `image_to_latex_workflow.json` - Main n8n workflow
- `api_wrapper_workflow.json` - API endpoint wrapper for n8n
- `batch_processing_workflow.json` - Batch image processing workflow

## 🚀 How to Use

### Import to n8n

1. Open your n8n instance
2. Click on **Workflows** → **Import from File**
3. Select the JSON file from this folder
4. Configure your credentials:
   - OpenAI API key
   - File paths
   - Output destinations

### Workflow Overview

#### Main Workflow: `image_to_latex_workflow.json`

```
┌─────────────┐
│ Webhook/    │
│ File Upload │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Save Image  │
│ to Temp     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Execute     │
│ Pipeline    │
│ (Python)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Return PDF  │
│ or Error    │
└─────────────┘
```

## 🔧 Configuration

### Required Environment Variables in n8n

```json
{
  "OPENAI_API_KEY": "your-api-key",
  "PIPELINE_PATH": "/path/to/n8n_img2latex_pipeline",
  "PYTHON_PATH": "/usr/bin/python3"
}
```

### Node Configurations

#### 1. Webhook Node
- **Path**: `/image-to-latex`
- **Method**: `POST`
- **Binary Data**: Enabled
- **Expected Field**: `image`

#### 2. Execute Command Node
```json
{
  "command": "python",
  "arguments": [
    "pipeline.py",
    "--image", "{{ $json.imagePath }}",
    "--output", "{{ $json.outputName }}"
  ],
  "cwd": "/path/to/n8n_img2latex_pipeline"
}
```

#### 3. Respond to Webhook Node
- Success: Return PDF file as binary
- Error: Return error message as JSON

## 📊 Example Request

```bash
curl -X POST http://your-n8n-url/webhook/image-to-latex \
  -F "image=@test.jpg" \
  -F "outputName=my_solution" \
  -o result.pdf
```

## 🔄 Workflow Templates

### Template 1: Simple Upload → Process → Download
Best for: Direct user uploads

### Template 2: Watch Folder → Batch Process
Best for: Automated processing of multiple files

### Template 3: API Endpoint → Database Storage
Best for: Integration with other systems

## 📝 Notes

- Make sure Python environment has all dependencies installed
- LaTeX must be installed on the n8n server
- Set appropriate timeouts (processing can take 30-60 seconds)
- Configure error notifications

## 🐛 Troubleshooting

### "Python command not found"
Set absolute path to Python in Execute Command node

### "Pipeline not found"
Check the working directory in Execute Command node

### "OpenAI API error"
Verify API key is set correctly in environment

## 🔗 Related Documentation

- [Main README](../README.md)
- [USAGE Guide](../USAGE.md)
- [ARCHITECTURE](../ARCHITECTURE.md)
