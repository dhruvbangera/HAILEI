import streamlit as st
import subprocess
import sys
import os

st.set_page_config(
    page_title="HAILEI Agent Dashboard", 
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 HAILEI Instructional Design Agents")
st.markdown("Welcome to the HAILEI system - your AI-powered instructional design workflow")

# Agent descriptions
agents = {
    "IPDAi": {
        "name": "Instructional Planning & Design Agent", 
        "icon": "📘",
        "description": "Creates course structure, learning objectives, and syllabi using KDKA and PRRR frameworks",
        "file": "IPDAi.py"
    },
    "CAuthAi": {
        "name": "Course Authoring Agent",
        "icon": "📚", 
        "description": "Generates learning activities, lecture notes, and SCORM-ready content",
        "file": "CAuthAi.py"
    },
    "TFDAi": {
        "name": "Technical & Functional Design Agent",
        "icon": "🛠️",
        "description": "Maps content to LMS platforms and creates technical specifications", 
        "file": "TFDAi.py"
    },
    "EditorAi": {
        "name": "Content Review & Enhancement Agent",
        "icon": "✏️",
        "description": "Reviews content for clarity, accessibility, and Bloom's taxonomy alignment",
        "file": "EditorAi.py"
    },
    "EthosAi": {
        "name": "Ethical Oversight Agent", 
        "icon": "⚖️",
        "description": "Ensures ethical compliance, inclusivity, and academic integrity",
        "file": "EthosAi.py"
    },
    "SearchAi": {
        "name": "Semantic Search & Enrichment Agent",
        "icon": "🔍", 
        "description": "Enriches courses with verified educational resources and current knowledge",
        "file": "SearchAi.py"
    }
}

# Workflow visualization
st.header("🔄 HAILEI Workflow")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📋 Planning Phase")
    st.markdown("1. **IPDAi** - Course planning")
    st.markdown("2. **SearchAi** - Resource gathering")

with col2:
    st.markdown("### 🛠️ Development Phase") 
    st.markdown("3. **CAuthAi** - Content creation")
    st.markdown("4. **TFDAi** - Technical design")

with col3:
    st.markdown("### ✅ Review Phase")
    st.markdown("5. **EditorAi** - Content review")
    st.markdown("6. **EthosAi** - Ethical validation")

st.divider()

# Agent grid
st.header("🚀 Launch Agents")
st.markdown("Click on any agent below to open it in a new browser tab:")

# Create agent grid
cols = st.columns(3)
for i, (agent_id, agent_info) in enumerate(agents.items()):
    with cols[i % 3]:
        with st.container():
            st.markdown(f"### {agent_info['icon']} {agent_id}")
            st.markdown(f"**{agent_info['name']}**")
            st.markdown(agent_info['description'])
            
            # Launch button
            if st.button(f"Launch {agent_id}", key=f"launch_{agent_id}"):
                st.markdown(f"""
                <script>
                window.open('http://localhost:8501', '_blank');
                </script>
                """, unsafe_allow_html=True)
                st.info(f"To run {agent_id} separately, use: `streamlit run {agent_info['file']}`")

st.divider()

# System status
st.header("📊 System Status")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Available Agents", "6", "")
    
with col2:
    st.metric("Frameworks Integrated", "4", "KDKA, PRRR, Bloom's, TILT")
    
with col3:
    st.metric("Platform Support", "7+", "Canvas, Moodle, etc.")

# Quick start guide
st.header("🎯 Quick Start Guide")

with st.expander("🆕 New to HAILEI?"):
    st.markdown("""
    ### Getting Started:
    1. **Start with IPDAi** - Plan your course structure and objectives
    2. **Use SearchAi** - Gather relevant educational resources  
    3. **Run CAuthAi** - Create your content and activities
    4. **Configure TFDAi** - Set up technical specifications for your LMS
    5. **Review with EditorAi** - Enhance content quality and accessibility
    6. **Validate with EthosAi** - Ensure ethical compliance
    
    ### Best Practices:
    - Work through agents sequentially for best results
    - Save outputs from each agent to build comprehensive course materials
    - Use the n8n workflow for automated agent orchestration
    """)

with st.expander("⚙️ Technical Setup"):
    st.markdown("""
    ### Prerequisites:
    - Python 3.8+
    - Streamlit installed (`pip install streamlit`)
    - All dependencies from requirements.txt
    
    ### Running Individual Agents:
    ```bash
    cd agents/streamlit
    streamlit run IPDAi.py
    ```
    
    ### Running n8n Workflow:
    1. Import `workflows/n8n/HAILEI_n8n_workflow.json`
    2. Configure OpenAI API keys
    3. Set up webhook triggers
    """)

# Footer
st.divider()
st.markdown("**HAILEI** - Transforming instructional design through intelligent agent collaboration")
st.markdown("Built with pedagogical frameworks: KDKA • PRRR • Bloom's Taxonomy • TILT")