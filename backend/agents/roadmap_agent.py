from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..models.profile import StudentProfile
from ..models.agents import (
    CareerRoadmapAgentOutput,
    RoadmapPhase,
    SkillGapAgentOutput
)

class CareerRoadmapAgent(BaseAgent):
    """
    AGENT 3: CAREER ROADMAP AGENT
    Responsibilities:
    - Use the Skill Gap Agent's output
    - Create a structured 5-phase personalized learning and career roadmap:
      Phase 1: Foundation
      Phase 2: Core Skills
      Phase 3: Advanced Skills
      Phase 4: Projects and Portfolio
      Phase 5: Interview and Placement Preparation
    """
    def __init__(self):
        super().__init__(
            name="Career Roadmap Agent",
            role_description="an expert engineering curriculum planner that generates 5-phase career upskilling roadmaps."
        )

    def generate_roadmap(self, profile: StudentProfile, gap_output: SkillGapAgentOutput) -> CareerRoadmapAgentOutput:
        target_role = profile.target_career or "Software Engineer"
        missing_str = ", ".join(gap_output.missing_skills[:6])
        priority_str = ", ".join(gap_output.priority_skills)

        prompt = f"""
        Create a 5-phase personalized career upskilling roadmap for a student targeting: '{target_role}'.

        Student Context:
        - Current Skills: {', '.join(profile.get_skills_list())}
        - High Priority Gaps to Close: {priority_str}
        - Missing Skills: {missing_str}

        Divide the roadmap strictly into these 5 phases:
        Phase 1: Foundation
        Phase 2: Core Skills
        Phase 3: Advanced Skills
        Phase 4: Projects and Portfolio
        Phase 5: Interview and Placement Preparation

        For each phase, specify:
        - skills_to_learn: list of skills
        - suggested_activities: list of hands-on activities
        - expected_outcome: concrete milestone outcome

        Return strict JSON matching this schema:
        {{
            "target_role": "{target_role}",
            "estimated_timeline": "6 Months (12-15 hrs/week)",
            "phases": [
                {{
                    "phase_number": 1,
                    "phase_name": "Phase 1: Foundation",
                    "timeframe": "Month 1 (Weeks 1-4)",
                    "skills_to_learn": ["Skill 1", "Skill 2"],
                    "suggested_activities": ["Activity 1", "Activity 2"],
                    "expected_outcome": "Outcome description"
                }},
                {{
                    "phase_number": 2,
                    "phase_name": "Phase 2: Core Skills",
                    "timeframe": "Month 2 (Weeks 5-8)",
                    "skills_to_learn": ["Skill 1", "Skill 2"],
                    "suggested_activities": ["Activity 1", "Activity 2"],
                    "expected_outcome": "Outcome description"
                }},
                {{
                    "phase_number": 3,
                    "phase_name": "Phase 3: Advanced Skills",
                    "timeframe": "Month 3 (Weeks 9-12)",
                    "skills_to_learn": ["Skill 1", "Skill 2"],
                    "suggested_activities": ["Activity 1", "Activity 2"],
                    "expected_outcome": "Outcome description"
                }},
                {{
                    "phase_number": 4,
                    "phase_name": "Phase 4: Projects and Portfolio",
                    "timeframe": "Month 4-5 (Weeks 13-20)",
                    "skills_to_learn": ["Skill 1", "Skill 2"],
                    "suggested_activities": ["Activity 1", "Activity 2"],
                    "expected_outcome": "Outcome description"
                }},
                {{
                    "phase_number": 5,
                    "phase_name": "Phase 5: Interview and Placement Preparation",
                    "timeframe": "Month 6 (Weeks 21-24)",
                    "skills_to_learn": ["Skill 1", "Skill 2"],
                    "suggested_activities": ["Activity 1", "Activity 2"],
                    "expected_outcome": "Outcome description"
                }}
            ]
        }}
        """

        raw_llm = self._invoke_llm(prompt, json_mode=True)
        parsed = self._parse_json_response(raw_llm)

        if parsed and "phases" in parsed and len(parsed["phases"]) == 5:
            phases = []
            for p in parsed["phases"]:
                phases.append(RoadmapPhase(
                    phase_number=int(p.get("phase_number", 1)),
                    phase_name=p.get("phase_name", "Phase"),
                    timeframe=p.get("timeframe", "Month"),
                    skills_to_learn=p.get("skills_to_learn", []),
                    suggested_activities=p.get("suggested_activities", []),
                    expected_outcome=p.get("expected_outcome", "")
                ))
            return CareerRoadmapAgentOutput(
                target_role=target_role,
                phases=phases,
                estimated_timeline=parsed.get("estimated_timeline", "6 Months (12-15 hrs/week)")
            )

        # Fallback Heuristic 5-Phase Generator tailored by role
        return self._heuristic_roadmap(profile, gap_output)

    def _heuristic_roadmap(self, profile: StudentProfile, gap_output: SkillGapAgentOutput) -> CareerRoadmapAgentOutput:
        target = profile.target_career or "Software Engineer"
        target_lower = target.lower()
        missing = gap_output.missing_skills
        p1 = missing[0] if len(missing) > 0 else "Object-Oriented Design & Data Structures"
        p2 = missing[1] if len(missing) > 1 else "REST APIs & Backend Frameworks"
        p3 = missing[2] if len(missing) > 2 else "Relational Databases & SQL Tuning"

        if "software" in target_lower or "backend" in target_lower or "full" in target_lower:
            phases = [
                RoadmapPhase(
                    phase_number=1,
                    phase_name="Phase 1: Foundation",
                    timeframe="Month 1 (Weeks 1-4)",
                    skills_to_learn=["Data Structures & Algorithms in Java/Python", "Object-Oriented Design Patterns", "Git & GitHub Version Control"],
                    suggested_activities=[
                        "Solve 30 core algorithmic problems (Arrays, HashMaps, Two-Pointers, Recursion)",
                        "Implement classic OOP design patterns (Factory, Singleton, Strategy) in clean code",
                        "Configure Git branching workflows and semantic commit messages"
                    ],
                    expected_outcome="Strong mastery of algorithmic problem solving and modular object-oriented coding principles."
                ),
                RoadmapPhase(
                    phase_number=2,
                    phase_name="Phase 2: Core Skills",
                    timeframe="Month 2 (Weeks 5-8)",
                    skills_to_learn=[p1, p2, "Relational Databases & SQL Indexing", "RESTful API Design Standards"],
                    suggested_activities=[
                        "Build and document a full CRUD REST API using Spring Boot / FastAPI / Node.js",
                        "Design normalized database schemas with foreign keys, indexes, and transactions",
                        "Write automated unit and integration tests with 80%+ code coverage"
                    ],
                    expected_outcome="Ability to engineer production-ready API services and optimize database queries."
                ),
                RoadmapPhase(
                    phase_number=3,
                    phase_name="Phase 3: Advanced Skills",
                    timeframe="Month 3 (Weeks 9-12)",
                    skills_to_learn=["Microservices Architecture", "Redis Caching & Session Stores", "Authentication (JWT & OAuth2)", "Docker Containerization"],
                    suggested_activities=[
                        "Implement distributed caching with Redis to reduce database read latency",
                        "Containerize multi-container services with Docker Compose",
                        "Implement secure authentication with token rotation and role-based access control"
                    ],
                    expected_outcome="Proficiency in modern backend infrastructure, distributed caching, and container orchestration."
                ),
                RoadmapPhase(
                    phase_number=4,
                    phase_name="Phase 4: Projects and Portfolio",
                    timeframe="Month 4-5 (Weeks 13-20)",
                    skills_to_learn=["CI/CD Pipelines (GitHub Actions)", "Cloud Deployment (AWS/Render)", "System Observability & Logging"],
                    suggested_activities=[
                        "Build and deploy a flagship fullstack project with live frontend, backend API, and database",
                        "Set up automated CI/CD pipelines running linting and automated test suites on pull requests",
                        "Author comprehensive README with architecture diagrams and API documentation"
                    ],
                    expected_outcome="Two production-grade software applications deployed live on public URLs with GitHub repositories."
                ),
                RoadmapPhase(
                    phase_number=5,
                    phase_name="Phase 5: Interview and Placement Preparation",
                    timeframe="Month 6 (Weeks 21-24)",
                    skills_to_learn=["High-Level System Design", "STAR Behavioral Interview Method", "LeetCode Medium Problem Patterns", "ATS Resume Formatting"],
                    suggested_activities=[
                        "Practice high-level system design trade-offs (Scalability, Sharding, Load Balancing)",
                        "Conduct 10 technical mock interviews covering Data Structures and System Design",
                        "Tailor resume bullet points using the Google XYZ impact formula"
                    ],
                    expected_outcome="Complete interview readiness for tier-1 tech companies and high-growth software startups."
                )
            ]
        elif "data" in target_lower or "analyt" in target_lower:
            phases = [
                RoadmapPhase(
                    phase_number=1,
                    phase_name="Phase 1: Foundation",
                    timeframe="Month 1 (Weeks 1-4)",
                    skills_to_learn=["Advanced Python (Pandas, NumPy)", "Probability & Inferential Statistics", "Data Exploration & Visualization"],
                    suggested_activities=[
                        "Perform exploratory data analysis on complex real-world datasets using Pandas and Seaborn",
                        "Implement statistical hypothesis testing (t-tests, ANOVA, Chi-Square)",
                        "Clean and normalize noisy real-world data with missing value imputation"
                    ],
                    expected_outcome="Strong intuition for statistical reasoning and advanced data manipulation."
                ),
                RoadmapPhase(
                    phase_number=2,
                    phase_name="Phase 2: Core Skills",
                    timeframe="Month 2 (Weeks 5-8)",
                    skills_to_learn=[p1, "Scikit-Learn Machine Learning Pipelines", "Advanced SQL (Window Functions, CTEs)", "Feature Engineering"],
                    suggested_activities=[
                        "Train supervised and unsupervised machine learning models with rigorous cross-validation",
                        "Write complex analytical SQL queries with partitioning and ranking functions",
                        "Evaluate models using PR-AUC, ROC-AUC, RMSE, and confusion matrices"
                    ],
                    expected_outcome="Ability to formulate data science problems, engineer predictive features, and train ML models."
                ),
                RoadmapPhase(
                    phase_number=3,
                    phase_name="Phase 3: Advanced Skills",
                    timeframe="Month 3 (Weeks 9-12)",
                    skills_to_learn=["Gradient Boosting (XGBoost / LightGBM)", "Time-Series Forecasting", "A/B Testing Experimentation", "FastAPI Model Serving"],
                    suggested_activities=[
                        "Tune hyperparameters for ensemble gradient boosting models using Optuna",
                        "Design and analyze simulated A/B tests calculating required sample sizes and statistical power",
                        "Deploy machine learning prediction endpoints via FastAPI"
                    ],
                    expected_outcome="Mastery of industry standard tabular ML algorithms, experimentation, and inference deployment."
                ),
                RoadmapPhase(
                    phase_number=4,
                    phase_name="Phase 4: Projects and Portfolio",
                    timeframe="Month 4-5 (Weeks 13-20)",
                    skills_to_learn=["Streamlit / Dash Visual Analytics", "Docker Containerization", "Data Storytelling & Executive Reports"],
                    suggested_activities=[
                        "Build an end-to-end interactive data science dashboard deployed publicly",
                        "Write detailed case study writeups linking statistical metrics to business ROI",
                        "Publish polished Jupyter Notebooks with clean visual storytelling on GitHub"
                    ],
                    expected_outcome="Two flagship data science portfolio projects with interactive live web demos."
                ),
                RoadmapPhase(
                    phase_number=5,
                    phase_name="Phase 5: Interview and Placement Preparation",
                    timeframe="Month 6 (Weeks 21-24)",
                    skills_to_learn=["Data Science System Design", "SQL Live Coding Practice", "Business Metric Case Studies", "STAR Behavioral Preparation"],
                    suggested_activities=[
                        "Practice 20 live SQL whiteboard challenges under timed conditions",
                        "Simulate open-ended ML system design interviews (e.g., Recommendation Engine, Fraud Detection)",
                        "Optimize data science resume highlighting quantifiable model impact"
                    ],
                    expected_outcome="Confidence and readiness for technical screening and hiring manager rounds."
                )
            ]
        else: # AI / ML Engineer
            phases = [
                RoadmapPhase(
                    phase_number=1,
                    phase_name="Phase 1: Foundation",
                    timeframe="Month 1 (Weeks 1-4)",
                    skills_to_learn=["Advanced Python (AsyncIO, OOP)", "Linear Algebra & Multivariable Calculus", "NumPy & Pandas Vectorization"],
                    suggested_activities=[
                        "Implement matrix multiplications and gradient descent backprop from scratch in Python",
                        "Complete 20 algorithmic coding problems on Data Structures",
                        "Build exploratory data analysis scripts visualizing mathematical distributions"
                    ],
                    expected_outcome="Strong mastery of Python internals and mathematical intuition required for AI algorithms."
                ),
                RoadmapPhase(
                    phase_number=2,
                    phase_name="Phase 2: Core Skills",
                    timeframe="Month 2 (Weeks 5-8)",
                    skills_to_learn=[p1, "PyTorch Tensors & Autograd", "Scikit-Learn Model Pipelines", "SQL Indexing"],
                    suggested_activities=[
                        "Train, evaluate, and tune classical machine learning models (Random Forests, Gradient Boosting)",
                        "Build a PyTorch Neural Network with custom layers, learning rate schedulers, and early stopping",
                        "Profile query performance on relational databases with multi-table JOINs"
                    ],
                    expected_outcome="Ability to build, train, and evaluate deep learning models with reproducible pipelines."
                ),
                RoadmapPhase(
                    phase_number=3,
                    phase_name="Phase 3: Advanced Skills",
                    timeframe="Month 3 (Weeks 9-12)",
                    skills_to_learn=["Hugging Face Transformers", "RAG (Retrieval-Augmented Generation)", "Vector Databases (ChromaDB/Pinecone)", "FastAPI Async Services"],
                    suggested_activities=[
                        "Implement a semantic search pipeline using sentence embeddings and dense vector indexing",
                        "Fine-tune an open-source LLM using LoRA / QLoRA for domain-specific question answering",
                        "Package model inference behind a production FastAPI gateway with request validation"
                    ],
                    expected_outcome="Demonstrated competence in modern Generative AI, RAG architecture, and production inference APIs."
                ),
                RoadmapPhase(
                    phase_number=4,
                    phase_name="Phase 4: Projects and Portfolio",
                    timeframe="Month 4-5 (Weeks 13-20)",
                    skills_to_learn=["Docker Containerization", "GitHub Actions CI/CD", "Cloud Deployment (AWS/GCP)", "Model Observability"],
                    suggested_activities=[
                        "Build and deploy a flagship fullstack AI application with real-time UI, backend API, and cloud hosting",
                        "Write multi-stage Dockerfiles and container-compose configurations",
                        "Author comprehensive documentation, architecture diagrams, and GitHub release showcases"
                    ],
                    expected_outcome="Two live, production-grade portfolio projects deployed online with clean public GitHub repositories."
                ),
                RoadmapPhase(
                    phase_number=5,
                    phase_name="Phase 5: Interview and Placement Preparation",
                    timeframe="Month 6 (Weeks 21-24)",
                    skills_to_learn=["AI System Design Whiteboarding", "STAR Behavioral Interview Method", "ATS Resume Optimization", "Algorithmic Problem Solving"],
                    suggested_activities=[
                        "Practice 10 mock interview rounds in the CareerTwin AI simulation terminal",
                        "Solve LeetCode Medium problem patterns (Binary Search, Graphs, Dynamic Programming)",
                        "Format resume bullet points using the Google XYZ impact formula with quantifiable metrics"
                    ],
                    expected_outcome="Interview readiness for top tech companies and high-growth AI startups."
                )
            ]

        return CareerRoadmapAgentOutput(
            target_role=target,
            phases=phases,
            estimated_timeline="6 Months (12-15 hrs/week)"
        )

roadmap_agent = CareerRoadmapAgent()
