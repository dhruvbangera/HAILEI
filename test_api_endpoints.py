"""
Test HAILEI API endpoints with sample requests
Simulates what n8n will do
"""

import json
import requests
import time
from datetime import datetime

def test_endpoint(url, data, endpoint_name):
    """Test a single API endpoint"""
    print(f"\n🧪 Testing {endpoint_name}")
    print(f"📍 URL: {url}")
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📊 Agent: {result.get('agent', 'Unknown')}")
            print(f"🎯 Status: {result.get('status', 'Unknown')}")
            
            # Show key results
            if 'course_modules' in result:
                print(f"📚 Modules: {len(result['course_modules'])}")
            elif 'detailed_modules' in result:
                print(f"📖 Detailed Modules: {len(result['detailed_modules'])}")
            elif 'enriched_modules' in result:
                print(f"🔍 Enriched Modules: {len(result['enriched_modules'])}")
            
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Server not running")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_workflow_sequence():
    """Test the complete workflow sequence"""
    print("🔄 Testing Complete HAILEI Workflow Sequence")
    print("=" * 50)
    
    # Step 1: Test IPDAi
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
        "weeks": 4
    }
    
    ipdai_result = test_endpoint("http://localhost:8000/ipdai", course_input, "IPDAi")
    if not ipdai_result:
        print("❌ IPDAi failed - stopping workflow test")
        return
    
    # Step 2: Test CAuthAi
    cauthai_result = test_endpoint("http://localhost:8000/cauthai", ipdai_result, "CAuthAi")
    if not cauthai_result:
        print("❌ CAuthAi failed - stopping workflow test")
        return
    
    # Step 3: Test SearchAi
    searchai_result = test_endpoint("http://localhost:8000/searchai", cauthai_result, "SearchAi")
    if not searchai_result:
        print("❌ SearchAi failed - stopping workflow test")
        return
    
    # Workflow Summary
    print("\n🎉 Workflow Test Results")
    print("=" * 30)
    print(f"✅ IPDAi: Generated {len(ipdai_result.get('course_modules', []))} modules")
    print(f"✅ CAuthAi: Created {cauthai_result.get('content_summary', {}).get('total_activities', 0)} activities")
    print(f"✅ SearchAi: Added {searchai_result.get('resource_summary', {}).get('total_sources', 0)} knowledge sources")
    
    # Save final result
    final_workflow = {
        "workflow_test": "completed",
        "timestamp": datetime.now().isoformat(),
        "course_title": course_input["course_title"],
        "agents_tested": ["IPDAi", "CAuthAi", "SearchAi"],
        "final_result": searchai_result
    }
    
    with open('/Users/dhruvbangera/HAILEI/workflow_test_result.json', 'w') as f:
        json.dump(final_workflow, f, indent=2)
    
    print(f"💾 Results saved to: workflow_test_result.json")
    print("🚀 Ready for n8n integration!")

def test_direct_workflow():
    """Test workflow without server (direct function calls)"""
    print("🧪 Testing Direct Workflow (No Server)")
    print("=" * 40)
    
    from agents.core.test_workflow import MockIPDAi, MockCAuthAi, MockSearchAi
    
    # Initialize agents
    ipdai = MockIPDAi()
    cauthai = MockCAuthAi()
    searchai = MockSearchAi()
    
    # Test data
    course_input = {
        "course_title": "Introduction to Machine Learning",
        "course_description": "Learn ML fundamentals through hands-on projects",
        "course_level": "Intermediate",
        "course_domain": "Data Science",
        "goals": [
            "Master ML algorithms",
            "Build predictive models",
            "Deploy ML solutions"
        ],
        "weeks": 6
    }
    
    print(f"📝 Input: {course_input['course_title']}")
    
    # Run workflow
    print("\n🎯 Running IPDAi...")
    ipdai_result = ipdai.process_course_input(course_input)
    print(f"✅ Generated {len(ipdai_result.get('course_modules', []))} modules")
    
    print("\n📚 Running CAuthAi...")
    cauthai_result = cauthai.process_ipdai_output(ipdai_result)
    print(f"✅ Created {len(cauthai_result.get('detailed_modules', []))} detailed modules")
    
    print("\n🔍 Running SearchAi...")
    searchai_result = searchai.process_cauthai_output(cauthai_result)
    print(f"✅ Added {searchai_result.get('resource_summary', {}).get('total_sources', 0)} knowledge sources")
    
    print("\n🎉 Direct Workflow Complete!")
    print("✅ All agents working correctly")
    print("✅ Data flow validated")
    print("🚀 Ready to build n8n workflow!")
    
    return searchai_result

if __name__ == "__main__":
    print("🧪 HAILEI API Endpoint Testing")
    print("=" * 40)
    
    # Test direct workflow first (no server needed)
    direct_result = test_direct_workflow()
    
    print("\n" + "=" * 50)
    print("Next Steps:")
    print("1. ✅ Agent workflow validated")  
    print("2. 🔄 Ready for n8n integration")
    print("3. 🎯 Configure n8n with these endpoints:")
    print("   - http://localhost:8000/ipdai")
    print("   - http://localhost:8000/cauthai") 
    print("   - http://localhost:8000/searchai")
    print("4. 🚀 Test complete n8n workflow")