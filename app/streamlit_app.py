import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))


import streamlit as st

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

st.set_page_config(page_title="AI Resume & Job Match Analyzer", layout="wide")
st.title("AI Resume & Job Match Analyzer")

# Sidebar sections
with st.sidebar:
    st.header("Resume Upload")
    st.header("Job Description")
    st.header("ATS Match Score")
    st.header("Skill Gap Analysis")
    st.header("Recruiter Feedback")
    st.header("Reports")
    
    # Analysis History
    st.divider()
    st.subheader("📊 Recent Analysis History")
    
    history = get_analysis_history(limit=5)
    if history:
        for analysis in history:
            with st.expander(f"📅 {analysis['created_at'][:10]} - ATS: {analysis['ats_score']:.0f}"):
                st.write(f"**Resume:** {analysis['resume_filename']}")
                st.write(f"**ATS Score:** {analysis['ats_score']:.1f}/100")
                st.write(f"**Skill Match:** {analysis['skill_match_percentage']:.1f}%")
                st.write(f"**Semantic Score:** {analysis['semantic_score']:.1f}/100")
                
                matched = analysis['matched_skills']
                missing = analysis['missing_skills']
                
                if matched:
                    st.write(f"**Matched:** {', '.join(matched[:3])}")
                if missing:
                    st.write(f"**Missing:** {', '.join(missing[:3])}")
    else:
        st.info("No analysis history yet. Run your first analysis above!")

# Main content
uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")
job_desc = st.text_area("Job Description")

if st.button("Analyze Resume"):
    if not uploaded_file:
        st.error("Please upload a resume PDF.")
    elif not job_desc.strip():
        st.error("Please enter a job description.")
    else:
        try:
            resume_data = extract_text_from_pdf(uploaded_file)
            job_data = parse_job_description(job_desc)

            st.success("Resume and job description parsed successfully!")

            # Parsing Metrics
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Resume Metrics")
                st.write(f"Word Count: {resume_data['word_count']}")
                st.write(f"Character Count: {resume_data['character_count']}")
                st.write(f"Page Count: {resume_data['page_count']}")
            with col2:
                st.subheader("Job Description Metrics")
                st.write(f"Word Count: {job_data['word_count']}")
                st.write(f"Character Count: {job_data['character_count']}")

            # Calculate ATS Score
            if not resume_data['raw_text']:
                st.warning("No readable text found in this PDF. It may be scanned or image-based.")
            else:
                ats_results = calculate_ats_score(
                    resume_data['raw_text'],
                    job_data['raw_text']
                )

                # ATS Score Display
                st.divider()
                st.subheader("ATS Analysis Results")

                # Check if job skills detected
                if len(ats_results['job_skills']) == 0:
                    st.warning("No known skills detected in the job description. Try pasting a more detailed job description.")
                else:
                    # Main scoring metrics
                    score_col1, score_col2, score_col3, score_col4 = st.columns(4)
                    
                    with score_col1:
                        st.metric("ATS Score", f"{ats_results['ats_score']}/100")
                    with score_col2:
                        st.metric("Skill Match", f"{ats_results['skill_match_percentage']:.1f}%")
                    with score_col3:
                        st.metric("Semantic Score", f"{ats_results['semantic_score']:.1f}/100")
                    with score_col4:
                        st.metric("Completeness", f"{ats_results['completeness_score']:.1f}%")

                    # Semantic Label
                    st.write(f"**Semantic Match**: {ats_results['semantic_label']}")

                    # Feedback Summary
                    st.divider()
                    st.write(f"**Feedback**: {ats_results['feedback_summary']}")

                    # Skills Analysis
                    st.divider()
                    st.subheader("Skills Analysis")

                    skills_col1, skills_col2 = st.columns(2)

                    with skills_col1:
                        st.write("**Matched Skills** ✓")
                        if ats_results['matched_skills']:
                            for skill in ats_results['matched_skills']:
                                st.write(f"• {skill}")
                        else:
                            st.write("No matching skills found.")

                    with skills_col2:
                        st.write("**Missing Skills** ✗")
                        if ats_results['missing_skills']:
                            for skill in ats_results['missing_skills']:
                                st.write(f"• {skill}")
                        else:
                            st.write("All job skills are covered!")

                    # Detailed Skills Lists
                    with st.expander("Resume Skills"):
                        if ats_results['resume_skills']:
                            st.write(", ".join(ats_results['resume_skills']))
                        else:
                            st.write("No skills detected in resume.")

                    with st.expander("Job Skills"):
                        if ats_results['job_skills']:
                            st.write(", ".join(ats_results['job_skills']))
                        else:
                            st.write("No skills detected in job description.")

                    # Generate feedback and recommendations
                    feedback = generate_feedback(ats_results)
                    resume_bullets = generate_resume_bullets(
                        resume_data['raw_text'],
                        job_data['raw_text'],
                        ats_results
                    )
                    cover_letter = generate_cover_letter(
                        resume_data['raw_text'],
                        job_data['raw_text'],
                        ats_results
                    )
                    linkedin_message = generate_linkedin_message(ats_results)

                    # Recruiter Feedback Section
                    st.divider()
                    st.subheader("Recruiter Feedback")

                    feedback_col1, feedback_col2 = st.columns(2)

                    with feedback_col1:
                        st.write("**Strengths** 💪")
                        for strength in feedback['strengths']:
                            st.write(f"• {strength}")

                    with feedback_col2:
                        st.write("**Weaknesses** ⚠️")
                        for weakness in feedback['weaknesses']:
                            st.write(f"• {weakness}")

                    st.write("**Suggestions** 📝")
                    for i, suggestion in enumerate(feedback['suggestions'], 1):
                        st.write(f"{i}. {suggestion}")

                    # Resume Improvement Section
                    st.divider()
                    st.subheader("Resume Improvement Examples")

                    st.write("Consider using these ATS-friendly bullet points in your resume:")
                    for i, bullet in enumerate(resume_bullets, 1):
                        st.write(f"{i}. {bullet}")

                    # Cover Letter Section
                    st.divider()
                    st.subheader("Cover Letter Draft")

                    with st.expander("View Cover Letter"):
                        st.text_area(
                            "Cover Letter",
                            cover_letter,
                            height=300,
                            disabled=True,
                            key="cover_letter_preview"
                        )
                        st.info("Edit this draft and personalize it with your details and the specific job/company information.")

                    # LinkedIn Message Section
                    st.divider()
                    st.subheader("LinkedIn Outreach Message")

                    with st.expander("View LinkedIn Message"):
                        st.text_area(
                            "LinkedIn Message",
                            linkedin_message,
                            height=250,
                            disabled=True,
                            key="linkedin_preview"
                        )
                        st.info("Personalize this message with the recruiter's name and your details before sending.")

                    # Report Download Section
                    st.divider()
                    st.subheader("Download Full Report")

                    report_content = generate_text_report(
                        resume_metrics=resume_data,
                        job_metrics=job_data,
                        ats_result=ats_results,
                        feedback=feedback,
                        resume_bullets=resume_bullets,
                        cover_letter=cover_letter,
                        linkedin_message=linkedin_message
                    )

                    # Save analysis to database
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
                            report_text=report_content
                        )
                    except Exception as e:
                        st.warning(f"Could not save to history: {str(e)}")

                    st.download_button(
                        label="📄 Download Full Report (Text)",
                        data=report_content,
                        file_name="resume_analysis_report.txt",
                        mime="text/plain"
                    )

                    st.success("✅ All analysis complete! Download the full report or use the generated content above.")

            # Text Previews
            st.divider()
            st.subheader("Text Previews")

            with st.expander("Extracted Resume Text Preview"):
                preview = resume_data['raw_text'][:3000]
                st.text_area("Resume Text", preview, height=200, disabled=True)
                if len(resume_data['raw_text']) > 3000:
                    st.write("... (truncated)")

            with st.expander("Cleaned Job Description Preview"):
                preview = job_data['raw_text'][:3000]
                st.text_area("Job Description", preview, height=200, disabled=True)
                if len(job_data['raw_text']) > 3000:
                    st.write("... (truncated)")

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")