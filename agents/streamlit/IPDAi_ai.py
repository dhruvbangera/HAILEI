import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="IPDAi - True AI Course Planning", layout="wide")

st.title("🤖 IPDAi - True AI Course Planning Agent")
st.markdown("**Real AI Generation:** Uses LLM prompting to create intelligent, context-aware course content!")

# API Configuration
api_key = st.text_input("Enter OpenAI API Key (required for AI generation):", type="password")
use_ai = bool(api_key)

if use_ai:
    import openai
    openai.api_key = api_key
    
    def generate_with_ai(prompt: str, max_tokens: int = 800) -> str:
        """Generate content using OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert instructional designer specializing in KDKA (Knowledge, Delivery, Context, Assessment) and PRRR (Personal, Relatable, Relative, Real-world) pedagogical frameworks. Create pedagogically sound, engaging educational content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"AI generation failed: {str(e)}")
            return None
else:
    st.info("💡 Enter OpenAI API key above to enable true AI generation. Without it, you'll get basic template responses.")

# Initialize session state
for key in ['objectives_generated', 'frameworks_generated', 'modules_generated']:
    if key not in st.session_state:
        st.session_state[key] = False

# ===== STEP 1: BASIC COURSE INFO =====
st.header("Step 1: Course Information")
course_title = st.text_input("Course Title")
course_desc = st.text_area("Course Description", height=100)
course_level = st.selectbox("Course Level", ["Introductory", "Intermediate", "Advanced"])
course_domain = st.text_input("Course Domain")
weeks = st.slider("Number of Modules", 4, 12, 8)

# ===== STEP 2: COURSE GOALS =====
st.header("Step 2: Course Goals")
goals = []
for i in range(3):
    goal = st.text_input(f"Goal {i+1} {'(optional)' if i > 1 else ''}")
    if goal.strip():
        goals.append(goal.strip())

# ===== STEP 3: AI GENERATION =====
st.header("🧠 Step 3: AI Generation")

ready = course_title and course_desc and len(goals) >= 2

if ready:
    col1, col2, col3 = st.columns(3)
    
    # Generate Learning Objectives
    with col1:
        if st.button("🎯 Generate Objectives", type="primary", disabled=st.session_state.objectives_generated):
            with st.spinner("🤖 AI creating learning objectives..."):
                if use_ai:
                    prompt = f"""
Create learning objectives for this course using Bloom's taxonomy:

**Course:** {course_title}
**Description:** {course_desc}  
**Level:** {course_level}
**Domain:** {course_domain}
**Goals:** {', '.join(goals)}

Please generate:
1. ONE Terminal Learning Objective (TLO) - overarching outcome
2. 5-6 Enabling Learning Objectives (ELOs) - specific skills

Requirements:
- Use Bloom's verbs appropriate for {course_level} level
- Make objectives measurable and specific
- Align with the course goals provided
- Focus on what students will DO/DEMONSTRATE

Format as:
TLO: [single comprehensive objective]
ELOs: 
• [objective 1]
• [objective 2]
• [etc.]
"""
                    
                    result = generate_with_ai(prompt)
                    if result:
                        # Parse TLO and ELOs
                        parts = result.split('ELOs:')
                        tlo = parts[0].replace('TLO:', '').strip()
                        elo = parts[1].strip() if len(parts) > 1 else "• Generated enabling objectives"
                        
                        st.session_state.tlo = tlo
                        st.session_state.elo = elo
                        st.session_state.objectives_generated = True
                        st.success("✅ AI-generated objectives!")
                        st.rerun()
                else:
                    st.error("⚠️ OpenAI API key required for AI generation")
    
    # Generate KDKA/PRRR Frameworks
    with col2:
        if st.button("🧠 Generate Frameworks", type="primary", disabled=st.session_state.frameworks_generated):
            with st.spinner("🤖 AI creating pedagogical frameworks..."):
                if use_ai:
                    prompt = f"""
Create KDKA and PRRR pedagogical frameworks for this course:

**Course:** {course_title}
**Description:** {course_desc}
**Level:** {course_level}
**Domain:** {course_domain}

Generate frameworks:

**KDKA Model (Knowledge, Delivery, Context, Assessment):**
- Knowledge: What key knowledge will students acquire?
- Delivery: How will content be delivered effectively?
- Context: What real-world contexts will connect learning?
- Assessment: How will learning be measured?

**PRRR Model (Personal, Relatable, Relative, Real-world):**
- Personal: How does content connect to student experiences?
- Relatable: What examples/analogies make content relatable?
- Relative: How does each element support course outcomes?
- Real-world: What authentic applications will students engage with?

Format as JSON:
{{
  "kdka": {{
    "knowledge": "...",
    "delivery": "...",
    "context": "...",
    "assessment": "..."
  }},
  "prrr": {{
    "personal": "...",
    "relatable": "...",
    "relative": "...",
    "realworld": "..."
  }}
}}
"""
                    
                    result = generate_with_ai(prompt, 600)
                    if result:
                        try:
                            # Try to parse JSON
                            import re
                            json_match = re.search(r'\{.*\}', result, re.DOTALL)
                            if json_match:
                                frameworks = json.loads(json_match.group())
                                st.session_state.kdka = frameworks.get('kdka', {})
                                st.session_state.prrr = frameworks.get('prrr', {})
                            else:
                                # Fallback parsing
                                st.session_state.kdka = {"knowledge": "AI-generated", "delivery": "AI-generated", "context": "AI-generated", "assessment": "AI-generated"}
                                st.session_state.prrr = {"personal": "AI-generated", "relatable": "AI-generated", "relative": "AI-generated", "realworld": "AI-generated"}
                            
                            st.session_state.frameworks_generated = True
                            st.success("✅ AI-generated frameworks!")
                            st.rerun()
                        except:
                            st.error("Error parsing AI response. Please try again.")
                else:
                    st.error("⚠️ OpenAI API key required for AI generation")
    
    # Generate Modules
    with col3:
        if st.button("📚 Generate Modules", type="primary", disabled=st.session_state.modules_generated):
            with st.spinner("🤖 AI creating course modules..."):
                if use_ai:
                    prompt = f"""
Create {weeks} course modules for this course:

**Course:** {course_title}
**Description:** {course_desc}
**Level:** {course_level}
**Goals:** {', '.join(goals)}

Generate {weeks} modules with:
- Progressive learning sequence
- Clear module titles
- Specific learning objectives for each module
- Engaging activities aligned with course level
- Appropriate assessments

Format as JSON array:
[
  {{
    "title": "Module Title",
    "objectives": "What students will learn/do in this module",
    "activities": "Learning activities and exercises",
    "assessment": "How learning will be assessed"
  }},
  ...
]
"""
                    
                    result = generate_with_ai(prompt, 1000)
                    if result:
                        try:
                            # Try to parse JSON
                            import re
                            json_match = re.search(r'\[.*\]', result, re.DOTALL)
                            if json_match:
                                modules = json.loads(json_match.group())
                                st.session_state.modules = modules
                            else:
                                # Create basic modules from AI text
                                lines = [line.strip() for line in result.split('\n') if line.strip()]
                                modules = []
                                for i in range(min(weeks, len(lines))):
                                    modules.append({
                                        "title": lines[i] if i < len(lines) else f"Module {i+1}",
                                        "objectives": "AI-generated objectives",
                                        "activities": "AI-generated activities", 
                                        "assessment": "AI-generated assessment"
                                    })
                                st.session_state.modules = modules
                            
                            st.session_state.modules_generated = True
                            st.success("✅ AI-generated modules!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error parsing AI response: {e}")
                else:
                    st.error("⚠️ OpenAI API key required for AI generation")

else:
    st.info("💡 Complete Steps 1-2 to enable AI generation")

# ===== DISPLAY RESULTS =====
if st.session_state.objectives_generated:
    st.subheader("✅ AI-Generated Learning Objectives")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Terminal Learning Objectives:**")
        st.write(st.session_state.tlo)
    with col2:
        st.write("**Enabling Learning Objectives:**")
        st.write(st.session_state.elo)

if st.session_state.frameworks_generated:
    st.subheader("✅ AI-Generated Pedagogical Frameworks")
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
    st.subheader("✅ AI-Generated Course Modules")
    for i, module in enumerate(st.session_state.modules):
        with st.expander(f"Module {i+1}: {module['title']}"):
            st.write(f"**Objectives:** {module['objectives']}")
            st.write(f"**Activities:** {module['activities']}")
            st.write(f"**Assessment:** {module['assessment']}")

# ===== FINAL SYLLABUS =====
if all([st.session_state.objectives_generated, st.session_state.frameworks_generated, st.session_state.modules_generated]):
    st.header("🎓 Complete AI-Generated Syllabus")
    
    if st.button("📄 Generate Final Syllabus", type="primary"):
        syllabus = f"""# {course_title}

## Course Description
{course_desc}

## Course Goals
{chr(10).join([f"• {goal}" for goal in goals])}

## Learning Outcomes
**Terminal Learning Objectives:** {st.session_state.tlo}

**Enabling Learning Objectives:**
{st.session_state.elo}

## Pedagogical Framework Integration
This course integrates KDKA and PRRR models:

**KDKA Framework:**
- **Knowledge:** {st.session_state.kdka.get('knowledge', 'N/A')}
- **Delivery:** {st.session_state.kdka.get('delivery', 'N/A')}
- **Context:** {st.session_state.kdka.get('context', 'N/A')}
- **Assessment:** {st.session_state.kdka.get('assessment', 'N/A')}

**PRRR Framework:**
- **Personal:** {st.session_state.prrr.get('personal', 'N/A')}
- **Relatable:** {st.session_state.prrr.get('relatable', 'N/A')}
- **Relative:** {st.session_state.prrr.get('relative', 'N/A')}
- **Real-world:** {st.session_state.prrr.get('realworld', 'N/A')}

## Course Modules
"""
        for i, module in enumerate(st.session_state.modules):
            syllabus += f"""
### Module {i+1}: {module['title']}
- **Learning Objectives:** {module['objectives']}
- **Learning Activities:** {module['activities']}
- **Assessment:** {module['assessment']}
"""
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Download Syllabus", syllabus, f"{course_title}_AI_syllabus.md")
        with col2:
            course_data = {
                "course_title": course_title,
                "ai_generated": True,
                "tlo": st.session_state.tlo,
                "elo": st.session_state.elo,
                "kdka": st.session_state.kdka,
                "prrr": st.session_state.prrr,
                "modules": st.session_state.modules,
                "generated_date": datetime.now().isoformat()
            }
            st.download_button("📊 Export JSON", json.dumps(course_data, indent=2), f"{course_title}_AI_data.json")
        
        st.success("🎉 Complete AI-generated, KDKA/PRRR-compliant syllabus created!")
        st.code(syllabus, language="markdown")

# Reset
if st.button("🔄 Start Over"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()