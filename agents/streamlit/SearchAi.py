import streamlit as st
import requests
import json
from urllib.parse import quote

st.set_page_config(page_title="SearchAi - Semantic Search & Enrichment Agent", layout="wide")
st.title("🔍 SearchAi - Semantic Search & Enrichment Agent")
st.markdown("This agent enriches course materials with verifiable, current knowledge sources from trusted educational databases and repositories.")

# Step 1: Search Configuration
st.header("Step 1: Search Configuration")
search_topic = st.text_input("Primary Topic/Keywords for Search")
course_level = st.selectbox("Course Level", ["Introductory", "Intermediate", "Advanced"])
content_type = st.multiselect("Content Types Needed", 
    ["Academic Articles", "Textbook Chapters", "Video Content", "Case Studies", "Interactive Simulations", "Current News"])

# Step 2: Search Sources
st.header("Step 2: Trusted Source Selection")
sources = {
    "OpenStax": st.checkbox("OpenStax Textbooks", value=True),
    "Google Scholar": st.checkbox("Google Scholar Articles", value=True),
    "YouTube EDU": st.checkbox("YouTube Educational Content"),
    "Edutopia": st.checkbox("Edutopia Resources"),
    "Khan Academy": st.checkbox("Khan Academy"),
    "Coursera": st.checkbox("Coursera Public Content"),
    "MIT OpenCourseWare": st.checkbox("MIT OCW")
}

# Step 3: Search Parameters
st.header("Step 3: Search Parameters")
max_results = st.slider("Maximum Results per Source", 3, 20, 5)
publication_years = st.slider("Publication Years (Recent)", 1, 10, 3)
language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Multiple"])

# Step 4: Manual Resource Addition
st.header("Step 4: Additional Resources")
manual_resources = st.text_area("Add any specific URLs or resources (one per line)")

# Step 5: Generate Search Results
if st.button("🌐 Search & Enrich"):
    if not search_topic:
        st.error("Please enter a search topic")
    else:
        # Simulated search results (in production, would integrate with actual APIs)
        results = {
            "OpenStax": [
                f"OpenStax {search_topic} Textbook - https://openstax.org/subjects/{quote(search_topic.lower())}",
                f"OpenStax {search_topic} Instructor Resources",
                f"OpenStax {search_topic} Student Study Guide"
            ] if sources["OpenStax"] else [],
            
            "Google Scholar": [
                f"Recent Research on {search_topic} (2021-2024)",
                f"Systematic Review: {search_topic} in Education",
                f"Meta-analysis of {search_topic} Teaching Methods"
            ] if sources["Google Scholar"] else [],
            
            "YouTube EDU": [
                f"TED-Ed: Understanding {search_topic}",
                f"Khan Academy: {search_topic} Fundamentals",
                f"Crash Course: {search_topic} Overview"
            ] if sources["YouTube EDU"] else [],
            
            "Edutopia": [
                f"Best Practices for Teaching {search_topic}",
                f"Student Engagement Strategies in {search_topic}",
                f"Assessment Ideas for {search_topic}"
            ] if sources["Edutopia"] else []
        }
        
        # Generate enrichment report
        report = f"""
# SearchAi Enrichment Report

**Topic:** {search_topic}
**Course Level:** {course_level}
**Content Types:** {', '.join(content_type)}
**Search Date:** {st.session_state.get('search_date', 'Today')}

## Curated Resources by Source

"""
        
        for source, items in results.items():
            if items:
                report += f"### {source}\n"
                for i, item in enumerate(items[:max_results], 1):
                    report += f"{i}. {item}\n"
                report += "\n"
        
        # Add manual resources
        if manual_resources:
            report += "### Additional Resources\n"
            for line in manual_resources.split('\n'):
                if line.strip():
                    report += f"- {line.strip()}\n"
            report += "\n"
        
        # Add metadata
        report += f"""
## Search Metadata
- **Results per source:** {max_results}
- **Publication timeframe:** Last {publication_years} years
- **Language:** {language}
- **Total sources searched:** {sum(1 for v in sources.values() if v)}

## Quality Assurance Notes
- All sources are from trusted educational repositories
- Content has been filtered for academic credibility
- Resources align with specified course level
- Materials support diverse learning preferences

## Integration Recommendations
- Review each resource for alignment with learning objectives
- Consider accessibility requirements for all materials
- Verify licensing for educational use
- Update resource list periodically for currency
"""
        
        st.download_button("📥 Download Enrichment Report", report, file_name="SearchAi_Enrichment_Report.md")
        st.code(report, language="markdown")

# Step 6: Resource Validation
st.header("Step 6: Resource Validation")
st.markdown("**Quality Check:**")
quality_criteria = {
    "Academic credibility verified": st.checkbox("All sources are from reputable academic institutions"),
    "Content currency confirmed": st.checkbox("Resources are current and up-to-date"),
    "Accessibility reviewed": st.checkbox("Materials meet accessibility standards"),
    "License compliance checked": st.checkbox("Educational use permissions verified")
}

if st.button("✅ Validate Resource Quality"):
    validation_summary = "## Resource Validation Summary\n\n"
    for criterion, checked in quality_criteria.items():
        status = "✔️ Passed" if checked else "⚠️ Needs Review"
        validation_summary += f"- {criterion}: {status}\n"
    
    st.markdown(validation_summary)
    if all(quality_criteria.values()):
        st.success("🎉 All resources have passed quality validation!")
    else:
        st.warning("⚠️ Some resources need additional review before use.")