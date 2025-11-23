# n8n Workflows for Image to LaTeX Pipeline

Pre-built n8n workflows for automating the Image to LaTeX Pipeline.

## 📦 Available Workflows

### 1. **Complete Workflow** (`complete_workflow.json`) ⭐ Recommended
Single image processing via webhook with full error handling.

**Features:**
- ✅ Webhook endpoint for image upload
- ✅ Automatic temp file cleanup
- ✅ PDF generation and download
- ✅ Error handling with retry logic
- ✅ Processing time tracking

**Use Case:** Web apps, manual uploads, API integration

**Endpoint:** `POST /webhook/image-to-latex`

**Quick Test:**
```bash
curl -X POST http://localhost:5678/webhook/image-to-latex \
  -F "image=@test.jpg" \
  -o result.pdf
```

---

### 2. **Batch Processing Workflow** (`batch_processing_workflow.json`)
Automated folder watching and batch processing.

**Features:**
- ✅ Watches folder for new images
- ✅ Processes multiple images automatically
- ✅ Moves files to processed/ or failed/
- ✅ CSV logging of all operations
- ✅ Email summary reports (optional)

**Use Case:** Bulk processing, scheduled tasks, automation

**Setup:**
```bash
mkdir -p /watch/images /processed /failed
# Drop images into /watch/images/
```

---

### 3. **REST API Wrapper** (`api_wrapper_workflow.json`)
Production-ready REST API with authentication.

**Features:**
- ✅ API key authentication
- ✅ Returns PDF or LaTeX source
- ✅ Request validation
- ✅ Debug mode support
- ✅ Processing time metrics

**Use Case:** Service integration, programmatic access

**Endpoint:** `POST /webhook/api/v1/convert`

**Quick Test:**
```bash
curl -X POST http://localhost:5678/webhook/api/v1/convert \
  -H "X-API-Key: your-secret-key" \
  -F "image=@test.jpg" \
  -F "format=pdf" \
  -o result.pdf
```

---

## 🚀 Quick Start

### 1. Import Workflow

1. Open n8n
2. **Workflows** → **Import from File**
3. Select a JSON file from this folder
4. Click **Import**

### 2. Configure Paths

Update these in the workflow:

```javascript
// In "Prepare Paths" or similar node:
const pipelinePath = '/path/to/n8n_img2latex_pipeline'; // ← Change this
```

### 3. Set Environment Variables

In n8n **Settings** → **Environments**:

```bash
OPENAI_API_KEY=your-api-key-here
PIPELINE_PATH=/home/user/n8n_img2latex_pipeline
PYTHON_PATH=/usr/bin/python3
```

### 4. Test!

Click **Execute Workflow** and upload a test image.

---

## 📚 Documentation

### 📖 [**SETUP_GUIDE.md**](SETUP_GUIDE.md) - Complete Setup Guide
Detailed instructions for:
- Step-by-step setup
- Configuration options
- Testing procedures
- Troubleshooting
- Production deployment
- Security best practices

**👉 Start here if this is your first time!**

---

## 🎯 Which Workflow Should I Use?

| Scenario | Recommended Workflow |
|----------|---------------------|
| **Web application** with user uploads | Complete Workflow |
| **API integration** with other services | REST API Wrapper |
| **Bulk processing** of many images | Batch Processing |
| **Manual testing** and development | Complete Workflow |
| **Scheduled automation** | Batch Processing |
| **Production service** with auth | REST API Wrapper |

---

## 📊 Workflow Comparison

| Feature | Complete | Batch | API Wrapper |
|---------|----------|-------|-------------|
| Webhook trigger | ✅ | ❌ | ✅ |
| Folder watching | ❌ | ✅ | ❌ |
| API authentication | ❌ | ❌ | ✅ |
| Multiple images | ❌ | ✅ | ❌ |
| Email notifications | ❌ | ✅ | ❌ |
| Logging to CSV | ❌ | ✅ | ❌ |
| Processing metrics | ✅ | ✅ | ✅ |
| Error handling | ✅ | ✅ | ✅ |
| Cleanup | ✅ | ✅ | ✅ |

---

## 🔧 Prerequisites

### Required:
- ✅ n8n installed and running
- ✅ Python 3.8+ with pipeline installed
- ✅ LaTeX distribution (TexLive/MiKTeX)
- ✅ OpenAI API key

### Optional:
- Email server (for batch notifications)
- Redis (for production queue management)
- PostgreSQL (for n8n persistence)

---

## 🏗️ Architecture

### Complete Workflow Flow
```
┌─────────────┐
│ Upload      │
│ Image       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Save to     │
│ Temp        │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Execute     │
│ Pipeline    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Success?    │
└──────┬──────┘
       │
   ┌───┴───┐
   ▼       ▼
  YES      NO
   │       │
   ▼       ▼
┌─────┐ ┌─────┐
│ PDF │ │Error│
└─────┘ └─────┘
```

### Batch Processing Flow
```
┌─────────────┐
│ Watch       │
│ Folder      │ (every minute)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ For Each    │
│ Image       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Process     │
└──────┬──────┘
       │
   ┌───┴───┐
   ▼       ▼
Success   Fail
   │       │
   ▼       ▼
┌────┐  ┌────┐
│Log │  │Log │
└────┘  └────┘
   │       │
   └───┬───┘
       ▼
┌─────────────┐
│ Email       │
│ Summary     │
└─────────────┘
```

### API Wrapper Flow
```
┌─────────────┐
│ API         │
│ Request     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validate    │
│ API Key     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Execute     │
│ Pipeline    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Return      │
│ PDF or TEX  │
└─────────────┘
```

---

## 🔐 Security Notes

### API Key Protection

**DON'T:**
```javascript
const apiKey = 'sk-1234567890'; // ❌ Hardcoded
```

**DO:**
```javascript
const apiKey = $env.OPENAI_API_KEY; // ✅ Environment variable
```

### Webhook Security

For production:
1. **Enable authentication** on webhook nodes
2. **Use HTTPS** only
3. **Implement rate limiting**
4. **Validate input** thoroughly
5. **Set file size limits**

### File Permissions

Ensure proper permissions:
```bash
chmod 750 /path/to/n8n_img2latex_pipeline
chmod 644 /path/to/n8n_img2latex_pipeline/*.py
```

---

## 🧪 Testing

### Test Each Workflow

**1. Complete Workflow:**
```bash
curl -X POST http://localhost:5678/webhook/image-to-latex \
  -F "image=@../test_images/sample.jpg" \
  -o test_output.pdf
```

**2. Batch Processing:**
```bash
cp ../test_images/*.jpg /watch/images/
# Wait 1 minute, check /processed/ folder
```

**3. API Wrapper:**
```bash
curl -X POST http://localhost:5678/webhook/api/v1/convert \
  -H "X-API-Key: test-key" \
  -F "image=@../test_images/sample.jpg" \
  -F "format=pdf" \
  -o api_test.pdf
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** "Workflow not found"
```
Solution: Check you imported the JSON correctly
```

**Issue:** "Python not found"
```
Solution: Use full path to Python
/usr/bin/python3 instead of python3
```

**Issue:** "Pipeline fails"
```
Solution: Test pipeline manually first:
cd /path/to/pipeline && python3 pipeline.py --image test.jpg
```

**Issue:** "Webhook unreachable"
```
Solution: Check n8n is running and firewall settings
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting.

---

## 📝 Customization

### Modify Timeout

In "Execute Pipeline" node:
```json
{
  "timeout": 180000  // 3 minutes in milliseconds
}
```

### Add Custom Headers

In "Return PDF" node:
```json
{
  "responseHeaders": {
    "entries": [
      { "name": "X-Custom-Header", "value": "custom-value" }
    ]
  }
}
```

### Change Webhook Path

In "Webhook" node:
```json
{
  "path": "my-custom-endpoint"  // Changes URL
}
```

---

## 📊 Monitoring

### View Executions

In n8n:
1. Go to **Executions**
2. Filter by workflow name
3. Click execution to see details

### Check Logs

```bash
# Pipeline logs
tail -f /path/to/pipeline/temp/*.log

# n8n logs
docker logs -f n8n  # if using Docker
```

### Metrics to Track

- **Success rate**: % of successful conversions
- **Processing time**: Average time per image
- **Error types**: Common failure reasons
- **API usage**: OpenAI API calls/cost

---

## 💡 Pro Tips

### Tip 1: Start Simple
Begin with **complete_workflow.json** for testing, then move to others.

### Tip 2: Use Environment Variables
Store all configuration in n8n environment variables.

### Tip 3: Test Locally First
Always test the pipeline manually before using in n8n.

### Tip 4: Monitor Costs
Track OpenAI API usage to avoid unexpected bills.

### Tip 5: Set Up Notifications
Configure error notifications to catch issues quickly.

---

## 🔗 Related Documentation

- **[Main README](../README.md)** - Project overview
- **[Setup Guide](SETUP_GUIDE.md)** - Detailed n8n setup
- **[Usage Guide](../USAGE.md)** - Pipeline usage
- **[Architecture](../ARCHITECTURE.md)** - Technical design

---

## 📞 Support

**Issues with n8n?** Check [n8n docs](https://docs.n8n.io)
**Issues with pipeline?** Check [main README](../README.md)
**Setup questions?** See [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## 🎯 Quick Reference

### Import Steps
1. n8n → Workflows → Import from File
2. Select JSON file
3. Update paths in "Prepare Paths" node
4. Set environment variables
5. Test with sample image

### Required Env Vars
```bash
OPENAI_API_KEY=sk-...
PIPELINE_PATH=/path/to/pipeline
```

### Test Command
```bash
curl -X POST http://localhost:5678/webhook/YOUR-ENDPOINT \
  -F "image=@test.jpg" \
  -o result.pdf
```

---

**Ready to get started?** Import a workflow and follow the [SETUP_GUIDE.md](SETUP_GUIDE.md)! 🚀
