import streamlit as st

st.set_page_config(page_title="EthosAi - Ethical Oversight Agent", layout="wide")
st.title("⚖️ EthosAi - Ethical Oversight Agent")
st.markdown("This agent ensures ethical alignment of all instructional materials and decisions in the course design process, guided by academic integrity, inclusiveness, transparency, and fairness.")

# Step 1: Course or Module Overview
st.header("Step 1: Course Context")
course_title = st.text_input("Course Title")
module_or_doc = st.text_input("Module or Document Title")
ethical_framework = st.selectbox("Primary Ethical Framework to Apply", [
    "AI Ethics in Education",
    "Universal Design for Learning (UDL)",
    "Equity and Inclusion",
    "Academic Integrity Principles",
    "Transparency in Assessment"
])

# Step 2: Ethical Criteria Checklist
st.header("Step 2: Ethical Design Checklist")
checklist = {
    "Learner privacy protected": st.checkbox("Learner privacy and data ethics ensured"),
    "Inclusive language used": st.checkbox("Inclusive and culturally sensitive language used"),
    "No implicit bias present": st.checkbox("No evidence of stereotyping or implicit bias"),
    "Assessment is fair and transparent": st.checkbox("Assessment rubrics and grading are clear and fair"),
    "Accessibility maintained": st.checkbox("All materials accessible to students with disabilities"),
    "AI or automation tools disclosed": st.checkbox("Use of AI tools clearly disclosed and explained")
}

custom_flags = st.text_area("Additional Ethical Flags, Notes, or Reviewer Comments")

# Step 3: Generate Ethical Audit
if st.button("🔎 Run Ethical Audit"):
    report = f"""
# ETHOSAi Ethical Audit Report

**Course:** {course_title}
**Module/Document:** {module_or_doc}
**Framework Applied:** {ethical_framework}

## Ethical Criteria Summary:
"""
    for item, checked in checklist.items():
        status = "✔️ Yes" if checked else "❌ Needs Attention"
        report += f"- {item}: {status}\n"

    report += f"\n## Additional Notes\n{custom_flags if custom_flags else 'None'}\n"

    st.download_button("📥 Download Audit Report", report, file_name="EthosAi_Ethical_Audit.md")
    st.text_area("Audit Summary Preview", value=report, height=300)