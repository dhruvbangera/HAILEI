import streamlit as st
import json
from datetime import datetime
import openai
import os
from typing import Dict, List

st.set_page_config(page_title="IPDAi - AI Course Planning Agent", layout="wide")

st.title("🤖 IPDAi - AI-Powered Course Planning Agent")
st.markdown("**True AI Generation:** Uses OpenAI GPT to intelligently create KDKA/PRRR-compliant course content!")

# OpenAI API Setup
@st.cache_data
def setup_openai():
    """Setup OpenAI client"""
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OpenAI API key required. Set OPENAI_API_KEY environment variable or add to Streamlit secrets.")
        st.info("For demo purposes, you can still use the template-based generation below.")
        return None
    openai.api_key = api_key
    return True

# API key input fallback
if not setup_openai():
    api_key_input = st.text_input("Enter OpenAI API Key (optional - for true AI generation):", type="password")
    if api_key_input:
        openai.api_key = api_key_input
        st.success("✅ OpenAI API key configured!")
        st.rerun()

def generate_with_ai(prompt: str) -> str:
    """Generate content using OpenAI API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert instructional designer specializing in KDKA and PRRR pedagogical frameworks. Generate educational content that is pedagogically sound, engaging, and appropriate for the specified course level."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"AI generation failed: {e}")
        return None

# Initialize session state
for key in ['objectives_generated', 'frameworks_generated', 'modules_generated']:
    if key not in st.session_state:
        st.session_state[key] = False

# ===== STEP 1: BASIC COURSE INFO =====
st.header("Step 1: Basic Course Information")
course_title = st.text_input("Course Title")
course_desc = st.text_area("Course Description", height=100)
course_level = st.selectbox("Course Level", ["Introductory", "Intermediate", "Advanced"])
course_domain = st.text_input("Course Domain (e.g., STEM, Business, Humanities)")
weeks = st.slider("Number of Modules", 4, 12, 8)

# ===== STEP 2: SIMPLE GOALS =====
st.header("Step 2: Course Goals")
st.markdown("What should students achieve? (Enter 2-4 broad goals)")
goal1 = st.text_input("Primary Goal")
goal2 = st.text_input("Secondary Goal")
goal3 = st.text_input("Additional Goal (optional)")

goals = [g for g in [goal1, goal2, goal3] if g.strip()]

# ===== STEP 3: AI MAGIC STARTS HERE =====
st.header("🪄 Step 3: Let AI Do the Heavy Lifting")

ready_for_ai = course_title and course_desc and len(goals) >= 2

if ready_for_ai:
    col1, col2, col3 = st.columns(3)
    
    # Generate Learning Objectives
    with col1:
        if st.button("🎯 Generate Learning Objectives", type="primary", disabled=st.session_state.objectives_generated):
            with st.spinner("🧠 AI generating learning objectives..."):
                # Create AI prompt for learning objectives
                prompt = f"""
Create pedagogically sound learning objectives for this course:

Course: {course_title}
Description: {course_desc}
Level: {course_level}
Goals: {', '.join(goals)}

Generate:
1. ONE Terminal Learning Objective (TLO) using appropriate Bloom's taxonomy verbs for {course_level} level
2. 5-6 Enabling Learning Objectives (ELOs) that support the TLO

Requirements:
- Use Bloom's taxonomy verbs appropriate for {course_level} level
- Make objectives measurable and specific
- Align with course goals
- Format as: TLO: [single paragraph], ELOs: [bulleted list]
"""
                
                # Try AI generation first, fallback to templates
                ai_result = generate_with_ai(prompt)
                if ai_result and openai.api_key:
                    # Parse AI response (simple parsing)
                    lines = ai_result.split('\n')
                    tlo_line = next((line for line in lines if 'TLO:' in line), '')
                    tlo = tlo_line.replace('TLO:', '').strip() if tlo_line else ai_result.split('\n')[0]
                    
                    elo_lines = [line.strip() for line in lines if line.strip().startswith(('•', '-', '1.', '2.', '3.', '4.', '5.', '6.'))]
                    elo = '\n'.join(elo_lines) if elo_lines else "• AI-generated enabling objectives"
                else:
                    # Fallback to improved templates
                    if "artificial intelligence" in course_title.lower() or "ai" in course_title.lower():
                        tlo = "Students will analyze AI concepts, evaluate machine learning applications, and create intelligent solutions for real-world problems."
                        elo = "• Identify types of machine learning algorithms\n• Explain neural network fundamentals\n• Evaluate AI applications across industries\n• Analyze ethical implications of AI systems\n• Communicate AI concepts to diverse audiences"
                    elif "data science" in course_title.lower():
                        tlo = "Students will analyze datasets, evaluate statistical models, and create data-driven solutions for real-world problems."
                        elo = "• Identify and clean data sources\n• Apply statistical analysis techniques\n• Create compelling visualizations\n• Build predictive models\n• Communicate findings effectively"
                    else:
                        tlo = f"Students will analyze core concepts in {course_title.lower()}, evaluate practical applications, and create innovative solutions for real-world challenges."
                        elo = f"• Master fundamental principles\n• Apply theoretical frameworks\n• Analyze complex problems\n• Develop creative solutions\n• Communicate professionally"
                
                st.session_state.tlo = tlo
                st.session_state.elo = elo
                st.session_state.objectives_generated = True
                st.rerun()
    
    # Generate KDKA/PRRR Frameworks  
    with col2:
        if st.button("🧠 Generate Frameworks", type="primary", disabled=st.session_state.frameworks_generated):
            # Auto-generate based on course type
            if "data science" in course_title.lower():
                kdka = {
                    "knowledge": "Statistical concepts, programming, ML principles, ethics",
                    "delivery": "Hands-on labs, case studies, projects", 
                    "context": "Real datasets, industry applications",
                    "assessment": "Portfolio, projects, peer review"
                }
                prrr = {
                    "personal": "Career goals in tech/analytics",
                    "relatable": "Social media data, sports stats",
                    "relative": "Builds toward complete projects", 
                    "realworld": "Industry partnerships, internships"
                }
            elif "artificial intelligence" in course_title.lower() or "ai" in course_title.lower() or "machine learning" in course_title.lower():
                kdka = {
                    "knowledge": "AI fundamentals, machine learning types, neural networks, ethics",
                    "delivery": "Interactive demos, case studies, hands-on AI tools",
                    "context": "Real AI applications in healthcare, business, technology",
                    "assessment": "AI tool projects, case analysis, ethical discussions"
                }
                prrr = {
                    "personal": "Career opportunities in AI and tech industry",
                    "relatable": "Everyday AI (Siri, Netflix, GPS), social media algorithms",
                    "relative": "Progressive understanding from basics to applications",
                    "realworld": "Industry case studies, AI tool usage, career pathways"
                }
            elif "business" in course_title.lower():
                kdka = {
                    "knowledge": "Strategy, finance, leadership, operations",
                    "delivery": "Case studies, simulations, guest speakers",
                    "context": "Current business environment",
                    "assessment": "Business plans, case analysis"
                }
                prrr = {
                    "personal": "Entrepreneurial aspirations",
                    "relatable": "Startups, local businesses",
                    "relative": "Progressive skill building",
                    "realworld": "Internships, competitions"
                }
            else:
                kdka = {
                    "knowledge": f"Core {course_domain} principles and applications",
                    "delivery": "Interactive lectures, workshops, projects",
                    "context": f"Current {course_domain} trends and applications", 
                    "assessment": "Projects, portfolios, presentations"
                }
                prrr = {
                    "personal": f"Personal interests in {course_domain}",
                    "relatable": "Current events and popular examples",
                    "relative": "Systematic skill progression",
                    "realworld": f"Professional {course_domain} applications"
                }
            
            st.session_state.kdka = kdka
            st.session_state.prrr = prrr
            st.session_state.frameworks_generated = True
            st.rerun()
    
    # Generate Course Modules
    with col3:
        if st.button("📚 Generate Modules", type="primary", disabled=st.session_state.modules_generated):
            # Generate modules based on course type
            if "data science" in course_title.lower():
                module_titles = [
                    "Data Science Foundations", "Data Collection & Cleaning", "Exploratory Analysis",
                    "Statistical Modeling", "Machine Learning Basics", "Data Visualization", 
                    "Ethics & Communication", "Capstone Project"
                ][:weeks]
            elif "artificial intelligence" in course_title.lower() or "ai" in course_title.lower() or "machine learning" in course_title.lower():
                module_titles = [
                    "AI Fundamentals & History", "Machine Learning Types & Applications", "Neural Networks & Deep Learning",
                    "AI in Healthcare & Medicine", "AI in Business & Finance", "Natural Language Processing",
                    "AI Ethics & Bias", "Future of AI & Career Pathways"
                ][:weeks]
            elif "business" in course_title.lower():
                module_titles = [
                    "Business Fundamentals", "Market Analysis", "Financial Planning",
                    "Operations Management", "Leadership Skills", "Digital Strategy",
                    "Ethics & Responsibility", "Business Plan Development"
                ][:weeks]
            else:
                module_titles = [
                    f"{course_domain} Foundations", f"Core {course_title} Concepts", 
                    "Practical Applications", "Analysis & Critical Thinking",
                    "Advanced Topics", "Real-World Cases", 
                    "Professional Practice", "Synthesis & Future Directions"
                ][:weeks]
            
            modules = []
            for i, title in enumerate(module_titles):
                modules.append({
                    "title": title,
                    "objectives": f"Students will master key concepts in {title.lower()} and apply them practically",
                    "activities": f"Interactive sessions, hands-on exercises, case studies related to {title.lower()}",
                    "assessment": f"Formative quiz, practical project, peer discussion on {title.lower()}"
                })
            
            st.session_state.modules = modules
            st.session_state.modules_generated = True
            st.rerun()

else:
    st.info("💡 Fill in course title, description, and at least 2 goals to activate AI generation")

# ===== DISPLAY GENERATED CONTENT =====
if st.session_state.objectives_generated:
    st.subheader("✅ Generated Learning Objectives")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Terminal Learning Objectives:**")
        st.write(st.session_state.tlo)
    with col2:
        st.write("**Enabling Learning Objectives:**")  
        st.write(st.session_state.elo)

if st.session_state.frameworks_generated:
    st.subheader("✅ Generated KDKA & PRRR Frameworks")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**KDKA Framework:**")
        kdka = st.session_state.kdka
        for k, v in kdka.items():
            st.write(f"• **{k.title()}:** {v}")
    with col2:
        st.write("**PRRR Framework:**")
        prrr = st.session_state.prrr
        for k, v in prrr.items():
            st.write(f"• **{k.title()}:** {v}")

if st.session_state.modules_generated:
    st.subheader("✅ Generated Course Modules")
    for i, module in enumerate(st.session_state.modules):
        with st.expander(f"Module {i+1}: {module['title']}"):
            st.write(f"**Objectives:** {module['objectives']}")
            st.write(f"**Activities:** {module['activities']}")
            st.write(f"**Assessment:** {module['assessment']}")

# ===== FINAL SYLLABUS GENERATION =====
if all([st.session_state.objectives_generated, st.session_state.frameworks_generated, st.session_state.modules_generated]):
    st.header("🎓 Generate Complete Syllabus")
    
    if st.button("📄 Create Final Syllabus", type="primary"):
        syllabus = f"""# {course_title}

## Course Description
{course_desc}

## Course Goals
{chr(10).join([f"• {goal}" for goal in goals])}

## Learning Outcomes
**Terminal Learning Objectives:** {st.session_state.tlo}

**Enabling Learning Objectives:**
{st.session_state.elo}

## Teaching & Learning Framework
This course integrates KDKA and PRRR pedagogical models:
- **Knowledge:** {st.session_state.kdka['knowledge']}
- **Delivery:** {st.session_state.kdka['delivery']}  
- **Context:** {st.session_state.kdka['context']}
- **Assessment:** {st.session_state.kdka['assessment']}

## Course Modules
"""
        for i, module in enumerate(st.session_state.modules):
            syllabus += f"""
### Module {i+1}: {module['title']}
- **Learning Objectives:** {module['objectives']}
- **Learning Activities:** {module['activities']}
- **Assessment:** {module['assessment']}
"""
        
        # Export options
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Download Syllabus", syllabus, f"{course_title}_syllabus.md")
        
        with col2:
            # JSON export for n8n
            course_data = {
                "course_title": course_title,
                "course_description": course_desc,
                "course_level": course_level,
                "goals": goals,
                "tlo": st.session_state.tlo,
                "elo": st.session_state.elo,
                "kdka": st.session_state.kdka,
                "prrr": st.session_state.prrr,
                "modules": st.session_state.modules,
                "generated_date": datetime.now().isoformat()
            }
            st.download_button("📊 Export JSON (for n8n)", json.dumps(course_data, indent=2), f"{course_title}_data.json")
        
        st.success("🎉 Complete KDKA/PRRR-compliant syllabus generated!")
        st.code(syllabus, language="markdown")

# Reset button
if st.button("🔄 Start Over"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()