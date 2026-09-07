import re
import io
from typing import Dict, Any, List, Optional
from pypdf import PdfReader
from ..models.profile import StudentProfile

# Expanded tech skills lexicon for accurate matching
TECH_SKILLS_LEXICON = [
    # Languages
    "Python", "Java", "C++", "C", "C#", "JavaScript", "TypeScript", "SQL", "HTML", "CSS", "R", "Go", "Rust", "Kotlin", "Swift", "PHP",
    # AI / ML / Data Science
    "PyTorch", "TensorFlow", "Keras", "Scikit-Learn", "Pandas", "NumPy", "OpenCV", "Matplotlib", "Seaborn",
    "Deep Learning", "Machine Learning", "Computer Vision", "NLP", "Natural Language Processing",
    "Hugging Face", "Transformers", "LLMs", "Generative AI", "RAG", "LangChain", "LlamaIndex",
    "Vector Databases", "ChromaDB", "Pinecone", "Milvus", "Weaviate", "FAISS",
    # Backend & Web
    "FastAPI", "Flask", "Django", "React", "Node.js", "Express", "Next.js", "Spring Boot", "REST APIs", "GraphQL",
    # Databases & Caching
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Cassandra", "Elasticsearch",
    # Cloud & DevOps
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Git", "GitHub", "Linux", "CI/CD", "Terraform", "MLOps",
    # System Design & Core CS
    "System Design", "Microservices", "Data Structures", "Algorithms", "Object-Oriented Programming"
]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text lines cleanly from uploaded PDF bytes."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def extract_skills_from_text(raw_text: str) -> List[str]:
    """Finds all technical skills in the text using boundary-safe regex."""
    text_lower = raw_text.lower()
    found_skills = []
    
    # Custom aliases
    alias_map = {
        "ml": "Machine Learning",
        "dl": "Deep Learning",
        "nlp": "NLP",
        "cv": "Computer Vision",
        "sklearn": "Scikit-Learn",
        "torch": "PyTorch",
        "k8s": "Kubernetes",
        "postgres": "PostgreSQL",
        "js": "JavaScript",
        "ts": "TypeScript"
    }

    for skill in TECH_SKILLS_LEXICON:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill.lower()) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            if skill not in found_skills:
                found_skills.append(skill)

    for alias, canonical in alias_map.items():
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower) and canonical not in found_skills:
            found_skills.append(canonical)

    return found_skills

def parse_resume_text(raw_text: str, filename: str = "") -> Dict[str, Any]:
    """Extract profile metadata from resume text using regex and heuristics."""
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    if not lines:
        return {}

    # Extract name (first non-empty header line if valid name format)
    name = ""
    if lines:
        candidate_line = lines[0]
        if "@" not in candidate_line and "http" not in candidate_line.lower() and len(candidate_line.split()) <= 4:
            name = candidate_line

    # Extract Degree & Branch
    degree = "B.Tech"
    branch = "Computer Science Engineering"
    text_lower = raw_text.lower()

    if "b.e." in text_lower or "bachelor of engineering" in text_lower:
        degree = "B.E."
    elif "m.tech" in text_lower or "master of technology" in text_lower:
        degree = "M.Tech"
    elif "b.s." in text_lower or "bachelor of science" in text_lower:
        degree = "B.S."
    elif "m.s." in text_lower or "master of science" in text_lower:
        degree = "M.S."
    elif "bca" in text_lower:
        degree = "BCA"
    elif "mca" in text_lower:
        degree = "MCA"

    if "artificial intelligence" in text_lower or "ai & ds" in text_lower:
        branch = "Artificial Intelligence & Data Science"
    elif "information technology" in text_lower or " it " in text_lower:
        branch = "Information Technology"
    elif "data science" in text_lower:
        branch = "Data Science"
    elif "electronics" in text_lower or "ece" in text_lower:
        branch = "Electronics and Communication Engineering"

    # Extract Year of Study / Graduation Year
    year_of_study = "3rd Year"
    year_match = re.search(r"(?:202[4-9]|203[0-5])", raw_text)
    if year_match:
        grad_year = year_match.group(0)
        year_of_study = f"Class of {grad_year}"

    # Extract CGPA
    cgpa_match = re.search(r"(?:CGPA|GPA|cgpa|gpa)[\s:]*([0-9]\.\d{1,2})", raw_text)
    cgpa = float(cgpa_match.group(1)) if cgpa_match else 8.0

    # Extract Skills
    found_skills = extract_skills_from_text(raw_text)
    if not found_skills:
        found_skills = ["Python", "SQL", "HTML", "CSS", "JavaScript"]

    # Extract Projects bullet points
    bullet_regex = re.findall(r"(?:•|\*|-|\d+\.)\s+(.+)", raw_text)
    bullets = [b.strip() for b in bullet_regex if len(b.strip()) > 20]

    projects = bullets[:3] if bullets else [
        "Web Development & Responsive UI Portfolio",
        "Machine Learning Predictive Modeling System in Python"
    ]

    # Extract Certifications
    certs = []
    cert_matches = re.findall(r"(?:certified|certification|certificate|coursera|deeplearning\.ai|aws certified)[\s:]*([A-Za-z0-9\s\-]+)", raw_text, re.IGNORECASE)
    for c in cert_matches:
        cleaned = c.strip()
        if len(cleaned) > 5 and len(cleaned) < 50:
            certs.append(cleaned)
    if not certs:
        certs = ["Python Programming Fundamentals", "Relational Database Foundations & SQL Basics"]

    # Infer target role
    target_role = "AI Engineer" if any(s in ["PyTorch", "TensorFlow", "Transformers", "Scikit-Learn", "Deep Learning", "LLMs", "RAG"] for s in found_skills) else "Software Engineer"

    parsed_profile = StudentProfile(
        name=name,
        degree=degree,
        branch=branch,
        year_of_study=year_of_study,
        cgpa=cgpa,
        current_skills=found_skills,
        projects=projects,
        certifications=certs[:3],
        target_career=target_role,
        resume_filename=filename,
        raw_resume_text=raw_text[:4000]
    )

    return parsed_profile.model_dump()

def parse_resume_file(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    if filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    else:
        text = file_bytes.decode("utf-8", errors="ignore")
    return parse_resume_text(text, filename=filename)
