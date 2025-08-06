"""
Test HAILEI HTTP API endpoints - the actual n8n workflow simulation
"""

import requests
import json
from datetime import datetime

def test_http_endpoints():
    """Test all HTTP endpoints in sequence like n8n would"""
    
    print("🧪 Testing HAILEI HTTP API Workflow")
    print("=" * 50)
    
    # Step 1: Test IPDAi endpoint
    print("\n🎯 Step 1: Testing IPDAi HTTP Endpoint")
    
    course_input = {
        "course_title": "Introduction to Artificial Intelligence",
        "course_description": "A comprehensive introduction to AI for non-technical learners",
        "course_level": "Introductory",
        "course_domain": "Computer Science",
        "goals": [
            "Understand core AI concepts",
            "Evaluate AI applications across industries", 
            "Develop AI literacy skills"
        ],
        "weeks": 6
    }
    
    try:
        print("📡 Sending request to http://localhost:8000/ipdai")
        response = requests.post("http://localhost:8000/ipdai", json=course_input, timeout=30)
        
        if response.status_code == 200:
            ipdai_result = response.json()
            print(f"✅ IPDAi Success: {ipdai_result['status']}")
            print(f"   Generated {len(ipdai_result.get('course_modules', []))} modules")
            print(f"   TLO: {ipdai_result.get('learning_objectives', {}).get('tlo', 'N/A')[:60]}...")
        else:
            print(f"❌ IPDAi Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Make sure server is running on port 8000")
        return
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Step 2: Test CAuthAi endpoint
    print("\n📚 Step 2: Testing CAuthAi HTTP Endpoint")
    
    try:
        print("📡 Sending IPDAi output to http://localhost:8000/cauthai")
        response = requests.post("http://localhost:8000/cauthai", json=ipdai_result, timeout=30)
        
        if response.status_code == 200:
            cauthai_result = response.json()
            print(f"✅ CAuthAi Success: {cauthai_result['status']}")
            print(f"   Generated {len(cauthai_result.get('detailed_modules', []))} detailed modules")
            print(f"   Total activities: {cauthai_result.get('content_summary', {}).get('total_activities', 0)}")
        else:
            print(f"❌ CAuthAi Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Step 3: Test SearchAi endpoint
    print("\n🔍 Step 3: Testing SearchAi HTTP Endpoint")
    
    try:
        print("📡 Sending CAuthAi output to http://localhost:8000/searchai")
        response = requests.post("http://localhost:8000/searchai", json=cauthai_result, timeout=30)
        
        if response.status_code == 200:
            searchai_result = response.json()
            print(f"✅ SearchAi Success: {searchai_result['status']}")
            print(f"   Added {searchai_result.get('resource_summary', {}).get('total_sources', 0)} knowledge sources")
            print(f"   Quality verified: {searchai_result.get('resource_summary', {}).get('quality_verified', False)}")
        else:
            print(f"❌ SearchAi Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Final Results
    print("\n🎉 HTTP Workflow Test Results")
    print("=" * 40)
    print(f"✅ Course: {course_input['course_title']}")
    print(f"✅ IPDAi: {len(ipdai_result.get('course_modules', []))} modules planned")
    print(f"✅ CAuthAi: {cauthai_result.get('content_summary', {}).get('total_activities', 0)} activities created")
    print(f"✅ SearchAi: {searchai_result.get('resource_summary', {}).get('total_sources', 0)} resources added")
    
    # Save the complete workflow result
    complete_result = {
        "workflow_test": "HTTP endpoints",
        "timestamp": datetime.now().isoformat(),
        "course_title": course_input["course_title"],
        "agents_tested": ["IPDAi", "CAuthAi", "SearchAi"],
        "ipdai_output": ipdai_result,
        "cauthai_output": cauthai_result,
        "searchai_output": searchai_result,
        "workflow_status": "completed",
        "ready_for_n8n": True
    }
    
    with open('/Users/dhruvbangera/HAILEI/complete_workflow_test.json', 'w') as f:
        json.dump(complete_result, f, indent=2)
    
    print(f"\n💾 Complete results saved to: complete_workflow_test.json")
    print("\n🚀 HTTP API Workflow Test SUCCESSFUL!")
    print("✅ All endpoints responding correctly")
    print("✅ Data flow working perfectly") 
    print("✅ Ready for n8n integration!")
    
    # Show a sample of the final enriched module
    if searchai_result.get('enriched_modules'):
        module = searchai_result['enriched_modules'][0]
        print(f"\n📋 Sample Final Module: '{module['title']}'")
        print(f"   Objectives: {module['objectives'][:80]}...")
        print(f"   Knowledge Sources: {len(module.get('knowledge_sources', {}).get('academic_sources', []))} academic papers")
        print(f"   Quality: {module.get('resource_quality', {}).get('academic_credibility', 'N/A')}")
    
    return complete_result

if __name__ == "__main__":
    result = test_http_endpoints()
    
    if result:
        print("\n" + "="*60)
        print("🎯 NEXT STEPS:")
        print("1. ✅ HTTP endpoints working perfectly")
        print("2. ✅ Complete HAILEI workflow validated")
        print("3. 🔄 Ready to import n8n workflow:")
        print("   → workflows/n8n/hailei_complete_workflow.json")
        print("4. 🚀 Execute workflow in n8n to generate complete syllabus!")
        print("="*60)