# HAILEI Render Deployment Guide

## Quick Deployment Steps

### 1. Create Render Account
- Go to [render.com](https://render.com) and sign up
- Connect your GitHub account

### 2. Deploy to Render
1. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the HAILEI repository

2. **Configure Deployment**
   - **Name**: `hailei-agents`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r agents/production/requirements.txt`
   - **Start Command**: `python agents/production/main.py`
   - **Plan**: Free (sufficient for testing)

3. **Environment Variables**
   - `RENDER=production`
   - `PORT` will be automatically set by Render

### 3. Alternative: Auto-Deploy with render.yaml
1. Place `render.yaml` in your repository root:
   ```bash
   cp agents/production/render.yaml ./render.yaml
   ```

2. Update render.yaml paths:
   ```yaml
   buildCommand: pip install -r agents/production/requirements.txt
   startCommand: python agents/production/main.py
   ```

3. Push to GitHub and deploy automatically

## API Endpoints

Once deployed, your service will be available at:
`https://hailei-agents.onrender.com`

### Available Endpoints:
- `GET /` - Service info
- `GET /health` - Health check
- `GET /docs` - API documentation
- `POST /ipdai` - Instructional Planning Agent
- `POST /cauthai` - Course Authoring Agent
- `POST /searchai` - Search & Enrichment Agent
- `POST /tfdai` - Technical Design Agent
- `POST /editorai` - Content Review Agent
- `POST /ethosai` - Ethical Oversight Agent
- `POST /complete-workflow` - Run all 6 agents

## n8n Cloud Integration

### 1. Import Workflow
- Import `workflows/n8n/hailei_render_workflow.json` into n8n Cloud
- All endpoints point to your Render deployment

### 2. Test Workflow
- Use the manual trigger in n8n
- Monitor execution in n8n Cloud interface
- Check Render logs for any issues

## Testing Deployment

### Local Test (before deployment):
```bash
cd agents/production
python main.py
```

### Test Production Endpoints:
```bash
curl https://hailei-agents.onrender.com/health
curl https://hailei-agents.onrender.com/docs
```

## Troubleshooting

### Common Issues:
1. **Build Failures**: Check requirements.txt dependencies
2. **Port Issues**: Ensure main.py uses `os.environ.get("PORT", 8000)`
3. **CORS Issues**: Verified - configured for n8n Cloud access
4. **Timeout Issues**: Render free tier has 15-minute idle timeout

### Checking Logs:
- Go to Render dashboard → Your service → Logs
- Monitor real-time logs during n8n workflow execution

## Production Considerations

### Free Tier Limitations:
- 15-minute idle timeout (service sleeps)
- Limited CPU/memory
- Shared IP address

### Upgrading:
- Consider paid plan for production use
- Custom domains available
- Better performance and uptime

## Next Steps

1. ✅ Deploy to Render
2. ✅ Test health endpoint
3. ✅ Import n8n workflow
4. ✅ Run complete HAILEI workflow
5. 🚀 Generate your first AI-powered syllabus!