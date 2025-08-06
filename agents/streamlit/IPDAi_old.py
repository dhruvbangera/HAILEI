import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="IPDAi - AI Course Planning Agent", layout="wide")

st.title("🤖 IPDAi - AI-Powered Course Planning Agent")
st.markdown("**Ultra-streamlined workflow:** Just enter basic course info, and AI handles the rest!")

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
            if "data science" in course_title.lower():
                tlo = "Students will analyze datasets, evaluate statistical models, and create data-driven solutions for real-world problems."
                elo = "• Identify and clean data sources\n• Apply statistical analysis techniques\n• Create compelling visualizations\n• Build predictive models\n• Communicate findings effectively"
            elif "business" in course_title.lower():
                tlo = "Students will analyze business challenges, evaluate strategic options, and create comprehensive business solutions."
                elo = "• Analyze market opportunities\n• Evaluate financial performance\n• Develop strategic plans\n• Lead project teams\n• Present business recommendations"
            else:
                tlo = f"Students will analyze core concepts, evaluate applications, and create innovative solutions in {course_domain}."
                elo = f"• Master fundamental principles\n• Apply theoretical frameworks\n• Solve complex problems\n• Develop new approaches\n• Communicate professionally"
            
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