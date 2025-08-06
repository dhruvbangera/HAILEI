# HAILEI Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
cd HAILEI
pip install -r requirements/requirements.txt
```

### 2. Launch Main Dashboard
```bash
cd agents/streamlit
streamlit run main.py
```

### 3. Test Individual Agents
```bash
# Example: Run IPDAi
streamlit run IPDAi.py
```

## Testing Your Installation

### ✅ Dependency Check
All agents tested and working with these imports:
- streamlit ✅
- requests ✅ 
- json ✅
- datetime ✅
- typing ✅

### 🖥️ Agent Functionality
- **IPDAi**: Course planning with JSON export ✅
- **CAuthAi**: Content authoring with PRRR/TILT ✅
- **TFDAi**: LMS technical specifications ✅
- **EditorAi**: Content review & Bloom's analysis ✅
- **EthosAi**: Ethical compliance checking ✅
- **SearchAi**: Resource enrichment ✅

### 🔗 n8n Integration Ready
- JSON exports configured for workflow data exchange
- Webhook-compatible output formats
- Agent coordination protocols defined

## Next Steps for n8n

1. **Import Workflow**: Load `workflows/n8n/HAILEI_n8n_workflow.json`
2. **Configure API Keys**: Set up OpenAI API access
3. **Test Webhook Triggers**: Verify agent-to-agent data flow

Your HAILEI system is ready for production use!