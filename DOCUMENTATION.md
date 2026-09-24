# CareerTwin AI 🚀

## Multi-Agent AI Career Digital Twin Platform

CareerTwin AI is a multi-agent AI application designed to help students and early-career developers understand their current career readiness, identify technical skill gaps, build personalized learning roadmaps, receive portfolio project recommendations, simulate hypothetical career improvements, and generate an overall career strategy.

The system combines an **external Large Language Model (Google Gemini)** with a **deterministic Python-based analysis layer**.

This dual-approach architecture allows CareerTwin AI to demonstrate practical LLM-powered multi-agent functionality without making the entire application dependent on an external LLM API.

---

# 1. Problem Statement

Students preparing for internships and placements often face difficulty determining:

* Which technical skills are required for their target role
* Which skills they already possess
* Which important skills they are missing
* What they should learn next
* Which projects can strengthen their portfolio
* How their profile could improve after learning new skills
* How to organize their placement preparation

CareerTwin AI addresses these problems by creating a structured digital representation of a student's career profile and processing it through multiple specialized agents.

---

# 2. Project Objectives

The main objectives of CareerTwin AI are:

1. Create a structured digital representation of a student's career profile.
2. Analyze the student's skills against target-role requirements.
3. Calculate an AI-estimated career readiness score.
4. Identify strong, developing, and missing skills.
5. Prioritize important skill gaps.
6. Generate a personalized five-phase career roadmap.
7. Recommend practical portfolio projects.
8. Simulate hypothetical career improvements.
9. Generate a consolidated career strategy.
10. Support resume upload and profile extraction.
11. Support custom Job Description analysis.
12. Integrate an external LLM through Google Gemini.
13. Provide deterministic fallback functionality when the external LLM is unavailable.

---

# 3. Core AI Architecture

CareerTwin AI follows a **dual-approach AI architecture**.

```text
                         CareerTwin AI
                              |
                +-------------+-------------+
                |                           |
                v                           v
        External LLM Mode          Deterministic Mode
                |                           |
                v                           v
        Google Gemini API          Python-based Logic
                |                           |
                +-------------+-------------+
                              |
                              v
                     Multi-Agent Pipeline
                              |
                              v
                    Career Analysis Results
```

The two approaches have different responsibilities.

### External LLM Approach

When a valid Gemini API key is configured, the specialized agents can use **Google Gemini** to generate contextual and structured AI responses.

### Deterministic Approach

When Gemini is unavailable, the application uses predefined Python logic, role benchmarks, skill matching, scoring rules, and fallback generators.

This means the application **does not completely depend on Gemini**.

Instead:

```text
Gemini Available
      ↓
LLM-powered generation

Gemini Unavailable
      ↓
Deterministic fallback
```

---

# 4. External LLM Integration

CareerTwin AI uses **Google Gemini as its external Large Language Model**.

The Gemini integration is implemented through:

```text
backend/services/gemini_client.py
backend/agents/base_agent.py
```

The application initializes the Google GenAI client using the configured API key.

Example configuration:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

The application can also attempt supported Gemini model fallbacks if the configured model is unavailable.

The LLM client sends agent-specific prompts to Gemini and can request structured JSON responses.

The shared `BaseAgent` class provides:

* LLM invocation
* System instructions
* JSON response mode
* JSON parsing
* Response cleanup
* Error handling

This allows multiple specialized agents to share the same LLM infrastructure.

---

# 5. Why Two AI Approaches Are Used

The project intentionally combines:

### 1. LLM-powered intelligence

Google Gemini is used for:

* Contextual analysis
* Natural-language generation
* Structured recommendations
* Personalized roadmap generation
* Skill-gap interpretation
* Project recommendations
* Career strategy generation

### 2. Deterministic processing

Python-based logic is used for:

* Readiness-score calculation
* Role benchmark comparison
* Skill matching
* Missing-skill identification
* Fallback roadmap generation
* Fallback project recommendations
* Fallback career simulation

This separation provides more control over important calculations while still allowing the project to demonstrate external LLM integration.

---

# 6. Multi-Agent Pipeline

The current implementation contains six specialized agents coordinated by the `AIOrchestrator`.

The execution pipeline is:

```text
Student Profile
      |
      v
1. Digital Twin / Profile Agent
      |
      v
2. Skill Gap Agent
      |
      v
3. Career Roadmap Agent
      |
      v
4. Project & Experience Agent
      |
      v
5. Future Career Simulation Agent
      |
      v
6. Career Strategist Agent
      |
      v
Final Master Career Strategy
```

The orchestrator records an `AgentTrace` for every stage, including the agent name, input summary, analysis, output summary, and structured output.

---

# 7. Agent 1 — Digital Twin / Profile Agent

### File

```text
backend/agents/profile_agent.py
```

### Purpose

The Profile Agent creates the initial career assessment from the student's profile.

It considers:

* Current technical skills
* Target career role
* Projects
* Education
* Certifications
* CGPA
* Resume information
* Custom Job Description

It produces:

* Career stage
* Strengths
* Weaknesses
* Matched skills
* Missing skills
* AI-estimated readiness score
* Score breakdown
* Improvement recommendations

The readiness score itself is calculated deterministically.

---

# 8. Readiness Score

The current implementation calculates the readiness score using four dimensions:

| Dimension                       | Maximum |
| ------------------------------- | ------: |
| Required Skills Match           |      40 |
| Projects & Practical Experience |      25 |
| Education & Certifications      |      15 |
| Role-Specific Gap Alignment     |      20 |
| **Total**                       | **100** |

## 8.1 Required Skills — 40 Points

The system compares the student's skills with:

* Core skills for the selected role
* Skills extracted from a custom Job Description
* Important benchmark skills

The matched proportion contributes up to 40 points.

---

## 8.2 Projects & Practical Experience — 25 Points

The current implementation uses the number of projects to determine the project component.

```text
3 or more projects → 25 points
2 projects         → 19 points
1 project          → 12 points
No projects        → 0 or 4 points depending on profile state
```

If the resume text contains internship-related information, an additional experience contribution can be added, subject to the 25-point maximum.

---

## 8.3 Education & Certifications — 15 Points

The education component considers:

* Degree/branch information
* CGPA
* Certifications

Relevant technical branches receive a larger contribution.

CGPA thresholds contribute additional points.

Certifications contribute additional points, subject to the 15-point maximum.

---

## 8.4 Role Gap Alignment — 20 Points

The implementation considers the number of missing skills.

```text
0–1 missing skills → 20 points
2–3 missing skills → 14 points
4–5 missing skills → 9 points
More than 5       → 5 points
```

---

## 8.5 Initial Empty State

When a new profile has:

* No skills
* No projects
* No uploaded resume

the readiness score is intentionally:

```text
0%
```

This ensures that a new user does not receive a misleading readiness score before providing profile information.

---

## 8.6 Important Interpretation

The readiness score is an **AI-estimated project metric**, not an official employability score.

It is based on the application's predefined scoring methodology and role benchmarks.

It does not guarantee:

* Interview selection
* Internship selection
* Job selection
* Employment
* Any specific career outcome

---

# 9. Agent 2 — Skill Gap Agent

### File

```text
backend/agents/skill_gap_agent.py
```

### Purpose

The Skill Gap Agent compares the student's current skills with the requirements of the selected target role.

It categorizes skills into:

### Strong

Skills already possessed and directly matching role requirements.

### Developing

Skills that the student has some familiarity with or that fall into the important-skill category.

### Missing

Important skills not currently present in the profile.

### Priority Skills

The most important missing skills that should be learned first.

The agent also generates radar-chart information comparing the student's capabilities with role benchmarks.

---

# 10. Skill Match Calculation

When Gemini is unavailable, the deterministic implementation:

1. Loads the selected role benchmark.
2. Adds skills extracted from a custom Job Description if available.
3. Compares student skills with required skills.
4. Categorizes them.
5. Calculates a role-match percentage.
6. Generates radar-chart data.

The deterministic match calculation gives:

```text
Strong skill      → full contribution
Developing skill  → half contribution
Missing skill     → no contribution
```

The result is bounded by the implementation's defined minimum and maximum values.

When Gemini is available, the Skill Gap Agent can instead request a structured skill-gap analysis from the external LLM.

---

# 11. Agent 3 — Career Roadmap Agent

### File

```text
backend/agents/roadmap_agent.py
```

### Purpose

The Career Roadmap Agent converts the detected skill gaps into a structured learning and career-development plan.

The roadmap contains five phases:

### Phase 1 — Foundation

Fundamental programming, data structures, algorithms, object-oriented concepts, and version control.

### Phase 2 — Core Skills

Important technical skills related to the student's target role.

### Phase 3 — Advanced Skills

Advanced concepts relevant to the target career.

### Phase 4 — Projects and Portfolio

Practical implementation through production-oriented projects.

### Phase 5 — Interview and Placement Preparation

Technical interview preparation, system design, and placement readiness.

For each phase, the system can provide:

* Skills to learn
* Suggested activities
* Timeframe
* Expected outcome

When Gemini is available, the agent requests a structured five-phase roadmap from the LLM.

If Gemini is unavailable, the built-in heuristic roadmap generator is used.

---

# 12. Agent 4 — Project & Experience Agent

### File

```text
backend/agents/project_agent.py
```

### Purpose

The Project & Experience Agent recommends practical projects based on:

* Target career role
* Current skills
* Missing skills
* Existing projects

The agent is designed to recommend projects that help demonstrate practical capability.

A generated project recommendation can include:

* Project title
* Difficulty
* Skills gained
* Career relevance
* Architecture
* Deliverable

The deterministic fallback provides role-specific project recommendations when LLM generation is unavailable.

---

# 13. Agent 5 — Career Strategist Agent

### File

```text
backend/agents/strategist_agent.py
```

### Purpose

The Career Strategist Agent is the final synthesis layer.

It receives outputs from the previous agents:

```text
Profile Agent
Skill Gap Agent
Career Roadmap Agent
Project & Experience Agent
Future Career Simulation Agent
```

It then generates a consolidated career strategy.

The strategy can contain:

* Current career assessment
* Top strengths
* Biggest gaps
* Immediate next steps
* Short-term strategy
* Long-term strategy
* Priority actions

This agent brings together the individual agent outputs into a single career plan.

---

# 14. Agent 6 — Future Career Simulation Agent

### File

```text
backend/agents/simulation_agent.py
```

### Purpose

The Future Career Simulation Agent provides a hypothetical "What-If" analysis.

The user can select hypothetical upskilling actions.

The system then compares:

```text
Current Digital Twin
        ↓
Selected Upskilling Actions
        ↓
Future Simulated Twin
```

The simulation can provide:

* Current readiness
* Future simulated readiness
* Score improvement
* Skill gaps closed
* New capabilities
* Current profile snapshot
* Future profile snapshot
* Competitive tier
* Simulation summary

The simulation represents a hypothetical modeled scenario rather than a guaranteed prediction of employment.

---

# 15. AI Orchestrator

### File

```text
backend/agents/orchestrator.py
```

The `AIOrchestrator` coordinates the complete multi-agent workflow.

The current execution order is:

```text
Agent 1 → Digital Twin / Profile Agent
Agent 2 → Skill Gap Agent
Agent 3 → Career Roadmap Agent
Agent 4 → Project & Experience Agent
Agent 6 → Future Career Simulation Agent
Agent 5 → Career Strategist Agent
```

The numerical identifiers are implementation IDs; the actual execution order is the sequence above.

The orchestrator stores the outputs from every stage and returns a final `OrchestrationResult`.

---

# 16. Agent Trace and Observability

For each agent, the orchestrator creates an `AgentTrace`.

The trace contains information such as:

* Agent ID
* Agent name
* Role description
* Status
* Input summary
* Reasoning/analysis summary
* Output summary
* Full structured output

This makes the multi-agent workflow observable rather than treating the entire system as one black-box AI call.

---

# 17. Resume Processing

### File

```text
backend/services/resume_parser.py
```

CareerTwin AI supports resume processing.

Supported input formats include:

```text
PDF
TXT
```

The resume workflow is:

```text
Resume Upload
      ↓
File Validation
      ↓
Text Extraction
      ↓
Information Extraction
      ↓
Profile Update
      ↓
Career Analysis
```

The extracted information can include:

* Skills
* Projects
* Certifications
* Academic information
* Internship/experience information
* Raw resume text

The extracted data is then incorporated into the Career Twin profile.

---

# 18. Custom Job Description Analysis

The application supports custom Job Descriptions.

A user can provide a Job Description for a specific opportunity.

The system extracts relevant skills from the supplied text and incorporates them into the role analysis.

This allows the Career Twin to compare a student's profile against:

```text
General Role Benchmark
+
Specific Job Description
```

rather than relying only on a generic career role.

---

# 19. Role Benchmark System

### File

```text
backend/data/role_benchmarks.py
```

The project contains predefined role benchmarks.

These benchmarks provide information such as:

* Core skills
* Important skills
* Radar categories
* Benchmark scores

The selected target role determines which benchmark is used for career analysis.

---

# 20. Student Profile Model

### File

```text
backend/models/profile.py
```

The `StudentProfile` model represents the student's Career Twin.

The profile contains information such as:

```text
Name
Degree
Branch
Year of Study
CGPA
Technical Skills
Projects
Certifications
Career Interests
Target Career
Dream Company
Job Description
Resume Filename
Raw Resume Text
Readiness Score
```

This structured profile becomes the primary input for the multi-agent pipeline.

---

# 21. Data Storage

### File

```text
backend/services/storage.py
```

CareerTwin AI uses SQLite-based persistence.

The storage layer maintains the current Career Twin profile and relevant orchestration state.

This allows information to persist between API requests.

---

# 22. Profile Reset

The application provides a profile reset operation:

```text
POST /api/profile/reset
```

The reset functionality is designed to return the Career Twin to a clean initial state.

The clean state contains no previously entered:

* Skills
* Projects
* Certifications
* Resume information
* Job Description

and the readiness score returns to:

```text
0%
```

This allows a new analysis to begin from a fresh profile.

---

# 23. Backend Architecture

The backend is implemented using Python and FastAPI.

Main backend components include:

```text
backend/
│
├── api/
│   └── routes.py
│
├── agents/
│   ├── base_agent.py
│   ├── orchestrator.py
│   ├── profile_agent.py
│   ├── skill_gap_agent.py
│   ├── roadmap_agent.py
│   ├── project_agent.py
│   ├── simulation_agent.py
│   └── strategist_agent.py
│
├── models/
│   ├── profile.py
│   └── agents.py
│
├── data/
│   ├── role_benchmarks.py
│   └── sample_profiles.py
│
├── services/
│   ├── storage.py
│   ├── resume_parser.py
│   └── gemini_client.py
│
├── config.py
└── main.py
```

---

# 24. Frontend Architecture

The frontend uses standard web technologies.

```text
frontend/
│
├── index.html
├── css/
│   └── styles.css
└── js/
    └── app.js
```

The frontend provides the user interface for:

* Profile management
* Career selection
* Resume upload
* Career analysis
* Skill-gap visualization
* Roadmap display
* Project recommendations
* Career simulation
* Career strategy
* Backend API communication

---

# 25. REST API

The backend exposes REST APIs under the `/api` path.

Important operations include:

| Endpoint                      | Purpose                              |
| ----------------------------- | ------------------------------------ |
| `GET /api/status`             | Check current AI execution mode      |
| `GET /api/profile`            | Retrieve current profile             |
| `POST /api/profile`           | Update profile                       |
| `POST /api/profile/reset`     | Reset profile                        |
| `POST /api/resume/upload`     | Upload and process resume            |
| `POST /api/career-goal`       | Update target role / Job Description |
| `POST /api/orchestrate`       | Run the multi-agent pipeline         |
| `GET /api/orchestrate/latest` | Retrieve latest orchestration result |
| `POST /api/twin/simulate`     | Run future career simulation         |
| `GET /api/roles`              | Retrieve available roles             |

---

# 26. Typical User Workflow

```text
1. Open CareerTwin AI
        ↓
2. Enter profile information
   OR upload a resume
        ↓
3. Select target career role
        ↓
4. Optionally provide a Job Description
        ↓
5. Run Career Analysis
        ↓
6. Profile Agent analyzes readiness
        ↓
7. Skill Gap Agent identifies gaps
        ↓
8. Roadmap Agent creates a learning plan
        ↓
9. Project Agent recommends portfolio projects
        ↓
10. Simulation Agent performs What-If analysis
        ↓
11. Strategist Agent creates the final strategy
        ↓
12. Results are displayed on the dashboard
```

---

# 27. Main Features

## Career Dashboard

Displays the student's current Career Twin information and readiness.

## Skill Gap Analysis

Displays:

* Strong skills
* Developing skills
* Missing skills
* Priority skills
* Radar comparison

## Personalized Roadmap

Provides a five-phase learning and career-development plan.

## Project Recommendations

Provides practical projects related to the student's target role and skill gaps.

## Future Career Simulation

Allows the user to explore hypothetical upskilling scenarios.

## Career Strategy

Combines outputs from the multi-agent pipeline into a consolidated plan.

## Resume Processing

Allows PDF/TXT resumes to be processed into the Career Twin.

## Job Description Analysis

Allows a specific Job Description to influence skill-gap and career analysis.

---

# 28. Technology Stack

## Programming Language

* Python

## Backend

* FastAPI
* Uvicorn
* Pydantic

## Artificial Intelligence

* Google Gemini API
* Multi-agent architecture
* Deterministic heuristic AI

## Data Storage

* SQLite

## Frontend

* HTML
* CSS
* JavaScript

## Resume Processing

* PDF/Text parsing

## Environment Configuration

* python-dotenv

## Version Control

* Git
* GitHub

---

# 29. Installation

Clone the repository:

```bash
git clone https://github.com/revu2/CareerTwinAI.git
```

Move into the project directory:

```bash
cd CareerTwinAI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# 30. Environment Configuration

Create a local `.env` file.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=8000
HOST=127.0.0.1
```

The actual API key must never be committed to the public GitHub repository.

Use `.env.example` as the safe configuration template.

---

# 31. Running the Application

Start the application using:

```bash
python run.py
```

Open:

```text
http://127.0.0.1:8000
```

---

# 32. Running With Gemini

To use the external LLM:

1. Create a local `.env` file.
2. Add a valid Gemini API key.
3. Configure the Gemini model.
4. Start the application.

Example:

```env
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_MODEL=gemini-2.5-flash
```

When the key is available, the agents can use the external Google Gemini API.

---

# 33. Running Without Gemini

The application can also operate without an external Gemini API key.

If `GEMINI_API_KEY` is not configured:

```text
No Gemini API key
        ↓
Deterministic Python logic
        ↓
Fallback agent processing
```

This allows the core application workflow to remain functional without external API setup.

---

# 34. AI Execution Modes

The backend determines the mode based on whether a Gemini API key is configured.

### Gemini Mode

```text
GEMINI_API_KEY available
        ↓
Google Gemini
        ↓
LLM-powered agent generation
```

### Deterministic Mode

```text
GEMINI_API_KEY unavailable
        ↓
Built-in Python analysis
        ↓
Deterministic fallback
```

This dual-mode design is one of the important architectural features of the project.

---

# 35. Testing

The repository contains an automated test suite:

```text
tests/test_career_twin.py
```

Run the tests with:

```bash
python -m unittest tests/test_career_twin.py
```

The test suite is used to verify core Career Twin functionality.

---

# 36. Security

The Gemini API key is stored through an environment variable rather than directly in the source code.

The public repository should contain:

```text
.env.example
```

but should not contain:

```text
.env
```

The API key should remain private.

If a secret is accidentally exposed publicly, it should be revoked and replaced immediately.

---

# 37. Limitations

CareerTwin AI is an educational/project-level career analysis system.

The readiness score is an **AI-estimated project metric**, not an official employability measurement.

It does not guarantee:

* Job selection
* Internship selection
* Interview selection
* Employment
* Salary
* Career outcomes

The deterministic analysis depends on:

* Predefined role benchmarks
* User-provided profile information
* Skill matching rules
* Project information
* Education and certification information

LLM-generated results additionally depend on the configured Gemini model and the quality of the supplied information.

Future career simulation represents a hypothetical scenario and should not be interpreted as a guaranteed prediction.

---

# 38. Future Enhancements

Potential future improvements include:

* More career-role benchmarks
* More advanced resume parsing
* Additional external LLM providers
* Authentication and multi-user accounts
* Individual user workspaces
* Real-time job-market data
* Job-board integrations
* Retrieval-Augmented Generation (RAG)
* Vector database integration
* More advanced skill-level estimation
* Learning-resource recommendations
* Long-term progress tracking
* Enhanced agent observability
* Cloud scaling
* Additional career simulations

---

# 39. Project Structure

```text
CareerTwinAI/
│
├── backend/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── orchestrator.py
│   │   ├── profile_agent.py
│   │   ├── skill_gap_agent.py
│   │   ├── roadmap_agent.py
│   │   ├── project_agent.py
│   │   ├── simulation_agent.py
│   │   └── strategist_agent.py
│   │
│   ├── models/
│   │   ├── profile.py
│   │   └── agents.py
│   │
│   ├── data/
│   │   ├── role_benchmarks.py
│   │   └── sample_profiles.py
│   │
│   ├── services/
│   │   ├── storage.py
│   │   ├── resume_parser.py
│   │   └── gemini_client.py
│   │
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
│
├── tests/
│   └── test_career_twin.py
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

---

# 40. Live Application

The deployed CareerTwin AI application is available at:

https://careertwinai-production.up.railway.app

---

# 41. GitHub Repository

The source code is available at:

https://github.com/revu2/CareerTwinAI

---

# 42. Project Summary

CareerTwin AI demonstrates the practical use of **multi-agent AI combined with an external Large Language Model** to create a personalized career-support platform.

The application uses two complementary approaches:

```text
External LLM
Google Gemini
      +
Deterministic Python AI Logic
      ↓
Multi-Agent Career Twin
```

The six specialized agents are:

1. Digital Twin / Profile Agent
2. Skill Gap Agent
3. Career Roadmap Agent
4. Project & Experience Agent
5. Future Career Simulation Agent
6. Career Strategist Agent

The external Gemini LLM provides contextual and generative AI capabilities, while the deterministic layer provides controlled scoring, role benchmarking, skill matching, and fallback processing.

The resulting system demonstrates:

* External LLM integration
* Multi-agent architecture
* Agent orchestration
* Structured LLM outputs
* Deterministic AI processing
* Resume processing
* Job Description analysis
* Skill-gap analysis
* Personalized roadmaps
* Portfolio recommendations
* Career simulation
* REST API development
* Web-based visualization
* Persistent profile storage

CareerTwin AI therefore demonstrates how **external LLM capabilities and deterministic software logic can be combined within a practical multi-agent application**.
