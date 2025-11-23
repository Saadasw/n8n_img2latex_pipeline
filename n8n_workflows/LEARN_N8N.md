# Learn n8n Through the Image to LaTeX Pipeline 🎓

A hands-on guide to learning n8n by building real workflows for the Image to LaTeX Pipeline.

## 🎯 What You'll Learn

By the end of this guide, you'll understand:
- ✅ n8n basics: Nodes, connections, and workflows
- ✅ Webhook triggers and HTTP requests
- ✅ Code nodes (JavaScript in workflows)
- ✅ File operations (read, write, delete)
- ✅ Conditional logic (IF nodes)
- ✅ Error handling and debugging
- ✅ Environment variables and security
- ✅ Production deployment

**Best part?** You'll build 3 real, working workflows for the pipeline!

---

## 📚 Table of Contents

1. [n8n Basics](#n8n-basics)
2. [Your First Workflow](#your-first-workflow)
3. [Understanding Nodes](#understanding-nodes)
4. [Building the Complete Workflow](#building-the-complete-workflow)
5. [Advanced Concepts](#advanced-concepts)
6. [Production Tips](#production-tips)

---

## 🚀 n8n Basics

### What is n8n?

n8n is a **workflow automation tool** that connects different services together.

Think of it like **LEGO blocks for automation**:
- Each block (node) does one thing
- You connect blocks to build workflows
- Data flows from one block to the next

### Core Concepts

#### 1. **Workflow**
A series of connected nodes that automate a task.

```
Example: Image Upload → Process → Return PDF
```

#### 2. **Node**
A single step in your workflow.

Types of nodes:
- **Trigger nodes**: Start the workflow (Webhook, Schedule)
- **Action nodes**: Do something (Execute Command, Send Email)
- **Logic nodes**: Make decisions (IF, Switch)

#### 3. **Connection**
The link between nodes that passes data.

```
[Node A] ──data──> [Node B]
```

#### 4. **Execution**
One run of your workflow.

---

## 🎨 Your First Workflow

Let's build a simple "Hello World" workflow!

### Step 1: Create a Workflow

1. Open n8n (usually http://localhost:5678)
2. Click **"New Workflow"** (top right)
3. You'll see an empty canvas

### Step 2: Add a Manual Trigger

1. Click the **+** button
2. Search for "Manual"
3. Click **"Manual Trigger"**
4. This node lets you start the workflow manually

### Step 3: Add a Code Node

1. Click the **+** after Manual Trigger
2. Search for "Code"
3. Click **"Code"**
4. Paste this code:

```javascript
// JavaScript code that runs in n8n
const message = "Hello from n8n!";
const timestamp = new Date().toISOString();

return {
  message,
  timestamp,
  pipeline: "Image to LaTeX"
};
```

### Step 4: Test It!

1. Click **"Execute Workflow"** (top right)
2. You'll see the output in the Code node
3. Congratulations! 🎉

**What just happened?**
- Manual Trigger started the workflow
- Code node created data
- Data is now available for the next node

---

## 🧩 Understanding Nodes

### Trigger Nodes

**Webhook Node** - Our main trigger

```javascript
{
  "httpMethod": "POST",
  "path": "image-to-latex"
}
```

**What it does:**
- Listens for HTTP requests
- Receives uploaded images
- Starts the workflow

**Try it:**
```bash
curl -X POST http://localhost:5678/webhook/image-to-latex \
  -F "image=@test.jpg"
```

---

### Code Nodes

**Most powerful and flexible node!**

#### Basic Code Node

```javascript
// Access input data
const inputData = $input.item.json;

// Create new data
const outputData = {
  myField: "Hello",
  calculated: 1 + 1
};

// Return it
return outputData;
```

#### Accessing Environment Variables

```javascript
const apiKey = $env.OPENAI_API_KEY;
const pipelinePath = $env.PIPELINE_PATH;

return {
  apiKey,
  pipelinePath
};
```

#### Working with Files

```javascript
// Get uploaded file info
const fileName = $input.item.binary.data.fileName;
const fileSize = $input.item.binary.data.fileSize;

// Create paths
const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
const outputPath = `/tmp/${timestamp}_${fileName}`;

return {
  fileName,
  fileSize,
  outputPath
};
```

---

### Execute Command Node

**Run shell commands from n8n**

```json
{
  "command": "python3 /path/to/pipeline.py --image {{ $json.imagePath }}",
  "timeout": 120000
}
```

**Important:**
- Use `{{ }}` to access data from previous nodes
- Timeout in milliseconds (120000 = 2 minutes)
- Returns stdout, stderr, and exit code

---

### IF Node (Conditional Logic)

**Make decisions in your workflow**

```json
{
  "conditions": {
    "boolean": [
      {
        "value1": "={{ $json.success }}",
        "value2": true
      }
    ]
  }
}
```

**Flow:**
```
[IF Node]
   ├─> TRUE path (success = true)
   └─> FALSE path (success = false)
```

---

### File Nodes

#### Read Binary File
```json
{
  "filePath": "={{ $json.pdfPath }}"
}
```

#### Write Binary File
```json
{
  "fileName": "={{ $json.outputName }}.jpg",
  "dataPropertyName": "data"
}
```

#### Delete File
```json
{
  "fileName": "={{ $json.imagePath }}"
}
```

---

## 🏗️ Building the Complete Workflow

Now let's build our actual Image to LaTeX workflow step-by-step!

### Part 1: Webhook Setup

**Goal:** Receive image uploads

```
1. Add Webhook Node
2. Configure:
   - Method: POST
   - Path: image-to-latex
   - Binary Data: ON
```

**Test:**
```bash
curl -X POST http://localhost:5678/webhook-test/image-to-latex \
  -F "image=@test.jpg"
```

### Part 2: Save the Image

**Goal:** Save uploaded image to temp folder

```
1. Add "Write Binary File" node
2. Configure:
   - File Name: {{ $json.timestamp }}_image.jpg
   - Data Property: data
```

**Understanding:**
- Binary data flows from Webhook
- Write node saves it to disk
- Returns file path for next node

### Part 3: Prepare Execution Parameters

**Goal:** Create variables for pipeline execution

```
1. Add "Code" node
2. Name it "Prepare Paths"
3. Paste:
```

```javascript
const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
const filename = $input.item.binary.data?.fileName || 'test_image.jpg';
const outputName = $input.item.json.outputName || `solution_${timestamp}`;

const pipelinePath = $env.PIPELINE_PATH || '/path/to/pipeline';
const imagePath = `/tmp/${timestamp}_${filename}`;
const pdfPath = `${pipelinePath}/output/${outputName}.pdf`;

return {
  timestamp,
  filename,
  outputName,
  pipelinePath,
  imagePath,
  pdfPath
};
```

**What this does:**
- Creates unique timestamp
- Generates output name
- Builds file paths
- Makes data available to next nodes

### Part 4: Execute the Pipeline

**Goal:** Run Python pipeline

```
1. Add "Execute Command" node
2. Configure:
```

```bash
cd {{ $json.pipelinePath }} && python3 pipeline.py --image {{ $json.imagePath }} --output {{ $json.outputName }}
```

**Parameters:**
- Timeout: 180000 (3 minutes)
- Working Directory: {{ $json.pipelinePath }}

**Understanding `{{ }}` syntax:**
- `{{ $json.imagePath }}` - Access data from previous node
- `{{ $env.API_KEY }}` - Access environment variable
- `{{ $now }}` - Current timestamp

### Part 5: Parse the Result

**Goal:** Check if pipeline succeeded

```
1. Add "Code" node
2. Name it "Parse Result"
3. Paste:
```

```javascript
const exitCode = $input.item.json.exitCode || 0;
const stdout = $input.item.json.stdout || '';
const stderr = $input.item.json.stderr || '';

const success = exitCode === 0;
const error = stderr || '';

return {
  ...$input.item.json,  // Keep all previous data
  success,              // Add success flag
  error,                // Add error message
  processingComplete: true
};
```

**Spread operator (`...`):**
- `...$input.item.json` - Copies all existing data
- Then add new fields

### Part 6: Make a Decision

**Goal:** Route based on success/failure

```
1. Add "IF" node
2. Name it "Success?"
3. Configure:
   - Condition: Boolean
   - Value 1: {{ $json.success }}
   - Operation: Equals
   - Value 2: true
```

**Flow:**
```
[Success?]
  ├─> TRUE  → Read PDF
  └─> FALSE → Return Error
```

### Part 7: Handle Success

**Goal:** Read and return the PDF

```
1. Add "Read Binary File" node (on TRUE path)
2. Configure:
   - File Path: {{ $json.pdfPath }}

3. Add "Respond to Webhook" node
4. Configure:
   - Respond With: Binary
   - Headers:
     * Content-Type: application/pdf
     * Content-Disposition: attachment; filename={{ $json.outputName }}.pdf
```

### Part 8: Handle Errors

**Goal:** Return error message

```
1. Add "Respond to Webhook" node (on FALSE path)
2. Configure:
   - Respond With: JSON
   - Response Body:
```

```json
{
  "success": false,
  "error": "{{ $json.error }}",
  "message": "Failed to process image"
}
```

### Part 9: Cleanup

**Goal:** Delete temporary image file

```
1. Add "Delete File" node (after error response)
2. Configure:
   - File Path: {{ $json.imagePath }}
```

---

## 🧪 Testing Your Workflow

### Manual Testing

1. Click **"Execute Workflow"** button
2. Upload a test image
3. Watch each node execute
4. Check the output

### Testing with curl

```bash
# Test the workflow
curl -X POST http://localhost:5678/webhook/image-to-latex \
  -F "image=@test_images/sample.jpg" \
  -F "outputName=my_test" \
  -o result.pdf

# Check if PDF was created
file result.pdf
```

### Debugging Tips

#### View Node Data

1. Click on any executed node
2. Look at the **"Output"** tab
3. See exactly what data it produced

#### Check Logs

1. Go to **"Executions"** in sidebar
2. Click on your execution
3. See full execution history

#### Enable Debug Mode

In Code nodes:
```javascript
console.log('Debug:', $json);  // Logs to n8n output
return $json;
```

---

## 📊 Data Flow Example

Let's trace data through the workflow:

### Node 1: Webhook
```json
{
  "binary": {
    "data": {
      "fileName": "test.jpg",
      "fileSize": 125000
    }
  },
  "json": {
    "outputName": "my_solution"
  }
}
```

### Node 2: Prepare Paths
```json
{
  "timestamp": "2024-11-23T12-00-00",
  "filename": "test.jpg",
  "outputName": "my_solution",
  "imagePath": "/tmp/2024-11-23T12-00-00_test.jpg",
  "pdfPath": "/pipeline/output/my_solution.pdf"
}
```

### Node 3: Execute Command
```json
{
  "exitCode": 0,
  "stdout": "✅ SUCCESS! PDF: output/my_solution.pdf",
  "stderr": "",
  ...previous data...
}
```

### Node 4: Parse Result
```json
{
  "success": true,
  "error": "",
  "processingComplete": true,
  ...previous data...
}
```

**See the pattern?** Each node adds to or transforms the data!

---

## 🎓 Advanced Concepts

### Environment Variables

**Why use them?**
- Keep secrets safe (API keys)
- Easy configuration changes
- Different values for dev/production

**Setting in n8n:**
```bash
# In Settings → Environments
OPENAI_API_KEY=sk-...
PIPELINE_PATH=/home/user/pipeline
DEBUG_MODE=true
```

**Using in workflows:**
```javascript
// In Code nodes
const apiKey = $env.OPENAI_API_KEY;

// In Execute Command nodes
{{ $env.PIPELINE_PATH }}
```

### Error Handling

**Try-Catch in Code Nodes:**

```javascript
try {
  // Your code
  const result = doSomething();
  return { success: true, result };
} catch (error) {
  return {
    success: false,
    error: error.message
  };
}
```

**Workflow Error Handling:**

```
1. Add "Error Trigger" node
2. Connect it to error paths
3. Send notifications or retry
```

### Loops and Iterations

**Processing Multiple Items:**

```javascript
// Set mode to "runOnceForEachItem"
const item = $input.item.json;

// Process each item
const processed = processItem(item);

return processed;
```

**Example: Batch Processing**

```
[Read Files] → [For Each File] → [Process] → [Next File]
```

### Conditional Routing

**Switch Node (multiple conditions):**

```json
{
  "mode": "expression",
  "output": "={{ $json.fileType }}"
}
```

Routes to different paths based on value:
- Output 0: PDF files
- Output 1: Image files
- Output 2: Other files

---

## 🎯 Practice Exercises

### Exercise 1: Add Logging

**Task:** Add a node that logs every execution to a CSV file

**Hint:**
```javascript
// Create log entry
const logEntry = {
  timestamp: new Date().toISOString(),
  filename: $json.filename,
  success: $json.success
};

// Append to CSV (use Write File node)
```

### Exercise 2: Add Email Notifications

**Task:** Send email when pipeline fails

**Steps:**
1. Add "Email" node on error path
2. Configure SMTP settings
3. Set subject and body with error details

### Exercise 3: Rate Limiting

**Task:** Only allow 10 requests per minute

**Hint:**
```javascript
// In validation code node
const recentRequests = getRecentRequests(); // You implement this
if (recentRequests.length >= 10) {
  throw new Error('Rate limit exceeded');
}
```

### Exercise 4: Webhook Authentication

**Task:** Add API key authentication

**Solution:**
```javascript
const apiKey = $input.item.json.headers['x-api-key'];
const validKey = $env.API_KEY;

if (apiKey !== validKey) {
  throw new Error('Invalid API key');
}

return { authenticated: true };
```

---

## 🚀 Production Tips

### 1. Use Credentials

Store API keys securely:
1. Go to **Credentials** in sidebar
2. Create new credential
3. Type: Header Auth or API Key
4. Reference in nodes instead of hardcoding

### 2. Set Proper Timeouts

```json
{
  "timeout": 180000  // 3 minutes for large images
}
```

Rule of thumb:
- Simple tasks: 30s
- API calls: 60s
- Heavy processing: 180s+

### 3. Enable Execution Logging

1. **Settings** → **Log Output**
2. Set level: "verbose" for debugging
3. Monitor **Executions** tab

### 4. Add Monitoring

Create a monitoring workflow:
```
[Schedule: Every 5 min]
  → [Check if service is running]
  → [IF down: Send alert]
```

### 5. Backup Workflows

```bash
# Export all workflows
n8n export:workflow --all --output=backups/

# Import later
n8n import:workflow --input=backups/workflow.json
```

---

## 🎨 Best Practices

### 1. Name Your Nodes

**Bad:**
```
Code, Code 1, Code 2
```

**Good:**
```
Validate Input, Prepare Paths, Parse Result
```

### 2. Add Sticky Notes

Right-click canvas → Add Sticky Note

Use for:
- Configuration instructions
- Important notes
- Troubleshooting tips

### 3. Organize Workflows

```
Workflows/
├── Production/
│   ├── Image to LaTeX - Complete
│   └── Image to LaTeX - API
├── Development/
│   └── Testing workflows
└── Archive/
    └── Old versions
```

### 4. Use Sub-Workflows

For complex flows, create sub-workflows:
```
[Main Workflow]
  → [Execute Workflow: Preprocessing]
  → [Execute Workflow: Main Processing]
  → [Execute Workflow: Postprocessing]
```

### 5. Document Your Workflows

Add descriptions:
1. Workflow settings → Description
2. Explain what it does
3. List requirements
4. Note configuration needed

---

## 🔍 Common Patterns

### Pattern 1: Webhook → Process → Respond

```
[Webhook] → [Code/Execute] → [Respond to Webhook]
```

**Use for:** APIs, web forms

### Pattern 2: Schedule → Batch Process

```
[Cron] → [Read Files] → [For Each] → [Process]
```

**Use for:** Automated jobs, cleanup

### Pattern 3: Trigger → Notify → Log

```
[Trigger] → [IF: Error] → [Send Email] → [Write Log]
```

**Use for:** Monitoring, alerts

### Pattern 4: Webhook → Validate → Process → Respond

```
[Webhook] → [Validate] → [Process] → [IF: Success/Fail] → [Respond]
```

**Use for:** Secure APIs

---

## 🎯 Your Learning Path

### Level 1: Beginner ✅
- [x] Understand nodes and connections
- [x] Build simple webhook workflow
- [x] Use Code nodes
- [x] Test with curl

### Level 2: Intermediate 📚
- [ ] Add error handling
- [ ] Use environment variables
- [ ] Build batch processing workflow
- [ ] Add authentication

### Level 3: Advanced 🚀
- [ ] Create sub-workflows
- [ ] Implement monitoring
- [ ] Deploy to production
- [ ] Optimize performance

---

## 📚 Further Learning

### Official Resources
- **n8n Docs:** https://docs.n8n.io
- **n8n Community:** https://community.n8n.io
- **n8n YouTube:** https://youtube.com/@n8n-io

### Practice Projects
1. Build a form → email workflow
2. Create a Twitter bot
3. Automate data backups
4. Build a monitoring system

### Next Steps with This Pipeline

1. ✅ Import `complete_workflow.json`
2. ✅ Test with sample image
3. ✅ Modify and customize
4. ✅ Build your own workflow from scratch
5. ✅ Deploy to production

---

## 🎉 Congratulations!

You now understand:
- n8n fundamentals
- Building workflows
- Working with nodes
- Data flow
- Error handling
- Production deployment

**Keep learning by:**
- Building more workflows
- Joining n8n community
- Reading documentation
- Experimenting!

---

## 💡 Quick Reference Card

### Essential Shortcuts
- **Ctrl/Cmd + Enter**: Execute workflow
- **Ctrl/Cmd + S**: Save workflow
- **Ctrl/Cmd + A**: Select all nodes
- **Delete**: Delete selected node
- **Ctrl/Cmd + C/V**: Copy/Paste nodes

### Access Data
```javascript
$json            // Current node data
$input.item.json // Same as above
$env.API_KEY     // Environment variable
$now             // Current time
```

### Common Expressions
```javascript
{{ $json.fieldName }}           // Access field
{{ $json["field-name"] }}       // Field with special chars
{{ $json.field || 'default' }}  // With default value
{{ $json.arr[0] }}              // Array access
```

### Testing URLs
```
Webhook Test: http://localhost:5678/webhook-test/PATH
Webhook Prod:  http://localhost:5678/webhook/PATH
```

---

**Happy automating with n8n!** 🚀

Need help? Check [SETUP_GUIDE.md](SETUP_GUIDE.md) or [n8n community](https://community.n8n.io)
