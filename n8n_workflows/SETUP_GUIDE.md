# n8n Workflows - Complete Setup Guide

This guide will help you set up the Image to LaTeX Pipeline in n8n.

## 📋 Available Workflows

We provide 3 ready-to-use n8n workflows:

### 1. **complete_workflow.json** - Single Image Processing
**Use case:** Process one image at a time via webhook
**Best for:** Web applications, manual uploads, API integration

### 2. **batch_processing_workflow.json** - Automated Batch Processing
**Use case:** Watch a folder and automatically process all images
**Best for:** Bulk processing, automated workflows, scheduled tasks

### 3. **api_wrapper_workflow.json** - REST API
**Use case:** Expose the pipeline as a REST API endpoint
**Best for:** Integration with other services, programmatic access

---

## 🚀 Quick Start

### Step 1: Import Workflow to n8n

1. Open your n8n instance
2. Click **Workflows** in the left sidebar
3. Click **Import from File** (top right)
4. Select one of the JSON files from this folder
5. Click **Import**

### Step 2: Configure Paths

After importing, you'll need to update these paths in the workflow:

1. **Pipeline Path**: `/path/to/n8n_img2latex_pipeline`
   - Find in node: "Prepare Paths" or similar
   - Replace with your actual installation path

2. **Python Path**: `python3` or `/usr/bin/python3`
   - Find in node: "Execute Pipeline"
   - Use `which python3` to find your path

3. **Output Directory**: Check config.py for output paths

### Step 3: Set Environment Variables

In n8n, go to **Settings** → **Environments** and add:

```bash
OPENAI_API_KEY=your-actual-api-key-here
PIPELINE_PATH=/home/user/n8n_img2latex_pipeline
PYTHON_PATH=/usr/bin/python3
```

### Step 4: Test the Workflow

1. Click **Execute Workflow** (or the play button)
2. Upload a test image
3. Wait for processing
4. Check the output!

---

## 📝 Detailed Workflow Guides

### Workflow 1: Complete Workflow (Single Image)

**File:** `complete_workflow.json`

#### What it does:
```
User uploads image → Webhook receives it → Save to temp →
Execute pipeline → Check if successful →
If success: Return PDF → If fail: Return error
```

#### Configuration:

**1. Webhook Node:**
- **Path:** `/image-to-latex` (customize if needed)
- **Method:** POST
- **Authentication:** None (add if needed)
- **Binary Data:** Enabled

**2. Prepare Paths Node (Code):**
```javascript
// Update this path:
const pipelinePath = '/path/to/n8n_img2latex_pipeline';
```

**3. Execute Pipeline Node:**
```bash
# Update command:
cd /YOUR/PATH && python3 pipeline.py --image {{ $json.imagePath }} --output {{ $json.outputName }}
```

#### Testing:
```bash
curl -X POST http://your-n8n-url/webhook/image-to-latex \
  -F "image=@test.jpg" \
  -o result.pdf
```

---

### Workflow 2: Batch Processing

**File:** `batch_processing_workflow.json`

#### What it does:
```
Watch folder → Detect new images → Process each one →
Move to processed/ or failed/ → Log results → Send summary email
```

#### Configuration:

**1. Watch Folder Node:**
- **Path:** `/watch/images` (folder to watch)
- **Poll Interval:** Every minute (adjust as needed)
- **File Pattern:** `*.jpg,*.png` (image types)

**2. Folder Structure:**
Create these folders:
```bash
mkdir -p /watch/images
mkdir -p /processed
mkdir -p /failed
```

**3. Email Notification Node:**
- **Disabled by default** (remove "disabled: true" to enable)
- Configure SMTP settings
- Set recipient email

#### Workflow Steps:

1. **Watch Folder** - Monitors `/watch/images` for new files
2. **Read Images** - Loads image files
3. **Prepare Each Image** - Creates processing parameters
4. **Process Image** - Runs pipeline on each image
5. **Check Result** - Validates output
6. **Success or Fail?** - Splits based on result
7. **Move to Processed** - Moves successful images
8. **Move to Failed** - Moves failed images
9. **Log Success/Error** - Records results to CSV
10. **Summarize Batch** - Creates summary report
11. **Send Email** - Notifies administrator (optional)

#### Usage:
```bash
# Drop images into watch folder
cp test1.jpg test2.jpg test3.jpg /watch/images/

# Wait for processing (checks every minute)
# Results appear in /processed or /failed
# Check logs: batch_processing_log.csv and batch_processing_errors.csv
```

---

### Workflow 3: REST API Wrapper

**File:** `api_wrapper_workflow.json`

#### What it does:
```
API request → Validate API key → Save image →
Execute pipeline → Return PDF or LaTeX code
```

#### Configuration:

**1. API Security:**
```javascript
// In "Validate Request" node, update:
const validApiKey = 'your-secret-api-key';
```

**Production Security:**
- Use environment variables for API keys
- Add rate limiting
- Use HTTPS only
- Implement IP whitelisting if needed

**2. API Endpoint:**
- **URL:** `http://your-n8n-url/webhook/api/v1/convert`
- **Method:** POST
- **Authentication:** API Key in header

#### API Usage:

**Request Format:**
```bash
curl -X POST http://your-n8n-url/webhook/api/v1/convert \
  -H "X-API-Key: your-secret-api-key" \
  -F "image=@test.jpg" \
  -F "format=pdf" \
  -F "outputName=my_solution" \
  -F "debug=false" \
  -o result.pdf
```

**Parameters:**
- `image` (file, required) - The test image
- `format` (string, optional) - "pdf" or "tex" (default: "pdf")
- `outputName` (string, optional) - Custom output name
- `debug` (boolean, optional) - Enable debug mode

**Response Headers:**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="my_solution.pdf"
X-Processing-Time: 12.5s
X-Status: success
```

**Error Response:**
```json
{
  "success": false,
  "error": "Compilation failed",
  "message": "Failed to process image",
  "details": {
    "exitCode": 1,
    "processingTime": "8.3s"
  },
  "timestamp": "2024-11-23T12:00:00.000Z"
}
```

---

## 🔧 Advanced Configuration

### Environment Variables in n8n

Set these in n8n Settings → Environments:

```bash
# Required
OPENAI_API_KEY=sk-...
PIPELINE_PATH=/home/user/n8n_img2latex_pipeline

# Optional
MAX_RETRIES=3
RETRY_DELAY=2
DEBUG_MODE=false
API_KEY=your-secret-api-key
ADMIN_EMAIL=admin@yourdomain.com
```

### Using Environment Variables in Nodes

In Code nodes:
```javascript
const apiKey = $env.OPENAI_API_KEY;
const pipelinePath = $env.PIPELINE_PATH;
```

In Execute Command nodes:
```bash
cd {{ $env.PIPELINE_PATH }} && python3 pipeline.py ...
```

### Timeout Settings

Adjust timeouts based on your needs:
- **Small images:** 60 seconds (60000ms)
- **Medium images:** 120 seconds (120000ms) - default
- **Large/complex images:** 180 seconds (180000ms)

In Execute Command node:
```json
{
  "timeout": 180000
}
```

---

## 🐛 Troubleshooting

### Issue 1: "Python command not found"

**Solution:**
```javascript
// In Execute Pipeline node, use full path:
/usr/bin/python3 pipeline.py ...
```

Find your Python path:
```bash
which python3
# Output: /usr/bin/python3
```

### Issue 2: "Pipeline not found"

**Solution:**
Check the working directory:
```bash
cd {{ $json.pipelinePath }} && pwd && ls -la
```

### Issue 3: "OpenAI API error"

**Solution:**
1. Check if API key is set: `echo $OPENAI_API_KEY`
2. Verify key is valid on OpenAI platform
3. Check API quota/billing

### Issue 4: "Workflow executes but fails"

**Debug steps:**
1. Enable debug mode in the workflow
2. Check n8n execution logs
3. Check pipeline logs in `temp/` folder
4. Run pipeline manually: `python pipeline.py --image test.jpg --debug`

### Issue 5: "Webhook not accessible"

**Solution:**
1. Check n8n is running: `systemctl status n8n`
2. Check firewall: `sudo ufw status`
3. Check nginx/proxy settings
4. Verify webhook URL in n8n

---

## 📊 Monitoring & Logging

### Check Workflow Executions

In n8n:
1. Go to **Executions** in left sidebar
2. Filter by workflow name
3. Click on execution to see details
4. Check each node's output

### Enable Detailed Logging

In pipeline.py, enable debug mode:
```bash
python pipeline.py --image test.jpg --debug
```

Logs will be saved to `temp/` folder.

### Batch Processing Logs

CSV logs are created automatically:
- `batch_processing_log.csv` - Successful processing
- `batch_processing_errors.csv` - Failed processing

Format:
```csv
timestamp,filename,status,pdfPath,error
2024-11-23T12:00:00Z,test1.jpg,completed,/output/test1.pdf,
2024-11-23T12:01:00Z,test2.jpg,failed,,LaTeX compilation error
```

---

## 🔐 Security Best Practices

### 1. API Key Security
```javascript
// DON'T hardcode API keys:
const apiKey = 'sk-1234567890'; // ❌ BAD

// DO use environment variables:
const apiKey = $env.API_KEY; // ✅ GOOD
```

### 2. Webhook Authentication

Add authentication to webhook nodes:
- Basic Auth
- Header Auth (API Key)
- JWT tokens

### 3. File Upload Limits

Limit file sizes:
```javascript
// In validation node:
const maxFileSize = 10 * 1024 * 1024; // 10MB
if (fileSize > maxFileSize) {
  throw new Error('File too large');
}
```

### 4. Rate Limiting

Implement rate limiting for API endpoints:
- Use n8n's built-in rate limiting
- Or add custom rate limiting logic

---

## 🚀 Production Deployment

### Checklist

- [ ] Set all environment variables
- [ ] Configure proper paths
- [ ] Set up authentication
- [ ] Enable HTTPS
- [ ] Configure error notifications
- [ ] Set appropriate timeouts
- [ ] Enable logging
- [ ] Test with sample images
- [ ] Set up monitoring
- [ ] Configure backups

### Recommended Setup

1. **Use Docker** for n8n deployment
2. **Use PostgreSQL** for n8n database (not SQLite)
3. **Use Redis** for queue management
4. **Set up reverse proxy** (nginx) with SSL
5. **Configure auto-restart** (systemd or PM2)
6. **Set up monitoring** (Prometheus/Grafana)

### Docker Compose Example

```yaml
version: '3'
services:
  n8n:
    image: n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=changeme
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PIPELINE_PATH=/data/pipeline
    volumes:
      - ./n8n_data:/home/node/.n8n
      - ./n8n_img2latex_pipeline:/data/pipeline
```

---

## 💡 Tips & Tricks

### Tip 1: Test Locally First

Before using n8n, test the pipeline manually:
```bash
cd /path/to/n8n_img2latex_pipeline
python pipeline.py --image test.jpg --debug
```

### Tip 2: Use Sticky Notes

In n8n workflow editor, use sticky notes to document:
- Configuration requirements
- Important variables
- Troubleshooting tips

### Tip 3: Version Control

Export workflows regularly:
```bash
# Backup your workflows
n8n export:workflow --all --output=./backups/
```

### Tip 4: Parallel Processing

For batch processing, adjust concurrency:
```javascript
// In batch workflow, process multiple images in parallel
// Set in workflow settings
"concurrency": 3  // Process 3 images at once
```

### Tip 5: Error Notifications

Set up Slack/Discord/Email notifications for errors:
- Add notification nodes
- Connect to error outputs
- Configure templates

---

## 📞 Support

### Need Help?

1. Check this guide
2. Review n8n documentation: https://docs.n8n.io
3. Check pipeline documentation: ../README.md
4. Test pipeline manually first
5. Check n8n community forum

### Common Resources

- **n8n Docs:** https://docs.n8n.io
- **n8n Community:** https://community.n8n.io
- **Pipeline Docs:** [../README.md](../README.md)
- **Architecture:** [../ARCHITECTURE.md](../ARCHITECTURE.md)

---

## 🎯 Next Steps

After setup:

1. **Test each workflow** with sample images
2. **Monitor performance** and adjust timeouts
3. **Set up error handling** and notifications
4. **Implement authentication** for production
5. **Enable logging** for debugging
6. **Create backups** of workflows
7. **Document your customizations**

---

**Happy automating!** 🚀
