from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..models.profile import StudentProfile
from ..models.agents import (
    ProjectAgentOutput,
    ProjectRecommendation,
    SkillGapAgentOutput
)

class ProjectAndExperienceAgent(BaseAgent):
    """
    AGENT 4: PROJECT AND EXPERIENCE AGENT
    Responsibilities:
    - Recommend projects based on target role, missing skills, and current experience
    - Recommend practical portfolio-building activities
    - Suggest internship preparation areas
    """
    def __init__(self):
        super().__init__(
            name="Project & Experience Agent",
            role_description="a technical portfolio architect and practical engineering project advisor."
        )

    def recommend_projects(self, profile: StudentProfile, gap_output: SkillGapAgentOutput) -> ProjectAgentOutput:
        target_role = profile.target_career or "Software Engineer"
        missing_skills_str = ", ".join(gap_output.missing_skills[:5])

        prompt = f"""
        Recommend 3 practical, production-oriented portfolio projects for a student aiming to become a '{target_role}'.

        Student Context:
        - Current Skills: {', '.join(profile.get_skills_list())}
        - Key Missing Skills to Demonstrate: {missing_skills_str}
        - Current Projects: {'; '.join(profile.projects)}

        For each project, include:
        - title: Name of project
        - difficulty: "Beginner", "Intermediate", or "Advanced"
        - skills_gained: list of skills
        - why_it_helps: Clear explanation of how it impresses recruiters for {target_role}
        - architecture_overview: High-level architecture breakdown
        - deliverable: Tangible GitHub repository / live demo

        Also provide:
        - portfolio_activities: 3 practical tips for organizing their GitHub and portfolio
        - internship_preparation_areas: 3 areas to focus on for internship interview readiness.

        Return strict JSON matching this schema:
        {{
            "target_role": "{target_role}",
            "recommended_projects": [
                {{
                    "title": "Project 1 Title",
                    "difficulty": "Intermediate",
                    "skills_gained": ["Skill1", "Skill2"],
                    "why_it_helps": "Why it helps the career goal",
                    "architecture_overview": "Architecture summary",
                    "deliverable": "Working GitHub repo + demo"
                }}
            ],
            "portfolio_activities": [
                "Tip 1", "Tip 2", "Tip 3"
            ],
            "internship_preparation_areas": [
                "Area 1", "Area 2", "Area 3"
            ]
        }}
        """

        raw_llm = self._invoke_llm(prompt, json_mode=True)
        parsed = self._parse_json_response(raw_llm)

        if parsed and "recommended_projects" in parsed and len(parsed["recommended_projects"]) > 0:
            recs = []
            for p in parsed["recommended_projects"]:
                recs.append(ProjectRecommendation(
                    title=p.get("title", "Portfolio Project"),
                    difficulty=p.get("difficulty", "Intermediate"),
                    skills_gained=p.get("skills_gained", []),
                    why_it_helps=p.get("why_it_helps", ""),
                    architecture_overview=p.get("architecture_overview", ""),
                    deliverable=p.get("deliverable", "")
                ))
            return ProjectAgentOutput(
                target_role=target_role,
                recommended_projects=recs,
                portfolio_activities=parsed.get("portfolio_activities", []),
                internship_preparation_areas=parsed.get("internship_preparation_areas", [])
            )

        # Fallback Heuristic Project Recommendations tailored by role
        return self._heuristic_projects(profile, gap_output)

    def _heuristic_projects(self, profile: StudentProfile, gap_output: SkillGapAgentOutput) -> ProjectAgentOutput:
        target = profile.target_career or "Software Engineer"
        target_lower = target.lower()

        if "software" in target_lower or "backend" in target_lower or "full" in target_lower:
            recs = [
                ProjectRecommendation(
                    title="DevCollab: Real-Time Microservices Collaboration Engine",
                    difficulty="Intermediate",
                    skills_gained=["Java/Spring Boot / Node.js", "PostgreSQL", "Redis Caching", "Docker", "REST & WebSockets"],
                    why_it_helps=f"Proves to {target} recruiters that you can design multi-tier backend architectures, handle concurrent client sessions, and implement clean database indexing.",
                    architecture_overview="React Client -> API Gateway (JWT Auth) -> Event-Driven Microservices (Spring Boot / Node) -> PostgreSQL + Redis Cache -> Dockerized Deployment.",
                    deliverable="GitHub repository with Docker Compose, automated API integration tests (Postman/Pytest/JUnit), and live demo on Render/AWS."
                ),
                ProjectRecommendation(
                    title="DataFlow: Distributed Task Queue & Rate-Limiter Gateway",
                    difficulty="Advanced",
                    skills_gained=["Python / Go", "Redis", "FastAPI", "Docker", "System Design"],
                    why_it_helps="Demonstrates deep understanding of asynchronous task processing, distributed locks, rate-limiting algorithms (Token Bucket), and fault tolerance.",
                    architecture_overview="Inbound Gateway -> Token Bucket Rate Limiter -> Redis Task Broker -> Worker Pool -> Storage & Metrics Prometheus Exporter.",
                    deliverable="Production CLI tool and containerized service benchmarking 10,000 req/sec with latency profiling documentation."
                ),
                ProjectRecommendation(
                    title="CleanStore: Scalable E-Commerce Inventory & Order API",
                    difficulty="Beginner",
                    skills_gained=["SQL", "PostgreSQL", "REST APIs", "Git", "Unit Testing"],
                    why_it_helps="Demonstrates clean code principles, ACID transaction isolation, relational database normalization, and robust error handling.",
                    architecture_overview="RESTful API Endpoints -> Service Layer -> Repository Pattern -> PostgreSQL with schema migrations and seed scripts.",
                    deliverable="Tested backend service with 90%+ code coverage, Swagger OpenAPI documentation, and CI/CD workflow."
                )
            ]
        elif "data" in target_lower or "analyt" in target_lower:
            recs = [
                ProjectRecommendation(
                    title="InsightLens: Automated Customer Churn & Lifetime Value Predictor",
                    difficulty="Intermediate",
                    skills_gained=["Python", "Pandas", "Scikit-Learn", "XGBoost", "Streamlit", "SQL"],
                    why_it_helps="Demonstrates rigorous exploratory data analysis, feature engineering, cross-validation, and translating model metrics into revenue impact.",
                    architecture_overview="Raw Event Ingestion -> SQL Aggregation -> Feature Engineering Pipeline -> XGBoost / Random Forest -> Interactive Streamlit Dashboard.",
                    deliverable="Interactive web application with ROC-AUC evaluation curves, feature importance charts, and GitHub code repository."
                ),
                ProjectRecommendation(
                    title="MarketPulse: Algorithmic Time-Series Forecasting Engine",
                    difficulty="Advanced",
                    skills_gained=["Python", "Prophet / ARIMA", "Statsmodels", "Plotly", "FastAPI"],
                    why_it_helps="Proves competence in non-stationary time series modeling, trend/seasonality decomposition, and deploying predictive APIs.",
                    architecture_overview="Historical Time Series Ingestion -> Stationarity Testing (ADF) -> Forecasting Models -> FastAPI Serving -> Plotly Visualizations.",
                    deliverable="Containerized forecasting API with automated backtesting reports and confidence interval graphs."
                ),
                ProjectRecommendation(
                    title="DataWhiz: End-to-End SQL Analytics & Cohort Retention Engine",
                    difficulty="Beginner",
                    skills_gained=["SQL", "PostgreSQL", "Pandas", "Data Storytelling"],
                    why_it_helps="Shows mastery of complex SQL window functions, CTEs, self-joins, and business cohort retention analysis.",
                    architecture_overview="Multi-million row synthetic dataset -> Complex SQL Analytics -> Jupyter Notebook Storytelling with Executive Summary.",
                    deliverable="GitHub repository with reproducible SQL scripts, cohort retention heatmaps, and business decision insights."
                )
            ]
        else: # AI / ML Engineer Default
            recs = [
                ProjectRecommendation(
                    title="DocuBrain: Production Multimodal RAG Assistant",
                    difficulty="Intermediate",
                    skills_gained=["FastAPI", "PyTorch / Transformers", "ChromaDB", "Docker", "Prompt Engineering"],
                    why_it_helps=f"Proves to {target} hiring teams that you can build beyond toy scripts by deploying a working vector search pipeline with sub-second retrieval latency.",
                    architecture_overview="Document Chunking Pipeline -> BGE Embeddings -> ChromaDB Vector Index -> FastAPI Asynchronous Gateway -> Streamlit / React Web Client.",
                    deliverable="Public GitHub repository with Dockerfile, benchmark evaluation metrics (Precision/Recall), and live deployment."
                ),
                ProjectRecommendation(
                    title="VisionStream: Real-Time Edge Video Anomaly Detection",
                    difficulty="Advanced",
                    skills_gained=["PyTorch", "YOLOv8", "OpenCV", "TensorRT / ONNX Quantization", "WebSockets"],
                    why_it_helps="Demonstrates deep learning model optimization and low-latency computer vision inference under compute constraints.",
                    architecture_overview="Live Video Ingestion (OpenCV) -> YOLOv8 Detection -> TensorRT FP16 Quantized Inference -> Event Trigger -> Real-time WebSocket Alerting.",
                    deliverable="Containerized service processing 30+ FPS video stream with interactive dashboard and latency profiling charts."
                ),
                ProjectRecommendation(
                    title="AutoTuneML: Automated ML Model Hyperparameter Search & Benchmarking Engine",
                    difficulty="Intermediate",
                    skills_gained=["Python", "Scikit-Learn", "Optuna", "Pandas", "SQLAlchemy", "Plotly"],
                    why_it_helps="Shows solid understanding of statistical machine learning rigor, cross-validation, feature engineering, and automated evaluation.",
                    architecture_overview="Dataset Ingestion -> Automated Preprocessing & Scaling -> Bayesian Hyperparameter Optimization (Optuna) -> Interactive Evaluation Report.",
                    deliverable="Python PyPI package / CLI tool with automated test suite (Pytest) and HTML benchmark reports."
                )
            ]

        portfolio_tips = [
            "Structure every GitHub repository with a clear README containing: Problem Statement, System Architecture Diagram, Installation Guide, and Quantified Performance Metrics.",
            "Include a 45-second GIF / Loom video walkthrough at the top of your repository to grab the attention of recruiters within 5 seconds.",
            "Write modular, clean code following industry conventions with docstrings and unit test coverage."
        ]

        internship_areas = [
            f"Master core {target} technical foundations and coding interview problem patterns.",
            "Be prepared to explain architectural trade-offs: why you selected specific frameworks, data structures, or database indexing strategies.",
            "Practice live whiteboard and behavioral questions using the STAR framework."
        ]

        return ProjectAgentOutput(
            target_role=target,
            recommended_projects=recs,
            portfolio_activities=portfolio_tips,
            internship_preparation_areas=internship_areas
        )

project_agent = ProjectAndExperienceAgent()
