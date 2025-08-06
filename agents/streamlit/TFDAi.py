import streamlit as st
import json

st.set_page_config(page_title="TFDAi - Technical & Functional Design Agent", layout="wide")
st.title("🛠️ TFDAi - Technical & Functional Design Agent")
st.markdown("This agent translates pedagogical content into deployable technical specifications for various LMS platforms and delivery methods.")

# Step 1: Course Context Input
st.header("Step 1: Course Context")
course_title = st.text_input("Course Title")
module_title = st.text_input("Module/Unit Title")
target_lms = st.selectbox("Target LMS Platform", [
    "Canvas", "Moodle", "Blackboard", "D2L Brightspace", "Google Classroom", 
    "Custom LMS", "SCORM-Compatible Platform", "Standalone Web App"
])

# Step 2: Content Assets Mapping
st.header("Step 2: Content Assets & Features Mapping")
st.markdown("Map your instructional content to specific LMS features and delivery methods:")

content_mapping = {}

# Video Content
with st.expander("📹 Video Content"):
    has_video = st.checkbox("Course includes video content")
    if has_video:
        video_type = st.multiselect("Video Types", ["Lecture recordings", "Demonstrations", "Student presentations", "Interactive videos"])
        video_hosting = st.selectbox("Video Hosting", ["LMS native", "YouTube", "Vimeo", "Kaltura", "Panopto"])
        video_features = st.multiselect("Required Features", ["Captions", "Transcripts", "Chapter markers", "Interactive elements", "Analytics"])
        content_mapping["video"] = {"types": video_type, "hosting": video_hosting, "features": video_features}

# Assessment Tools
with st.expander("📝 Assessment & Activities"):
    quiz_types = st.multiselect("Quiz/Assessment Types", ["Multiple choice", "Essay", "Discussion forums", "Peer review", "Portfolio", "Project submissions"])
    interactive_elements = st.multiselect("Interactive Elements", ["H5P", "Simulations", "Virtual labs", "Gamification", "Branching scenarios"])
    grading_features = st.multiselect("Grading Features", ["Rubrics", "Auto-grading", "Peer assessment", "Group grading", "Grade passback"])
    content_mapping["assessment"] = {"quiz_types": quiz_types, "interactive": interactive_elements, "grading": grading_features}

# Reading Materials
with st.expander("📚 Reading & Resources"):
    reading_formats = st.multiselect("Reading Material Formats", ["PDF documents", "Web links", "E-books", "Interactive texts", "Case studies"])
    resource_organization = st.selectbox("Resource Organization", ["Module-based folders", "Resource library", "Tagged collections", "Sequential pathway"])
    content_mapping["reading"] = {"formats": reading_formats, "organization": resource_organization}

# Communication Tools
with st.expander("💬 Communication & Collaboration"):
    communication_tools = st.multiselect("Communication Features", ["Discussion forums", "Chat/messaging", "Video conferencing", "Announcement system", "Email integration"])
    collaboration_features = st.multiselect("Collaboration Features", ["Group workspaces", "Shared documents", "Wiki", "Blogs", "Peer review system"])
    content_mapping["communication"] = {"tools": communication_tools, "collaboration": collaboration_features}

# Step 3: Technical Specifications
st.header("Step 3: Technical Specifications")

# SCORM/xAPI Configuration
with st.expander("📦 SCORM/xAPI Configuration"):
    packaging_standard = st.selectbox("Packaging Standard", ["SCORM 1.2", "SCORM 2004", "xAPI (Tin Can)", "cmi5", "QTI", "Custom API"])
    tracking_requirements = st.multiselect("Tracking Requirements", [
        "Completion tracking", "Progress tracking", "Time tracking", "Score tracking", 
        "Detailed analytics", "Learning path tracking"
    ])
    content_mapping["packaging"] = {"standard": packaging_standard, "tracking": tracking_requirements}

# Integration Requirements
with st.expander("🔗 Integration Requirements"):
    external_integrations = st.multiselect("External Tool Integrations", [
        "Google Workspace", "Microsoft 365", "Zoom", "Teams", "Slack", 
        "Library systems", "Student information system", "Plagiarism detection"
    ])
    api_requirements = st.multiselect("API Requirements", ["LTI 1.3", "REST API", "GraphQL", "Webhook support", "SSO integration"])
    content_mapping["integrations"] = {"external": external_integrations, "apis": api_requirements}

# Step 4: UI/UX Design Specifications
st.header("Step 4: UI/UX Design Specifications")

# Accessibility Requirements
accessibility_features = st.multiselect("Accessibility Features (WCAG 2.1)", [
    "Screen reader compatibility", "Keyboard navigation", "High contrast mode", 
    "Font size adjustment", "Closed captions", "Alt text for images", "Focus indicators"
])

# Mobile Responsiveness
mobile_requirements = st.multiselect("Mobile Requirements", [
    "Responsive design", "Mobile app compatibility", "Offline access", 
    "Touch-friendly interface", "Mobile-optimized video"
])

# User Experience Features
ux_features = st.multiselect("User Experience Features", [
    "Progress indicators", "Breadcrumb navigation", "Search functionality", 
    "Personalized dashboard", "Learning analytics dashboard", "Notification system"
])

content_mapping["ui_ux"] = {
    "accessibility": accessibility_features,
    "mobile": mobile_requirements,
    "ux": ux_features
}

# Step 5: Generate Technical Design Report
if st.button("🔧 Generate Technical Design Report"):
    if not course_title or not target_lms:
        st.error("Please fill in course title and target LMS")
    else:
        report = f"""
# TFDAi Technical & Functional Design Report

**Course:** {course_title}
**Module:** {module_title}
**Target Platform:** {target_lms}
**Generated:** {st.session_state.get('report_date', 'Today')}

## Executive Summary
This report outlines the technical specifications and functional requirements for deploying the course content on {target_lms}.

## Content Asset Mapping

### Video Content
"""
        if content_mapping.get("video"):
            video = content_mapping["video"]
            report += f"""
- **Types:** {', '.join(video.get('types', []))}
- **Hosting Platform:** {video.get('hosting', 'Not specified')}
- **Required Features:** {', '.join(video.get('features', []))}
"""
        else:
            report += "- No video content specified\n"

        report += f"""
### Assessment & Activities
"""
        if content_mapping.get("assessment"):
            assessment = content_mapping["assessment"]
            report += f"""
- **Quiz Types:** {', '.join(assessment.get('quiz_types', []))}
- **Interactive Elements:** {', '.join(assessment.get('interactive', []))}
- **Grading Features:** {', '.join(assessment.get('grading', []))}
"""

        report += f"""
### Reading Materials & Resources
"""
        if content_mapping.get("reading"):
            reading = content_mapping["reading"]
            report += f"""
- **Formats:** {', '.join(reading.get('formats', []))}
- **Organization:** {reading.get('organization', 'Not specified')}
"""

        report += f"""
## Technical Implementation

### Packaging & Standards
"""
        if content_mapping.get("packaging"):
            packaging = content_mapping["packaging"]
            report += f"""
- **Standard:** {packaging.get('standard', 'Not specified')}
- **Tracking:** {', '.join(packaging.get('tracking', []))}
"""

        report += f"""
### Integration Requirements
"""
        if content_mapping.get("integrations"):
            integrations = content_mapping["integrations"]
            report += f"""
- **External Tools:** {', '.join(integrations.get('external', []))}
- **API Requirements:** {', '.join(integrations.get('apis', []))}
"""

        report += f"""
## UI/UX Specifications

### Accessibility (WCAG 2.1 Compliance)
{chr(10).join([f"- {feature}" for feature in accessibility_features])}

### Mobile Responsiveness
{chr(10).join([f"- {req}" for req in mobile_requirements])}

### User Experience Features
{chr(10).join([f"- {feature}" for feature in ux_features])}

## Implementation Recommendations

### Phase 1: Core Setup
1. Configure {target_lms} course shell
2. Set up user roles and permissions
3. Implement basic navigation structure

### Phase 2: Content Deployment
1. Upload and organize content assets
2. Configure assessment tools and rubrics
3. Set up communication channels

### Phase 3: Integration & Testing
1. Implement external tool integrations
2. Configure SCORM/xAPI tracking
3. Conduct accessibility and usability testing

### Phase 4: Launch & Optimization
1. Deploy to production environment
2. Train instructors and support staff
3. Monitor performance and user feedback

## Quality Assurance Checklist

- [ ] All content assets properly uploaded and linked
- [ ] Assessment tools configured and tested
- [ ] Accessibility standards verified (WCAG 2.1)
- [ ] Mobile responsiveness tested across devices
- [ ] Integration points validated
- [ ] Performance benchmarks met
- [ ] User acceptance testing completed

## Support Documentation Required

1. Instructor Guide for {target_lms}
2. Student Orientation Materials
3. Technical Troubleshooting Guide
4. Integration API Documentation
5. Accessibility Compliance Report

---

*This technical design report should be reviewed by the institutional IT team and instructional designers before implementation.*
"""

        st.download_button("📥 Download Technical Design Report", report, file_name="TFDAi_Technical_Design_Report.md")
        st.code(report, language="markdown")

# Step 6: LMS-Specific Configuration
st.header("Step 6: LMS-Specific Configuration Notes")

lms_configs = {
    "Canvas": {
        "modules": "Use Canvas Modules for content organization",
        "grades": "Configure Canvas Gradebook with weighted categories",
        "discussions": "Set up Canvas Discussion Forums with rubrics",
        "files": "Organize in Canvas Files with folder structure"
    },
    "Moodle": {
        "activities": "Configure Moodle Activities and Resources",
        "gradebook": "Set up Moodle Gradebook with categories",
        "forums": "Create Moodle Forum activities with ratings",
        "files": "Use Moodle File API for resource management"
    },
    "Blackboard": {
        "content": "Use Blackboard Content Areas for organization",
        "gradecenter": "Configure Grade Center columns and categories",
        "discussions": "Set up Discussion Board tools",
        "files": "Manage through Course Files repository"
    }
}

if target_lms in lms_configs:
    st.subheader(f"{target_lms} Specific Recommendations:")
    config = lms_configs[target_lms]
    for key, value in config.items():
        st.write(f"• **{key.title()}:** {value}")

# Step 7: Export Configuration
st.header("Step 7: Export Configuration")
if st.button("📄 Export Full Configuration JSON"):
    full_config = {
        "course_info": {
            "title": course_title,
            "module": module_title,
            "target_lms": target_lms
        },
        "content_mapping": content_mapping,
        "ui_ux": {
            "accessibility": accessibility_features,
            "mobile": mobile_requirements,
            "ux": ux_features
        },
        "lms_specific": lms_configs.get(target_lms, {})
    }
    
    config_json = json.dumps(full_config, indent=2)
    st.download_button("📥 Download Configuration JSON", config_json, file_name="TFDAi_configuration.json", mime="application/json")
    st.json(full_config)