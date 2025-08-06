"""
IPDAi API Endpoint - Accepts JSON input, returns structured course data
For use in n8n workflow orchestration
"""

import json
from typing import Dict, Any
import openai
import os
from datetime import datetime

class IPDAiAPI:
    def __init__(self, api_key: str = None):
        """Initialize IPDAi with OpenAI API key"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate_with_ai(self, prompt: str, max_tokens: int = 800) -> str:
        """Generate content using OpenAI API"""
        if not self.api_key:
            return None
            
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert instructional designer specializing in KDKA and PRRR pedagogical frameworks."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def process_course_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing function - takes course input, returns structured output
        
        Input Schema:
        {
            "course_title": str,
            "course_description": str,
            "course_level": str,
            "course_domain": str,
            "goals": [str],
            "weeks": int
        }
        
        Output Schema:
        {
            "agent": "IPDAi",
            "course_title": str,
            "course_info": {...},
            "learning_objectives": {...},
            "pedagogical_frameworks": {...},
            "course_modules": [...],
            "metadata": {...}
        }
        """
        
        # Extract input data
        course_title = input_data.get("course_title", "")
        course_desc = input_data.get("course_description", "")
        course_level = input_data.get("course_level", "Intermediate")
        course_domain = input_data.get("course_domain", "")
        goals = input_data.get("goals", [])
        weeks = input_data.get("weeks", 8)
        
        # Validate input
        if not course_title or not course_desc or len(goals) < 2:
            return {
                "error": "Missing required fields: course_title, course_description, and at least 2 goals"
            }
        
        result = {
            "agent": "IPDAi",
            "course_title": course_title,
            "course_info": {
                "title": course_title,
                "description": course_desc,
                "level": course_level,
                "domain": course_domain,
                "goals": goals,
                "weeks": weeks
            },
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "agent_version": "1.0",
                "ai_enabled": bool(self.api_key)
            }
        }
        
        # Generate Learning Objectives
        objectives = self._generate_learning_objectives(course_title, course_desc, course_level, goals)
        result["learning_objectives"] = objectives
        
        # Generate Pedagogical Frameworks
        frameworks = self._generate_frameworks(course_title, course_desc, course_level, course_domain)
        result["pedagogical_frameworks"] = frameworks
        
        # Generate Course Modules
        modules = self._generate_modules(course_title, course_desc, course_level, weeks, goals)
        result["course_modules"] = modules
        
        return result
    
    def _generate_learning_objectives(self, title: str, desc: str, level: str, goals: list) -> Dict[str, str]:
        """Generate TLO and ELOs"""
        if self.api_key:
            prompt = f"""
Create learning objectives for: {title}
Description: {desc}
Level: {level}
Goals: {', '.join(goals)}

Generate:
1. ONE Terminal Learning Objective (TLO)
2. 5-6 Enabling Learning Objectives (ELOs)

Use Bloom's taxonomy verbs appropriate for {level} level.
Format as:
TLO: [objective]
ELOs:
• [objective 1]
• [objective 2]
• [etc.]
"""
            
            result = self.generate_with_ai(prompt)
            if result and "TLO:" in result:
                parts = result.split('ELOs:')
                tlo = parts[0].replace('TLO:', '').strip()
                elo = parts[1].strip() if len(parts) > 1 else "• Generated objectives"
                return {"tlo": tlo, "elo": elo}
        
        # Fallback for specific course types
        if "artificial intelligence" in title.lower() or "ai" in title.lower():
            return {
                "tlo": "Students will analyze AI concepts, evaluate machine learning applications, and create intelligent solutions for real-world problems.",
                "elo": "• Identify types of machine learning algorithms\n• Explain neural network fundamentals\n• Evaluate AI applications across industries\n• Analyze ethical implications of AI systems\n• Communicate AI concepts to diverse audiences"
            }
        else:
            return {
                "tlo": f"Students will analyze core concepts in {title.lower()}, evaluate practical applications, and create innovative solutions.",
                "elo": "• Master fundamental principles\n• Apply theoretical frameworks\n• Analyze complex problems\n• Develop creative solutions\n• Communicate professionally"
            }
    
    def _generate_frameworks(self, title: str, desc: str, level: str, domain: str) -> Dict[str, Dict[str, str]]:
        """Generate KDKA and PRRR frameworks"""
        if self.api_key:
            prompt = f"""
Create KDKA and PRRR frameworks for: {title}
Description: {desc}
Level: {level}

KDKA: Knowledge, Delivery, Context, Assessment
PRRR: Personal, Relatable, Relative, Real-world

Return as JSON format.
"""
            
            result = self.generate_with_ai(prompt, 600)
            # Try to parse JSON from result (simplified)
            
        # Fallback framework generation
        if "artificial intelligence" in title.lower():
            return {
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
            }
        else:
            return {
                "kdka": {
                    "knowledge": f"Core {domain} principles and applications",
                    "delivery": "Interactive lectures, workshops, projects",
                    "context": f"Current {domain} trends and applications",
                    "assessment": "Projects, portfolios, presentations"
                },
                "prrr": {
                    "personal": f"Personal interests in {domain}",
                    "relatable": "Current events and popular examples",
                    "relative": "Systematic skill progression",
                    "realworld": f"Professional {domain} applications"
                }
            }
    
    def _generate_modules(self, title: str, desc: str, level: str, weeks: int, goals: list) -> list:
        """Generate course modules"""
        if "artificial intelligence" in title.lower():
            module_titles = [
                "AI Fundamentals & History",
                "Machine Learning Types & Applications", 
                "Neural Networks & Deep Learning",
                "AI in Healthcare & Medicine",
                "AI in Business & Finance",
                "Natural Language Processing",
                "AI Ethics & Bias",
                "Future of AI & Career Pathways"
            ][:weeks]
        else:
            module_titles = [
                f"{title} Foundations",
                f"Core {title} Concepts",
                "Practical Applications",
                "Analysis & Critical Thinking",
                "Advanced Topics",
                "Real-World Cases",
                "Professional Practice",
                "Synthesis & Future Directions"
            ][:weeks]
        
        modules = []
        for i, module_title in enumerate(module_titles):
            modules.append({
                "module_number": i + 1,
                "title": module_title,
                "objectives": f"Students will master key concepts in {module_title.lower()} and apply them practically",
                "activities": f"Interactive sessions, hands-on exercises, case studies related to {module_title.lower()}",
                "assessment": f"Formative quiz, practical project, peer discussion on {module_title.lower()}"
            })
        
        return modules

# Test function
def test_ipdai_api():
    """Test the IPDAi API with sample data"""
    api = IPDAiAPI()
    
    test_input = {
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
    
    result = api.process_course_input(test_input)
    return result

if __name__ == "__main__":
    # Test the API
    result = test_ipdai_api()
    print(json.dumps(result, indent=2))