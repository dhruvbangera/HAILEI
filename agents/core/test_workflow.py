"""
Test HAILEI Agent Workflow Data Flow
Tests IPDAi -> CAuthAi -> SearchAi data passing without external dependencies
"""

import json
from datetime import datetime
from typing import Dict, Any

class MockIPDAi:
    """Mock IPDAi for testing workflow data flow"""
    
    def process_course_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process course input and return structured IPDAi output"""
        
        course_title = input_data.get("course_title", "")
        course_desc = input_data.get("course_description", "")
        course_level = input_data.get("course_level", "Intermediate")
        goals = input_data.get("goals", [])
        weeks = input_data.get("weeks", 8)
        
        return {
            "agent": "IPDAi",
            "status": "completed",
            "course_title": course_title,
            "course_info": {
                "title": course_title,
                "description": course_desc,
                "level": course_level,
                "goals": goals,
                "weeks": weeks
            },
            "learning_objectives": {
                "tlo": "Students will analyze AI concepts, evaluate machine learning applications, and create intelligent solutions for real-world problems.",
                "elo": "• Identify types of machine learning algorithms\n• Explain neural network fundamentals\n• Evaluate AI applications across industries\n• Analyze ethical implications of AI systems\n• Communicate AI concepts to diverse audiences"
            },
            "pedagogical_frameworks": {
                "kdka": {
                    "knowledge": "AI fundamentals, machine learning types, neural networks, ethics",
                    "delivery": "Interactive demos, case studies, hands-on AI tools",
                    "context": "Real AI applications in healthcare, business, technology",
                    "assessment": "AI tool projects, case analysis, ethical discussions"
                },
                "prrr": {
                    "personal": "Career opportunities in AI and tech industry",
                    "relatable": "Everyday AI (Siri, Netflix, GPS), social media algorithms",
                    "relative": "Progressive understanding from basics to applications",
                    "realworld": "Industry case studies, AI tool usage, career pathways"
                }
            },
            "course_modules": [
                {
                    "module_number": 1,
                    "title": "AI Fundamentals & History",
                    "objectives": "Students will master key concepts in AI fundamentals and apply them practically",
                    "activities": "Interactive sessions, hands-on exercises, case studies related to AI fundamentals",
                    "assessment": "Formative quiz, practical project, peer discussion on AI fundamentals"
                },
                {
                    "module_number": 2,
                    "title": "Machine Learning Types & Applications",
                    "objectives": "Students will master key concepts in machine learning and apply them practically",
                    "activities": "Interactive sessions, hands-on exercises, case studies related to machine learning",
                    "assessment": "Formative quiz, practical project, peer discussion on machine learning"
                }
            ],
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "agent_version": "1.0",
                "processing_time": "2.3s"
            }
        }

class MockCAuthAi:
    """Mock CAuthAi for testing workflow data flow"""
    
    def process_ipdai_output(self, ipdai_data: Dict[str, Any]) -> Dict[str, Any]:
        """Take IPDAi output and generate detailed course content"""
        
        if ipdai_data.get("status") != "completed":
            return {"error": "IPDAi output not completed"}
        
        course_info = ipdai_data.get("course_info", {})
        modules = ipdai_data.get("course_modules", [])
        frameworks = ipdai_data.get("pedagogical_frameworks", {})
        
        # Generate detailed content for each module
        detailed_modules = []
        for module in modules:
            detailed_modules.append({
                "module_number": module["module_number"],
                "title": module["title"],
                "objectives": module["objectives"],
                "detailed_content": {
                    "lecture_notes": f"Comprehensive lecture notes covering {module['title']} with theoretical foundations and practical examples aligned with PRRR framework.",
                    "activities": [
                        f"Interactive workshop on {module['title']}",
                        f"Case study analysis related to {module['title']}",
                        f"Hands-on project applying {module['title']} concepts"
                    ],
                    "assessments": [
                        f"Formative quiz on {module['title']} fundamentals",
                        f"Practical project demonstrating {module['title']} skills",
                        f"Peer discussion forum on {module['title']} applications"
                    ],
                    "readings": [
                        f"Required textbook chapter on {module['title']}",
                        f"Supplementary articles on {module['title']} trends",
                        f"Case studies in {module['title']} applications"
                    ]
                },
                "prrr_alignment": {
                    "personal": f"Connect {module['title']} to student career goals",
                    "relatable": f"Use everyday examples of {module['title']}",
                    "relative": f"Show how {module['title']} supports course objectives",
                    "realworld": f"Industry applications of {module['title']}"
                }
            })
        
        return {
            "agent": "CAuthAi",
            "status": "completed",
            "course_title": course_info.get("title"),
            "source_agent": "IPDAi",
            "detailed_modules": detailed_modules,
            "scorm_package": {
                "status": "ready_for_export",
                "modules_count": len(detailed_modules),
                "estimated_size": "45MB"
            },
            "content_summary": {
                "total_activities": len(detailed_modules) * 3,
                "total_assessments": len(detailed_modules) * 3,
                "total_readings": len(detailed_modules) * 3,
                "framework_compliance": "KDKA + PRRR + TILT"
            },
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "agent_version": "1.0",
                "source_data_date": ipdai_data.get("metadata", {}).get("generated_date"),
                "processing_time": "3.7s"
            }
        }

class MockSearchAi:
    """Mock SearchAi for testing workflow data flow"""
    
    def process_cauthai_output(self, cauthai_data: Dict[str, Any]) -> Dict[str, Any]:
        """Take CAuthAi output and enrich with knowledge sources"""
        
        if cauthai_data.get("status") != "completed":
            return {"error": "CAuthAi output not completed"}
        
        course_title = cauthai_data.get("course_title")
        modules = cauthai_data.get("detailed_modules", [])
        
        # Enrich each module with knowledge sources
        enriched_modules = []
        for module in modules:
            enriched_modules.append({
                **module,
                "knowledge_sources": {
                    "academic_sources": [
                        f"IEEE papers on {module['title']}",
                        f"ACM Digital Library resources for {module['title']}",
                        f"Nature articles related to {module['title']}"
                    ],
                    "educational_resources": [
                        f"Khan Academy content on {module['title']}",
                        f"Coursera courses covering {module['title']}",
                        f"edX materials for {module['title']}"
                    ],
                    "industry_sources": [
                        f"Industry reports on {module['title']}",
                        f"Company case studies in {module['title']}",
                        f"Professional blogs about {module['title']}"
                    ],
                    "multimedia": [
                        f"YouTube educational videos on {module['title']}",
                        f"TED talks related to {module['title']}",
                        f"Interactive simulations for {module['title']}"
                    ]
                },
                "resource_quality": {
                    "academic_credibility": "verified",
                    "currency": "current within 2 years",
                    "accessibility": "meets WCAG 2.1 standards",
                    "licensing": "educational use approved"
                }
            })
        
        return {
            "agent": "SearchAi",
            "status": "completed", 
            "course_title": course_title,
            "source_agent": "CAuthAi",
            "enriched_modules": enriched_modules,
            "resource_summary": {
                "total_sources": len(enriched_modules) * 12,
                "source_types": ["academic", "educational", "industry", "multimedia"],
                "quality_verified": True,
                "accessibility_compliant": True
            },
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "agent_version": "1.0",
                "source_data_date": cauthai_data.get("metadata", {}).get("generated_date"),
                "processing_time": "1.8s"
            }
        }

def test_agent_workflow():
    """Test the complete agent workflow data flow"""
    
    print("🧪 Testing HAILEI Agent Workflow Data Flow\n")
    
    # Step 1: Initial course input
    print("📝 Step 1: Course Input")
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
        "weeks": 2  # Shortened for testing
    }
    print(f"✅ Input: {course_input['course_title']}")
    
    # Step 2: IPDAi Processing
    print("\n🎯 Step 2: IPDAi Processing")
    ipdai = MockIPDAi()
    ipdai_output = ipdai.process_course_input(course_input)
    print(f"✅ IPDAi Status: {ipdai_output['status']}")
    print(f"   Generated {len(ipdai_output['course_modules'])} modules")
    print(f"   TLO: {ipdai_output['learning_objectives']['tlo'][:50]}...")
    
    # Step 3: CAuthAi Processing
    print("\n📚 Step 3: CAuthAi Processing")
    cauthai = MockCAuthAi()
    cauthai_output = cauthai.process_ipdai_output(ipdai_output)
    print(f"✅ CAuthAi Status: {cauthai_output['status']}")
    print(f"   Generated content for {len(cauthai_output['detailed_modules'])} modules")
    print(f"   Total activities: {cauthai_output['content_summary']['total_activities']}")
    
    # Step 4: SearchAi Processing  
    print("\n🔍 Step 4: SearchAi Processing")
    searchai = MockSearchAi()
    searchai_output = searchai.process_cauthai_output(cauthai_output)
    print(f"✅ SearchAi Status: {searchai_output['status']}")
    print(f"   Added {searchai_output['resource_summary']['total_sources']} knowledge sources")
    print(f"   Quality verified: {searchai_output['resource_summary']['quality_verified']}")
    
    # Step 5: Display Final Result Structure
    print("\n📊 Step 5: Final Workflow Result")
    final_result = {
        "workflow_status": "completed",
        "agents_processed": ["IPDAi", "CAuthAi", "SearchAi"],
        "course_title": course_input["course_title"],
        "final_output": searchai_output,
        "workflow_metadata": {
            "total_processing_time": "7.8s",
            "agents_successful": 3,
            "data_flow_verified": True
        }
    }
    
    print(f"✅ Workflow Status: {final_result['workflow_status']}")
    print(f"   Agents Processed: {', '.join(final_result['agents_processed'])}")
    print(f"   Data Flow: {final_result['workflow_metadata']['data_flow_verified']}")
    
    # Save results for n8n testing
    with open('/Users/dhruvbangera/HAILEI/test_workflow_output.json', 'w') as f:
        json.dump(final_result, f, indent=2)
    
    print(f"\n💾 Results saved to: test_workflow_output.json")
    print("🎉 Workflow test completed successfully!")
    
    return final_result

if __name__ == "__main__":
    test_agent_workflow()