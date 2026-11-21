# AI Resume Analyzer

An interactive Resume Analysis and Job Description Matching application built using Python and Machine Learning techniques.

## Project Overview

AI Resume Analyzer helps job applicants evaluate how well their resumes match a particular job description.

Users can upload a PDF resume, extract technical skills, compare them with job requirements, identify missing skills, calculate a matching score, and download a detailed analysis report.

## Features

- PDF Resume Text Extraction
- Technical Skill Extraction
- Resume Section Detection
- Job Description Analysis
- Matched and Missing Skills Identification
- Resume Match Score Calculation
- TF-IDF Text Similarity
- Personalized Improvement Recommendations
- Interactive Dashboard and Charts
- Downloadable PDF Analysis Report

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Web application |
| PyMuPDF | PDF text extraction |
| Regular Expressions | Skill extraction |
| Scikit-learn | TF-IDF and Cosine Similarity |
| Plotly / Streamlit Charts | Data visualization |
| ReportLab | PDF report generation |

## How It Works

1. User uploads a PDF resume.
2. The application extracts resume text.
3. Technical skills and resume sections are identified.
4. User pastes a job description.
5. Required skills are extracted.
6. Resume skills are compared with job requirements.
7. TF-IDF and Cosine Similarity calculate text similarity.
8. A combined matching score is generated.
9. The application displays recommendations and generates a PDF report.

## Matching Score

The application uses a weighted scoring approach:

- Skill Matching: 70%
- Text Similarity: 30%

**Formula:**

Final Score = (Skill Match × 0.70) + (Text Similarity × 0.30)

This is a heuristic matching score and not a prediction of hiring probability.

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project folder:

```bash
cd AI-Resume-Analyzer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Future Improvements

- Advanced NLP-based skill extraction
- LLM-powered resume feedback
- Semantic similarity using sentence embeddings
- Support for DOCX resumes
- Improved detection of resume sections
- Resume improvement suggestions based on job requirements

## Disclaimer

The matching score is an experimental evaluation metric. It should not be interpreted as an actual recruitment or hiring decision.

## Author

B. Abhitheswar Reddy

Computer Science and Engineering Student