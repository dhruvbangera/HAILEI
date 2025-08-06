# n8n Workflow Setup for HAILEI

## Overview
This directory contains the n8n workflow configuration that orchestrates all 6 HAILEI agents in sequence.

## Files
- `HAILEI_n8n_workflow.json` - Main workflow configuration
- `README.md` - This setup guide

## Setup Instructions

### 1. Prerequisites
- n8n installed (self-hosted or cloud)
- OpenAI API key
- HAILEI Streamlit agents running (optional for standalone testing)

### 2. Import Workflow
1. Open n8n interface
2. Go to Workflows → Import
3. Upload `HAILEI_n8n_workflow.json`

### 3. Configure Nodes

#### OpenAI Nodes Configuration
Each agent node needs:
```
Credentials: OpenAI API Key
Model: gpt-4
Temperature: 0.7
Max Tokens: 2000
```

#### Webhook Configuration
- Set up manual trigger or webhook trigger
- Configure input parameters for course topic/requirements

### 4. Agent Flow Sequence
```
Manual Trigger → HAILEI4T (MCP) → IPDAi → CAuthAi → TFDAi → EditorAi → EthosAi → SearchAi → Final Output
```

### 5. Test Workflow
1. Trigger workflow with sample input
2. Monitor each agent execution
3. Verify final compiled output

## Integration with Streamlit Agents

### Data Exchange Format
Agents export JSON data compatible with n8n workflow:
```json
{
  "course_title": "string",
  "course_data": {},
  "agent_outputs": {},
  "metadata": {}
}
```

### Webhook Endpoints
Configure these optional webhook URLs to trigger Streamlit agents:
- IPDAi: `http://localhost:8501/webhook/ipdai`
- CAuthAi: `http://localhost:8502/webhook/cauthai`
- (etc.)

## Troubleshooting

### Common Issues
1. **API Rate Limits**: Add delays between agent calls
2. **Token Limits**: Chunk large outputs
3. **Webhook Timeouts**: Increase timeout settings

### Monitoring
- Use n8n execution logs
- Monitor OpenAI API usage
- Track agent completion status

## Production Considerations
- Set up proper error handling
- Configure retry logic
- Implement logging and monitoring
- Secure API credentials