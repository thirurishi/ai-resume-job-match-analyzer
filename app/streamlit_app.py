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
    st.markdown("""
        <div class='hero-title'>AI Resume & Job Match Analyzer</div>
        <div class='hero-subtitle'>Analyze ATS readiness, skill gaps, semantic relevance, and recruiter fit in seconds.</div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='step-box'>
            <div class='step-title'>Workflow</div>
            <ol>
                <li>Upload Resume</li>
                <li>Paste Job Description</li>
                <li>Analyze Match</li>
                <li>Review Feedback</li>
                <li>Download Report</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.subheader("📊 Recent Analysis History")

    history = get_analysis_history(limit=5)
    if history:
        for analysis in history:
            with st.expander(f"📅 {analysis['created_at'][:10]}  •  ATS {analysis['ats_score']:.0f}"):
                st.write(f"**Resume:** {analysis['resume_filename']}")
                st.write(f"**Skill Match:** {analysis['skill_match_percentage']:.1f}%")
                st.write(f"**Semantic Score:** {analysis['semantic_score']:.1f}/100")
                if analysis['matched_skills']:
                    st.write(f"**Matched:** {', '.join(analysis['matched_skills'][:3])}")
                if analysis['missing_skills']:
                    st.write(f"**Missing:** {', '.join(analysis['missing_skills'][:3])}")
    else:
        st.info("No analysis history yet. Run your first analysis above.")

# Hero section
with st.container():
    st.markdown("""
        <div class='hero-card'>
            <div class='hero-title'>AI Resume & Job Match Analyzer</div>
            <div class='hero-subtitle'>Analyze ATS readiness, skill gaps, semantic relevance, and recruiter fit in seconds.</div>
            <div class='badge-pill'>ATS Scoring</div>
            <div class='badge-pill'>Skill Gap Analysis</div>
            <div class='badge-pill'>Recruiter Feedback</div>
            <div class='badge-pill'>Cover Letter Draft</div>
            <div class='badge-pill'>Report Download</div>
        </div>
    """, unsafe_allow_html=True)

# Input section
with st.container():
    input_left, input_right = st.columns([1, 1], gap="large")

    with input_left:
        st.markdown("""
            <div class='input-card'>
                <h3>Resume Upload</h3>
                <p>Upload a PDF resume to extract text and surface ATS-ready insights.</p>
            </div>
        """, unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Resume PDF",
            type="pdf",
            help="Upload a text-based PDF resume for best results.",
        )

    with input_right:
        st.markdown("""
            <div class='input-card'>
                <h3>Job Description</h3>
                <p>Paste a full job description for the best matching and scoring results.</p>
            </div>
        """, unsafe_allow_html=True)
        job_desc = st.text_area(
            "Job Description",
            height=320,
            help="Include the full job posting text for accurate skill matching.",
        )

    st.markdown("""
        <div class='input-card'>
            <p>Upload a PDF resume and paste a full job description for best results.</p>
        </div>
    """, unsafe_allow_html=True)

    button_col1, button_col2, button_col3 = st.columns([1, 0.4, 1])
    analyze_clicked = button_col2.button("Analyze Match")

# Analysis result container
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
            ats_results = None
            feedback = None
            resume_bullets = None
            cover_letter = None
            linkedin_message = None
            report_content = None

            with result_container:
                if not resume_data['raw_text']:
                    st.warning("No readable text found in this PDF. It may be scanned or image-based.")

                ats_results = calculate_ats_score(
                    resume_data['raw_text'],
                    job_data['raw_text'],
                )

                feedback = generate_feedback(ats_results)
                resume_bullets = generate_resume_bullets(
                    resume_data['raw_text'],
                    job_data['raw_text'],
                    ats_results,
                )
                cover_letter = generate_cover_letter(
                    resume_data['raw_text'],
                    job_data['raw_text'],
                    ats_results,
                )
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

                st.markdown("""
                    <div class='result-card'>
                        <h3>Match Dashboard</h3>
                        <p>Review ATS readiness, core metrics, and advanced recruiter feedback.</p>
                    </div>
                """, unsafe_allow_html=True)

                top1, top2, top3, top4 = st.columns(4, gap="large")
                top1.metric("ATS Score", f"{ats_results['ats_score']:.1f}/100")
                top2.metric("Skill Match", f"{ats_results['skill_match_percentage']:.1f}%")
                top3.metric("Semantic Score", f"{ats_results['semantic_score']:.1f}/100")
                top4.metric("Completeness", f"{ats_results['completeness_score']:.1f}%")

                chart_col1, chart_col2 = st.columns([1.2, 1], gap="large")

                gauge_fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=ats_results['ats_score'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 100], 'tickcolor': '#94a3b8'},
                            'bar': {'color': '#38bdf8'},
                            'bgcolor': '#0f172a',
                            'borderwidth': 0,
                            'steps': [
                                {'range': [0, 40], 'color': '#f87171'},
                                {'range': [40, 60], 'color': '#facc15'},
                                {'range': [60, 80], 'color': '#34d399'},
                                {'range': [80, 100], 'color': '#60a5fa'},
                            ],
                        },
                        title={'text': 'ATS Score', 'font': {'color': '#e2e8f0'}},
                        number={'font': {'color': '#e2e8f0'}}
                    )
                )
                gauge_fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    margin={'t': 20, 'b': 20, 'l': 0, 'r': 0},
                )

                bar_fig = px.bar(
                    x=['Skill Match', 'Semantic Score', 'Completeness'],
                    y=[
                        ats_results['skill_match_percentage'],
                        ats_results['semantic_score'],
                        ats_results['completeness_score'],
                    ],
                    labels={'x': '', 'y': 'Score'},
                    text=[
                        f"{ats_results['skill_match_percentage']:.1f}%",
                        f"{ats_results['semantic_score']:.1f}%",
                        f"{ats_results['completeness_score']:.1f}%",
                    ],
                    color=['Skill Match', 'Semantic Score', 'Completeness'],
                    color_discrete_sequence=['#38bdf8', '#a78bfa', '#67e8f9'],
                )
                bar_fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(15,23,42,0.6)',
                    font_color='#e2e8f0',
                    margin={'t': 10, 'b': 10, 'l': 0, 'r': 0},
                    showlegend=False,
                )
                bar_fig.update_traces(textposition='outside')

                chart_col1.plotly_chart(gauge_fig, use_container_width=True)
                chart_col2.plotly_chart(bar_fig, use_container_width=True)

                if len(ats_results['job_skills']) == 0:
                    st.warning("No known skills detected in the job description. Try pasting a more detailed job description.")

                st.markdown("""
                    <div class='result-card'>
                        <h4>Skill Match Breakdown</h4>
                    </div>
                """, unsafe_allow_html=True)

                skill_left, skill_right = st.columns(2, gap="large")
                with skill_left:
                    st.markdown("**Matched Skills** ✓")
                    if ats_results['matched_skills']:
                        matched_html = "".join([
                            f"<span class='tag-pill'>{skill}</span>" for skill in ats_results['matched_skills']
                        ])
                        st.markdown(matched_html, unsafe_allow_html=True)
                    else:
                        st.write("No matching skills found.")

                with skill_right:
                    st.markdown("**Missing Skills** ✗")
                    if ats_results['missing_skills']:
                        missing_html = "".join([
                            f"<span class='tag-pill missing'>{skill}</span>" for skill in ats_results['missing_skills']
                        ])
                        st.markdown(missing_html, unsafe_allow_html=True)
                    else:
                        st.write("All job skills are covered!")

                if ats_results['resume_skills']:
                    with st.expander("Resume Skills"):
                        st.markdown(", ".join(ats_results['resume_skills']))
                if ats_results['job_skills']:
                    with st.expander("Job Skills"):
                        st.markdown(", ".join(ats_results['job_skills']))

                st.markdown("""
                    <div class='result-card'>
                        <h4>Recruiter Feedback</h4>
                    </div>
                """, unsafe_allow_html=True)

                with st.expander("Strengths"):
                    for strength in feedback['strengths']:
                        st.write(f"• {strength}")

                with st.expander("Weaknesses"):
                    for weakness in feedback['weaknesses']:
                        st.write(f"• {weakness}")

                with st.expander("Improvement Suggestions"):
                    for i, suggestion in enumerate(feedback['suggestions'], 1):
                        st.write(f"{i}. {suggestion}")

                with st.expander("Resume Bullet Rewrites"):
                    for i, bullet in enumerate(resume_bullets, 1):
                        st.write(f"{i}. {bullet}")

                st.markdown("""
                    <div class='result-card'>
                        <h4>Generated Content</h4>
                    </div>
                """, unsafe_allow_html=True)

                tab1, tab2, tab3 = st.tabs(["Cover Letter", "LinkedIn Message", "Full Report"])

                with tab1:
                    st.text_area("Cover Letter Draft", cover_letter, height=320, disabled=True)

                with tab2:
                    st.text_area("LinkedIn Message Draft", linkedin_message, height=260, disabled=True)

                with tab3:
                    st.text_area("Full Report", report_content, height=380, disabled=True)

                st.markdown("""
                    <div class='result-card'>
                        <h4>Download</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.download_button(
                    label="📄 Download Full Report",
                    data=report_content,
                    file_name="resume_analysis_report.txt",
                    mime="text/plain",
                )

                st.success("Analysis complete. Scroll down for data previews and recommended actions.")

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
                st.subheader("Text Previews")

                with st.expander("Extracted Resume Text Preview"):
                    preview = resume_data['raw_text'][:3000]
                    st.text_area("Resume Text", preview, height=220, disabled=True)
                    if len(resume_data['raw_text']) > 3000:
                        st.write("... (truncated)")

                with st.expander("Cleaned Job Description Preview"):
                    preview = job_data['raw_text'][:3000]
                    st.text_area("Job Description", preview, height=220, disabled=True)
                    if len(job_data['raw_text']) > 3000:
                        st.write("... (truncated)")

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")