import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))


import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from app.styles import inject_css
from core.parser.resume_parser import extract_text_from_pdf
from core.parser.job_parser import parse_job_description
from core.scoring.ats_scorer import calculate_ats_score
from core.generators.feedback_generator import generate_feedback
from core.generators.resume_rewriter import generate_resume_bullets
from core.generators.cover_letter_generator import generate_cover_letter
from core.generators.linkedin_message_generator import generate_linkedin_message
from core.generators.report_generator import generate_text_report
from database.db_manager import init_db, save_analysis, get_analysis_history

# Initialize database on app startup
init_db()

st.set_page_config(
    page_title="AI Resume & Job Match Analyzer",
    page_icon="🧠",
    layout="wide",
)

inject_css()

# Sidebar layout
with st.sidebar:
    st.markdown(
        """
        <div class='sidebar-brand'>
            <div class='sidebar-icon'>✨</div>
            <div>
                <div class='sidebar-title-text'>AI Match</div>
                <div class='sidebar-subtitle'>Analyzer</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='workflow-section'>
            <div class='workflow-label'>Workflow</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='workflow-item'>
            <div class='workflow-dot'>1</div>
            <span>Upload Resume</span>
        </div>
        <div class='workflow-item'>
            <div class='workflow-dot'>2</div>
            <span>Paste Job Description</span>
        </div>
        <div class='workflow-item'>
            <div class='workflow-dot'>3</div>
            <span>Run Analysis</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='workflow-section'>
            <div class='workflow-label'>Recent History</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    history = get_analysis_history(limit=4)
    if history:
        for analysis in history:
            st.markdown(
                f"""
                <div class='recent-history-card'>
                    <strong>{analysis['resume_filename']}</strong><br>
                    ATS: {analysis['ats_score']:.0f}% • Skills: {analysis['skill_match_percentage']:.0f}%
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class='recent-history-card'>
                No recent analyses yet.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='privacy-card'>
            🔒 All data saved locally in SQLite. Never shared or stored remotely.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Top bar
st.markdown(
    """
    <div class='page-header'>
        <div class='small-badge'>🤖 AI Powered</div>
        <div class='page-title'>Resume & Job Match Analyzer</div>
        <div class='page-subtitle'>Upload your resume and paste a job description to get ATS scores, skill analysis, and recruiter feedback in seconds.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Main input card
with st.container():
    st.markdown(
        """
        <div class='analysis-card'>
            <div class='card-title'>Start Your Analysis</div>
            <div class='card-note'>Upload your resume PDF and paste the job description to receive a comprehensive match report.</div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type="pdf",
        help="Choose a text-based resume for the best results.",
        key="input_resume",
    )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    job_desc = st.text_area(
        "Job Description",
        placeholder="Paste the full job description here...",
        height=240,
        key="input_job_desc",
    )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    analyze_clicked = st.button("Analyze Your Match", use_container_width=True)

    st.markdown(
        """
        <div class='feature-chip-row'>
            <span class='feature-chip'>🎯 ATS Scoring</span>
            <span class='feature-chip'>🔍 Skill Matching</span>
            <span class='feature-chip'>🧠 Semantic Analysis</span>
            <span class='feature-chip'>📝 Recruiter Feedback</span>
            <span class='feature-chip'>📄 Report Download</span>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Result container
result_container = st.container()

if analyze_clicked:
    if not uploaded_file:
        st.error("Please upload a resume PDF.")
    elif not job_desc.strip():
        st.error("Please enter a job description.")
    else:
        try:
            resume_data = extract_text_from_pdf(uploaded_file)
            job_data = parse_job_description(job_desc)
            ats_results = calculate_ats_score(resume_data['raw_text'], job_data['raw_text'])
            feedback = generate_feedback(ats_results)
            resume_bullets = generate_resume_bullets(resume_data['raw_text'], job_data['raw_text'], ats_results)
            cover_letter = generate_cover_letter(resume_data['raw_text'], job_data['raw_text'], ats_results)
            linkedin_message = generate_linkedin_message(ats_results)
            report_content = generate_text_report(
                resume_metrics=resume_data,
                job_metrics=job_data,
                ats_result=ats_results,
                feedback=feedback,
                resume_bullets=resume_bullets,
                cover_letter=cover_letter,
                linkedin_message=linkedin_message,
            )

            with result_container:
                st.markdown(
                    """
                    <div class='result-section'>
                        <div class='section-title'>Analysis Results</div>
                        <div class='section-note'>Here's your complete resume-job match intelligence and actionable insights.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="large")
                with kpi1:
                    st.metric("ATS Score", f"{ats_results['ats_score']:.1f}%")
                with kpi2:
                    st.metric("Skill Match", f"{ats_results['skill_match_percentage']:.1f}%")
                with kpi3:
                    st.metric("Semantic Score", f"{ats_results['semantic_score']:.1f}%")
                with kpi4:
                    st.metric("Completeness", f"{ats_results['completeness_score']:.1f}%")

                st.markdown(
                    """
                    <div class='result-section'>
                        <div class='section-title'>Skill Match Analysis</div>
                        <div class='section-note'>Review your matched and missing skills relative to the job description.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                skill_left, skill_right = st.columns(2, gap="large")
                with skill_left:
                    st.markdown("**✓ Matched Skills**")
                    if ats_results['matched_skills']:
                        matched_html = "".join([f"<span class='chip-pill matched'>{skill}</span>" for skill in ats_results['matched_skills']])
                        st.markdown(matched_html, unsafe_allow_html=True)
                    else:
                        st.write("No matched skills found.")

                with skill_right:
                    st.markdown("**✗ Missing Skills**")
                    if ats_results['missing_skills']:
                        missing_html = "".join([f"<span class='chip-pill missing'>{skill}</span>" for skill in ats_results['missing_skills']])
                        st.markdown(missing_html, unsafe_allow_html=True)
                    else:
                        st.write("No major skill gaps detected.")

                st.markdown(
                    """
                    <div class='result-section'>
                        <div class='section-title'>Recruiter Insights</div>
                        <div class='section-note'>Strategic feedback to improve your application and stand out to recruiters.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                insight_left, insight_right = st.columns(2, gap="large")
                with insight_left:
                    with st.expander("💪 Your Strengths"):
                        for strength in feedback['strengths']:
                            st.write(f"• {strength}")
                    with st.expander("⚠️ Areas to Address"):
                        for weakness in feedback['weaknesses']:
                            st.write(f"• {weakness}")
                with insight_right:
                    with st.expander("✅ Recommended Improvements"):
                        for i, suggestion in enumerate(feedback['suggestions'], 1):
                            st.write(f"{i}. {suggestion}")
                    with st.expander("📝 Rewritten Bullets"):
                        for i, bullet in enumerate(resume_bullets, 1):
                            st.write(f"{i}. {bullet}")

                st.markdown(
                    """
                    <div class='result-section'>
                        <div class='section-title'>Application Materials Ready</div>
                        <div class='section-note'>Professionally drafted cover letter, LinkedIn message, and comprehensive report.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                tab1, tab2, tab3 = st.tabs(["📄 Cover Letter", "💼 LinkedIn Message", "📊 Full Report"])
                with tab1:
                    st.text_area("Cover Letter", cover_letter, height=300, disabled=False, key="cover_letter_view")
                with tab2:
                    st.text_area("LinkedIn Message", linkedin_message, height=240, disabled=False, key="linkedin_view")
                with tab3:
                    st.text_area("Full Report", report_content, height=420, disabled=False, key="report_view")

                st.markdown(
                    """
                    <div class='result-section'>
                        <div class='section-title'>Download Your Report</div>
                        <div class='section-note'>Save your analysis summary for your records or to share with mentors and career coaches.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="📥 Download Report",
                        data=report_content,
                        file_name="resume_match_analysis.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )

                if not resume_data['raw_text']:
                    st.warning("No readable text found in this PDF. It may be scanned or image-based.")

                try:
                    resume_filename = uploaded_file.name if uploaded_file else "resume.pdf"
                    save_analysis(
                        resume_filename=resume_filename,
                        job_text=job_data['raw_text'],
                        ats_score=ats_results['ats_score'],
                        skill_match_percentage=ats_results['skill_match_percentage'],
                        semantic_score=ats_results['semantic_score'],
                        completeness_score=ats_results['completeness_score'],
                        matched_skills=ats_results['matched_skills'],
                        missing_skills=ats_results['missing_skills'],
                        report_text=report_content,
                    )
                except Exception as e:
                    st.warning(f"Could not save to history: {str(e)}")

                st.divider()
                st.subheader("Raw Text Preview")

                with st.expander("Resume Text Preview"):
                    preview = resume_data['raw_text'][:3000]
                    st.text_area("Resume Text", preview, height=220, disabled=False)
                    if len(resume_data['raw_text']) > 3000:
                        st.write("... (truncated)")

                with st.expander("Job Description Preview"):
                    preview = job_data['raw_text'][:3000]
                    st.text_area("Job Description", preview, height=220, disabled=False)
                    if len(job_data['raw_text']) > 3000:
                        st.write("... (truncated)")

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")