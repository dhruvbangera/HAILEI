import streamlit as st
import textwrap

st.set_page_config(page_title="CAuthAi - Course Authoring Agent", layout="wide")
st.title("📚 CAuthAi - Course Authoring Agent")
st.markdown("This agent transforms instructional design data into full course modules using KDKA, PRRR, Bloom’s, and TILT. It collaborates with other HAILEI agents to generate complete instructional artifacts.")

# Step 1: Collect Module Metadata
st.header("Step 1: Module Overview")
module_title = st.text_input("Module Title")
tlo = st.text_area("Terminal Learning Objective (TLO)")
elos = st.text_area("Enabling Learning Objectives (ELOs)")

# Step 2: Generate Activities using Templates
st.header("Step 2: Generate Activities (PRRR & TILT-Aligned)")
activity_type = st.selectbox("Select Activity Type", ["Discussion", "Reflection", "Case Analysis", "Hands-on", "Current Events", "Project"])
activity_description = st.text_area("Describe Activity Purpose and Instructions")
success_criteria = st.text_area("Criteria for Success (TILT)")

# Step 3: Lecture Notes & Lesson Outline
st.header("Step 3: Lecture Notes & Outline")
lecture_notes = st.text_area("Lecture Notes (Detailed) for This Module")
lesson_outline = st.text_area("Lesson Presentation Outline (Bullet Format)")

# Step 4: Generate Reading List
st.header("Step 4: Suggested Readings")
reading_topic = st.text_input("Topic for Recommended Readings")
suggested_readings = [
    f"1. 'OpenStax: {reading_topic}' – https://openstax.org",
    f"2. Peer-reviewed article on {reading_topic} via Google Scholar",
    f"3. Chapter from trusted textbooks in the domain (e.g., Springer, Pearson, Elsevier)"
]

# Step 5: SCORM Placeholder
st.header("Step 5: SCORM Package (Simulated Output)")
st.markdown("⬇️ When finalized, this will be converted to a SCORM-compliant module using SCORM packaging tools.")

if st.button("🧠 Generate Full Module Output"):
    output = f"""
# MODULE: {module_title}

## Terminal Objective
{tlo}

## Enabling Objectives
{elos}

## PRRR-Aligned Activity ({activity_type})
**Instructions:** {activity_description}
**TILT Criteria for Success:** {success_criteria}

## Lecture Notes
{textwrap.fill(lecture_notes, 90)}

## Lesson Presentation Outline
{textwrap.fill(lesson_outline, 90)}

## Recommended Readings
"""
    for read in suggested_readings:
        output += f"- {read}\n"

    output += """

## SCORM Output
[Placeholder: To be generated as .zip SCORM package via export tool]
"""

    st.download_button("📥 Download Full Module (Markdown)", output, file_name="module_output.md")
    st.code(output, language="markdown")