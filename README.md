# CareerTwin AI 🚀
### Autonomous Multi-Agent AI Career Digital Twin Platform for Students

**CareerTwin AI** is an intelligent, multi-agent AI career digital twin platform designed specifically for students and early-career job seekers. It mirrors a student's academic and technical identity, benchmarks their capabilities against industry requirements for target career roles, pinpoints skill gaps, generates milestone roadmaps, conducts interactive mock interviews, optimizes resumes with Google STAR/XYZ impact metrics, and matches opportunities.

## 🚀 Live Demo

[Open CareerTwin AI](https://careertwinai-production.up.railway.app)
---

## 🌟 Key Features

1. **Student Profile & Digital Twin Knowledge Store**:
   - Collects and manages student identity: Name, Education, GPA, Graduation Year, Categorized Technical Skills (Languages, Frameworks, Databases, Cloud & DevOps, Tools), Projects, Certifications, and Target Career Role.
   - **1-Click Resume Ingestion**: Drag-and-drop PDF/Text resume parser that extracts skills, GPA, and projects automatically.
   - Preloaded with 3 diverse student sample profiles: **Alex Chen (AI/ML Engineer)**, **Sarah Lin (Fullstack Software Engineer)**, and **Marcus Miller (Cloud & DevOps Engineer)**.

2. **Multi-Agent AI Intelligence Engine**:
   - 🤖 **Digital Twin Core Orchestrator Agent (`twin_agent`)**: Coordinates all specialist agents, calculates the composite Twin Readiness Index (0-100%), and powers the conversational Career Copilot.
   - 📊 **Skill Gap & Market Intelligence Agent (`gap_analyzer_agent`)**: Benchmarks student capabilities against industry standards across 6 dimensions with interactive radar visualizations, identifying critical and secondary gaps.
   - 🗺️ **Roadmap & Curriculum Planner Agent (`roadmap_agent`)**: Generates step-by-step milestone roadmaps with time commitments, interactive task checklists, curated learning resources, and capstone project blueprints.
   - 📄 **Resume & Portfolio Branding Agent (`branding_agent`)**: Evaluates ATS keyword density, provides scoring breakdowns, and rewrites bullet points into quantifiable Google XYZ / STAR statements with live HTML print/PDF export.
   - 🎙️ **AI Mock Interviewer & Simulation Agent (`interview_agent`)**: Simulates realistic multi-round technical, system design, and behavioral interviews with real-time scoring, gold-standard model answers, and coaching takeaways.
   - 🚀 **Opportunity Scout & Application Matcher Agent (`scout_agent`)**: Analyzes candidate fit against target job postings, generating compatibility match scores, customized 3-paragraph cover letters, and high-converting cold outreach pitch emails.

3. **Resilient Dual-Mode Execution**:
   - **Google Gemini API Mode**: Powered by Gemini (`gemini-2.5-flash` / `gemini-1.5-flash`) when `GEMINI_API_KEY` is provided in `.env`.
   - **Deterministic AI Heuristic Engine**: Built-in fallback heuristics ensuring 100% of features work smoothly out of the box with zero external setup.

---

## 🏗️ Architecture

```
CareerTwinAI/
├── backend/
│   ├── api/
│   │   └── routes.py              # REST API endpoints for all Twin workflows
│   ├── agents/
│   │   ├── base_agent.py          # Base agent with LLM caller & JSON parser
│   │   ├── twin_agent.py          # Digital Twin Core Orchestrator
│   │   ├── gap_analyzer_agent.py  # Market intelligence & skill gap analyzer
│   │   ├── roadmap_agent.py       # Milestone upskilling roadmap planner
│   │   ├── branding_agent.py      # Resume & STAR/XYZ optimizer
│   │   ├── interview_agent.py     # Interactive mock interviewer
│   │   └── scout_agent.py         # Job compatibility & cover letter scout
│   ├── models/
│   │   ├── profile.py             # StudentProfile and schema definitions
│   │   └── agents.py              # Request/Response schemas
│   ├── data/
│   │   ├── role_benchmarks.py     # Industry role benchmarks & standards
│   │   └── sample_profiles.py     # Preloaded student candidate profiles
│   ├── services/
│   │   ├── storage.py             # SQLite persistence layer
│   │   ├── resume_parser.py       # PDF & Text resume parser
│   │   └── gemini_client.py       # Google GenAI client
│   ├── config.py                  # Environment & database settings
│   └── main.py                    # FastAPI server entrypoint
├── frontend/
│   ├── index.html                 # Modern SPA user interface
│   ├── css/styles.css             # Glassmorphism & custom styling
│   └── js/app.js                  # Frontend state management & visualizations
├── tests/
│   └── test_career_twin.py        # Automated test suite
├── .env.example                   # Environment configuration example
├── requirements.txt               # Python package dependencies
├── run.py                         # Application launcher script
└── README.md                      # Project documentation
```

---

## 🚀 Quick Start

### 1. Install Dependencies
Ensure Python 3.10+ is installed, then run:
```bash
python -m pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
To enable live Gemini API generation, create a `.env` file (or edit the existing one):
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=8000
HOST=127.0.0.1
```
*(Note: If `GEMINI_API_KEY` is not provided, CareerTwin AI operates using its built-in deterministic heuristic AI engine).*

### 3. Run the Application
Launch the server using:
```bash
python run.py
```
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 🧪 Running Tests

Execute the test suite using `unittest`:
```bash
python -m unittest tests/test_career_twin.py
```

---

## 💡 Usage Guide

1. **Dashboard**: View your overall **Twin Readiness Score**, dynamic Skill Radar Chart, and immediate high-priority gap alerts.
2. **Skill Gap Matrix**: Inspect how your skills stack up against standard expectations for roles like AI/ML Engineer, Fullstack Developer, DevOps Engineer, Data Scientist, and Cybersecurity Analyst.
3. **Dynamic Roadmap**: Follow customized milestones, check off completed learning tasks, and explore production-grade capstone project blueprints.
4. **ATS Resume Studio**: Review your ATS compatibility score, inspect missing keywords, view Google XYZ bullet transformations, and export a formatted resume to PDF.
5. **AI Mock Interview**: Practice answering technical and system design questions and receive instant multi-dimensional rubrics and model answers.
6. **Opportunity Scout**: Paste any job description to calculate your match score and generate tailored cover letters and LinkedIn outreach messages.
7. **Digital Twin Copilot**: Ask questions directly to your AI Career Twin about strategic upskilling and career planning.
