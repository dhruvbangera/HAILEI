"""
HAILEI Agent API Server
FastAPI server hosting HTTP endpoints for all HAILEI agents
For n8n workflow integration
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import json
import os
from datetime import datetime
import uvicorn

# Import our agent classes
from test_workflow import MockIPDAi, MockCAuthAi, MockSearchAi

app = FastAPI(
    title="HAILEI Agent API",
    description="HTTP API endpoints for HAILEI instructional design agents",
    version="1.0.0"
)

# Pydantic models for request/response validation
class CourseInput(BaseModel):
    course_title: str
    course_description: str
    course_level: str = "Intermediate"
    course_domain: str = ""
    goals: List[str]
    weeks: int = 8

class AgentResponse(BaseModel):
    agent: str
    status: str
    course_title: str
    metadata: Dict[str, Any]

# Initialize agents
ipdai = MockIPDAi()
cauthai = MockCAuthAi()
searchai = MockSearchAi()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "HAILEI Agent API",
        "status": "active",
        "agents": ["ipdai", "cauthai", "searchai", "tfdai", "editorai", "ethosai"],
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents_available": 6,
        "api_key_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

@app.post("/ipdai")
async def ipdai_endpoint(course_input: CourseInput):
    """
    IPDAi - Instructional Planning and Design Agent
    Creates foundational course structure, objectives, and frameworks
    """
    try:
        input_dict = course_input.dict()
        result = ipdai.process_course_input(input_dict)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IPDAi processing error: {str(e)}")

@app.post("/cauthai")
async def cauthai_endpoint(ipdai_data: Dict[str, Any]):
    """
    CAuthAi - Course Authoring Agent  
    Takes IPDAi output and creates detailed course content and activities
    """
    try:
        result = cauthai.process_ipdai_output(ipdai_data)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CAuthAi processing error: {str(e)}")

@app.post("/searchai")
async def searchai_endpoint(cauthai_data: Dict[str, Any]):
    """
    SearchAi - Semantic Search & Enrichment Agent
    Takes CAuthAi output and enriches with knowledge sources
    """
    try:
        result = searchai.process_cauthai_output(cauthai_data)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SearchAi processing error: {str(e)}")

@app.post("/tfdai")
async def tfdai_endpoint(searchai_data: Dict[str, Any]):
    """
    TFDAi - Technical & Functional Design Agent
    Takes SearchAi output and creates LMS technical specifications
    """
    try:
        # Mock TFDAi processing
        course_title = searchai_data.get("course_title")
        modules = searchai_data.get("enriched_modules", [])
        
        result = {
            "agent": "TFDAi",
            "status": "completed",
            "course_title": course_title,
            "source_agent": "SearchAi",
            "technical_specifications": {
                "target_lms": "Canvas",
                "scorm_version": "SCORM 2004",
                "mobile_compatible": True,
                "accessibility_compliant": "WCAG 2.1 AA"
            },
            "lms_mapping": {
                "modules": len(modules),
                "quizzes": len(modules) * 2,
                "discussions": len(modules),
                "assignments": len(modules) * 3
            },
            "integration_requirements": [
                "LTI 1.3 support",
                "Grade passback enabled",
                "Single sign-on (SSO)",
                "Mobile app compatibility"
            ],
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "agent_version": "1.0",
                "processing_time": "2.1s"
            }
        }
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TFDAi processing error: {str(e)}")

@app.post("/editorai")
async def editorai_endpoint(tfdai_data: Dict[str, Any]):
    """
    EditorAi - Content Review & Enhancement Agent
    Takes TFDAi output and reviews for quality, accessibility, and alignment
    """
    try:
        course_title = tfdai_data.get("course_title")
        
        result = {
            "agent": "EditorAi",
            "status": "completed",
            "course_title": course_title,
            "source_agent": "TFDAi",
            "review_results": {
                "grammar_check": "passed",
                "clarity_score": 92,
                "blooms_alignment": "verified",
                "accessibility_score": 95,
                "kdka_compliance": "validated",
                "prrr_integration": "confirmed"
            },
            "enhancements_made": [
                "Improved sentence structure for clarity",
                "Added alt text for visual elements",
                "Verified Bloom's taxonomy verb usage",
                "Enhanced PRRR framework integration",
                "Standardized formatting across modules"
            ],
            "quality_metrics": {
                "readability_level": "appropriate for course level",
                "content_length": "optimal for learning objectives",
                "engagement_score": 88,
                "pedagogical_soundness": "excellent"
            },
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "agent_version": "1.0",
                "processing_time": "3.2s"
            }
        }
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"EditorAi processing error: {str(e)}")

@app.post("/ethosai")
async def ethosai_endpoint(editorai_data: Dict[str, Any]):
    """
    EthosAi - Ethical Oversight Agent  
    Takes EditorAi output and ensures ethical compliance and inclusivity
    """
    try:
        course_title = editorai_data.get("course_title")
        
        result = {
            "agent": "EthosAi",
            "status": "completed",
            "course_title": course_title,
            "source_agent": "EditorAi",
            "ethical_audit": {
                "bias_detection": "no bias detected",
                "inclusivity_score": 94,
                "cultural_sensitivity": "reviewed and approved",
                "privacy_compliance": "FERPA compliant",
                "accessibility_audit": "meets UDL guidelines"
            },
            "compliance_checklist": {
                "academic_integrity": True,
                "inclusive_language": True,
                "cultural_awareness": True,
                "accessibility_standards": True,
                "ethical_ai_use": True,
                "student_privacy": True
            },
            "recommendations": [
                "Continue monitoring for bias in future updates",
                "Regular accessibility audits recommended",
                "Student feedback integration suggested"
            ],
            "final_approval": {
                "ethical_clearance": "approved",
                "ready_for_deployment": True,
                "approval_date": datetime.now().isoformat()
            },
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "agent_version": "1.0", 
                "processing_time": "1.9s"
            }
        }
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"EthosAi processing error: {str(e)}")

@app.post("/complete-workflow")
async def complete_workflow_endpoint(course_input: CourseInput):
    """
    Complete HAILEI workflow - runs all agents in sequence
    This endpoint demonstrates the full workflow for testing
    """
    try:
        workflow_start = datetime.now()
        
        # Step 1: IPDAi
        input_dict = course_input.dict()
        ipdai_result = ipdai.process_course_input(input_dict)
        
        # Step 2: CAuthAi
        cauthai_result = cauthai.process_ipdai_output(ipdai_result)
        
        # Step 3: SearchAi
        searchai_result = searchai.process_cauthai_output(cauthai_result)
        
        # Step 4: TFDAi (mock)
        tfdai_result = await tfdai_endpoint(searchai_result)
        
        # Step 5: EditorAi (mock)
        editorai_result = await editorai_endpoint(tfdai_result)
        
        # Step 6: EthosAi (mock)
        ethosai_result = await ethosai_endpoint(editorai_result)
        
        workflow_end = datetime.now()
        processing_time = (workflow_end - workflow_start).total_seconds()
        
        final_result = {
            "workflow": "HAILEI Complete",
            "status": "completed",
            "course_title": course_input.course_title,
            "agents_processed": ["IPDAi", "CAuthAi", "SearchAi", "TFDAi", "EditorAi", "EthosAi"],
            "final_output": ethosai_result,
            "workflow_metadata": {
                "start_time": workflow_start.isoformat(),
                "end_time": workflow_end.isoformat(),
                "total_processing_time": f"{processing_time:.2f}s",
                "agents_successful": 6,
                "final_approval": ethosai_result["final_approval"]["ready_for_deployment"]
            }
        }
        
        return final_result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Complete workflow error: {str(e)}")

# Agent status endpoints
@app.get("/agents/status")
async def agents_status():
    """Get status of all agents"""
    return {
        "agents": {
            "IPDAi": {"status": "active", "endpoint": "/ipdai"},
            "CAuthAi": {"status": "active", "endpoint": "/cauthai"},
            "SearchAi": {"status": "active", "endpoint": "/searchai"},
            "TFDAi": {"status": "active", "endpoint": "/tfdai"},
            "EditorAi": {"status": "active", "endpoint": "/editorai"},
            "EthosAi": {"status": "active", "endpoint": "/ethosai"}
        },
        "workflow_endpoint": "/complete-workflow"
    }

if __name__ == "__main__":
    print("🚀 Starting HAILEI Agent API Server...")
    print("📍 Endpoints available:")
    print("   http://localhost:8000/ipdai")
    print("   http://localhost:8000/cauthai") 
    print("   http://localhost:8000/searchai")
    print("   http://localhost:8000/tfdai")
    print("   http://localhost:8000/editorai")
    print("   http://localhost:8000/ethosai")
    print("   http://localhost:8000/complete-workflow")
    print("📚 API docs: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)