
import streamlit as st
import pymupdf
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Technical skills database

SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "C++": ["c++"],
    "SQL": ["sql", "mysql"],
    "Machine Learning": ["machine learning"],
    "Deep Learning": ["deep learning"],
    "Artificial Intelligence": ["artificial intelligence"],
    "NLP": ["nlp", "natural language processing"],
    "PyTorch": ["pytorch"],
    "TensorFlow": ["tensorflow"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "AWS": ["aws", "amazon web services"],
    "OCI": ["oci", "oracle cloud"],
    "Docker": ["docker"],
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "REST API": ["rest api", "rest apis", "restful api"],
    "Git": ["git", "github"],
    "RAG": ["rag", "retrieval augmented generation"],
    "HTML": ["html"],
    "CSS": ["css"],
    "JavaScript": ["javascript"],
    "React": ["react"],
    "Computer Vision": ["computer vision"]
}


# Function to extract skills from resume

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill, aliases in SKILLS.items():

        for alias in aliases:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(alias)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, text):

                found_skills.append(skill)
                break

    return found_skills


def analyze_resume_sections(text):

    sections = {
        "Education": ["education"],
        "Experience": ["experience", "work experience"],
        "Projects": ["projects"],
        "Certifications": ["certifications", "certificates"],
        "Achievements": ["achievements"],
        "Skills": ["technical skills", "skills"]
    }

    found_sections = []

    for line in text.splitlines():

        heading = line.strip().lower()

        for section, keywords in sections.items():

            if heading in keywords and section not in found_sections:
                found_sections.append(section)

    return found_sections





st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    h1 {
        color: #17365D;
        font-weight: 800;
    }

    h2, h3 {
        color: #24527A;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #dce3ed;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .stButton button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and extract its contents."
)

st.divider()

# Resume upload
st.subheader("Upload Your Resume")

resume = st.file_uploader(
    "Choose your PDF resume",
    type=["pdf"]
)

# Extract text from PDF

def extract_resume_text(pdf_file):

    document = pymupdf.open(
        stream=pdf_file.getvalue(),
        filetype="pdf"
    )

    resume_text = ""

    for page in document:
        resume_text += page.get_text() + "\n"

    document.close()

    return resume_text



# Process uploaded resume
if resume is not None:

    st.success("Resume uploaded successfully!")

    resume_text = extract_resume_text(resume)


    if resume_text.strip():
        st.subheader("Extracted Resume Text")
        st.text_area(
           "Resume Content",
            resume_text,
            height=350
        )

        st.info(
            f"Total words: {len(resume_text.split())}"
        )

    # Extract technical skills
    skills = extract_skills(resume_text)
    # Detect resume sections
    sections = analyze_resume_sections(resume_text)
    st.divider()
    st.subheader("📑 Detected Resume Sections")

    if sections:
       for section in sections:
        st.success(section)
    else:
          st.warning("No resume sections detected.")

    st.divider()
    st.subheader("🎯 Detected Technical Skills")

    if skills:

        for skill in skills:
            st.success(skill)

    else:
        st.warning("No technical skills detected.")

else:

    st.warning("No readable text found in this PDF.")

st.divider()

# Job Description Analysis
st.subheader("📋 Job Description Analysis")

job_description = st.text_area(
    "Paste the Job Description here:",
    height=200,
    placeholder="Paste the complete job description..."
)

if resume is not None and job_description.strip():

    jd_skills = extract_skills(job_description)

    matched_skills = [
        skill for skill in skills
        if skill in jd_skills
    ]

    missing_skills = [
        skill for skill in jd_skills
        if skill not in skills
    ]

    st.divider()
    st.subheader("📊 Resume vs Job Description Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("Required Skills", len(jd_skills))
    col2.metric("Matched Skills", len(matched_skills))
    col3.metric("Missing Skills", len(missing_skills))

    st.subheader("✅ Matched Skills")

    if matched_skills:
        for skill in matched_skills:
            st.success(skill)
    else:
        st.warning("No matching skills found.")

    st.subheader("❌ Missing Skills")

    if missing_skills:
        for skill in missing_skills:
            st.error(skill)
    else:
        st.success("Your resume contains all detected JD skills!")

    
    st.divider()
    st.subheader("🏆 Resume Match Score")

    if jd_skills:
        match_score = (len(matched_skills) / len(jd_skills)) * 100

        # Calculate text similarity using TF-IDF
        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform([
            resume_text,
            job_description
        ])

        similarity_score = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0] * 100

        # Combine skill matching and text similarity
        skill_score = match_score

        match_score = (
            0.70 * skill_score +
            0.30 * similarity_score
        )


        st.metric(
            "Overall Skill Match",
            f"{match_score:.2f}%"
        )

        st.metric(
            "Text Similarity",
            f"{similarity_score:.2f}%"
        )

        st.progress(match_score / 100)

        if match_score >= 80:
            st.success("Excellent! Your resume matches this job well.")
        elif match_score >= 50:
            st.warning("Good match, but you should improve some skills.")
        else:
            st.error("Your resume needs improvement for this job.")
    else:
        st.warning("No required skills detected in the job description.")

    
    st.divider()
    st.subheader("💡 Resume Improvement Recommendations")

    if missing_skills:
        st.write("Consider improving or learning these skills:")

        for skill in missing_skills:
            st.info(f"📌 Add relevant {skill} experience if you have it.")

        st.write("**Additional suggestions:**")
        st.write("- Include measurable achievements in your projects.")
        st.write("- Highlight relevant technical skills.")
        st.write("- Tailor your resume summary to the job description.")
        st.write("- Add project links and GitHub repositories.")
        
    else:
        st.success("Your resume covers all the detected required skills!")
        st.write("Focus on improving your project descriptions and achievements.")

    
    st.divider()
    st.subheader("📈 Visual Skill Analysis")

    
    chart_data = {
        "Skill Category": ["Matched Skills", "Missing Skills"],
        "Number of Skills": [
            len(matched_skills),
            len(missing_skills)
        ]
    }

    st.bar_chart(
        chart_data,
        x="Skill Category",
        y="Number of Skills"
    )


    st.subheader("📊 Analysis Summary")

    st.write(f"Total required skills: {len(jd_skills)}")
    st.write(f"Skills matched: {len(matched_skills)}")
    st.write(f"Skills missing: {len(missing_skills)}")
    st.write(f"Resume match score: {match_score:.2f}%")


    st.divider()
    st.subheader("📥 Download Analysis Report")

    pdf_buffer = BytesIO()

    pdf = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    report = []

    report.append(
        Paragraph("AI Resume Analysis Report", styles["Title"])
    )

    report.append(Spacer(1, 20))

    score_text = f"{match_score:.2f}%" if jd_skills else "N/A"

    report.append(
        Paragraph(f"Resume Match Score: {score_text}", styles["Heading2"])
    )
    report.append(
    Paragraph(
        f"Text Similarity: {similarity_score:.2f}%",
        styles["Normal"]
    )
)

    report.append(Spacer(1, 15))

    report.append(Spacer(1, 15))

    report.append(
        Paragraph("Matched Skills", styles["Heading2"])
    )

    for skill in matched_skills:
        report.append(Paragraph(f"- {skill}", styles["Normal"]))

    report.append(Spacer(1, 15))

    report.append(
        Paragraph("Missing Skills", styles["Heading2"])
    )

    for skill in missing_skills:
        report.append(Paragraph(f"- {skill}", styles["Normal"]))

    report.append(Spacer(1, 15))

    report.append(
        Paragraph("Recommendations", styles["Heading2"])
    )

    for skill in missing_skills:
        report.append(
            Paragraph(
                f"- Improve your knowledge of {skill}.",
                styles["Normal"]
            )
        )

    pdf.build(report)

    st.download_button(
        label="📄 Download Resume Analysis PDF",
        data=pdf_buffer.getvalue(),
        file_name="Resume_Analysis_Report.pdf",
        mime="application/pdf"
    )





   