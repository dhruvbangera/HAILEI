# HAILEI n8n Workflow Setup Instructions

## 🚀 Quick Setup Guide

### Prerequisites
- n8n installed (self-hosted or cloud)
- HAILEI agent endpoints running
- OpenAI API key (optional for AI generation)

### Step 1: Import Workflow
1. Open n8n interface
2. Go to **Workflows** → **Import from File**
3. Upload `hailei_complete_workflow.json`
4. Click **Import Workflow**

### Step 2: Configure Environment
Set these environment variables in n8n:

```bash
# Optional - for real AI generation
OPENAI_API_KEY=your_openai_api_key_here

# Agent endpoints (if different from localhost)
HAILEI_API_BASE=http://localhost:8000
```

### Step 3: Start Agent Server
```bash
cd /Users/dhruvbangera/HAILEI/agents/core
python3 simple_server.py
```

**Verify endpoints are running:**
- http://localhost:8000/health
- http://localhost:8000/ipdai
- http://localhost:8000/cauthai  
- http://localhost:8000/searchai

### Step 4: Test Workflow

#### Option A: Manual Trigger (Recommended for Testing)
1. Click **Execute Workflow** 
2. The workflow will use default course data:
   - Course: "Introduction to Artificial Intelligence"
   - Level: "Introductory"
   - 8 weeks, 3 goals

#### Option B: Custom Input
Modify the first node (Start Workflow) to accept custom data:
```json
{
  "course_title": "Your Course Title",
  "course_description": "Your course description",
  "course_level": "Introductory|Intermediate|Advanced",
  "course_domain": "Your domain",
  "goals": ["Goal 1", "Goal 2", "Goal 3"],
  "weeks": 8
}
```

### Step 5: Monitor Execution

The workflow processes through **6 agents sequentially**:

1. ✅ **IPDAi** - Course planning & objectives
2. ✅ **CAuthAi** - Detailed content creation  
3. ✅ **SearchAi** - Knowledge source enrichment
4. ✅ **TFDAi** - Technical LMS specifications
5. ✅ **EditorAi** - Content review & enhancement
6. ✅ **EthosAi** - Ethical compliance validation

**Expected Processing Time:** 15-30 seconds total

## 📊 Expected Outputs

### Final Files Generated:
- `hailei_complete_syllabus.json` - Complete course syllabus
- `hailei_error_log.json` - Error log (if issues occur)

### Email Notification:
- Sent to: `instructor@university.edu`
- Subject: "HAILEI Course Generation Complete: [Course Title]"

## 🛠️ Troubleshooting

### Common Issues:

**❌ Connection Error to Agent Endpoints**
```
Solution: Ensure agent server is running on localhost:8000
Check: curl http://localhost:8000/health
```

**❌ JSON Parsing Error**
```
Solution: Verify agent responses are valid JSON
Check agent logs for error details
```

**❌ Workflow Timeout**
```
Solution: Increase timeout in workflow settings
Current: 900s (15 minutes)
Max: 3600s (1 hour)
```

### Debug Mode:
1. Enable **Save execution data** in workflow settings
2. Check execution logs in n8n interface
3. Verify each agent's response data

## 🔧 Advanced Configuration

### Custom Agent Endpoints:
Modify HTTP Request nodes to use different URLs:
```
Production: https://api.hailei.edu/ipdai
Development: http://localhost:8000/ipdai
```

### OpenAI Integration:
To enable real AI generation instead of templates:
1. Set `OPENAI_API_KEY` environment variable
2. Agents will automatically use GPT for intelligent content generation

### Email Configuration:
Update the "Notify Completion" node with your SMTP settings:
- SMTP server
- Authentication credentials  
- From/To email addresses

## 📈 Monitoring & Analytics

### Execution Metrics:
- Average processing time per agent
- Success/failure rates
- Error patterns

### Data Quality Metrics:
- Course modules generated
- Knowledge sources added
- Quality scores from EditorAi
- Ethical compliance status

## 🚀 Production Deployment

### Scaling Considerations:
- Deploy agents as containerized microservices
- Use load balancer for multiple agent instances
- Implement queue system for high volume
- Set up monitoring and alerting

### Security:
- Secure API endpoints with authentication
- Encrypt sensitive data in transit
- Audit log all course generation activities
- Implement rate limiting

## 📞 Support

For technical issues:
1. Check agent server logs
2. Verify n8n execution data
3. Review error logs in output files
4. Contact HAILEI support team

---

**Next Steps:**
1. ✅ Import workflow to n8n
2. ✅ Start agent server  
3. ✅ Test with sample course
4. 🎯 Generate your first HAILEI syllabus!