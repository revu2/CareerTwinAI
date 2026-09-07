from typing import Dict, Any, List

ROLE_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "AI Engineer": {
        "title": "AI Engineer",
        "description": "Designs, trains, deploys, and scales machine learning and generative AI models into production applications.",
        "core_skills": [
            "Python", "PyTorch", "TensorFlow", "Scikit-Learn", "FastAPI", 
            "Docker", "Transformers", "LLMs", "RAG Architecture", "Vector Databases",
            "Git", "SQL", "Pandas", "MLOps", "Model Evaluation"
        ],
        "important_skills": [
            "LangChain", "Hugging Face", "CUDA/GPU Optimization", "Kubernetes",
            "Weights & Biases", "API Design", "ONNX", "Cloud (AWS/GCP/Azure)"
        ],
        "nice_to_have_skills": [
            "C++", "Ray", "Triton Inference Server", "MLflow", "Fine-tuning LoRA/QLoRA"
        ],
        "radar_categories": {
            "Languages (Python/C++)": 90,
            "ML Frameworks (PyTorch/Transformers)": 85,
            "GenAI & RAG Systems": 85,
            "Data Engineering & SQL": 75,
            "MLOps & Deployment (Docker/CI)": 70,
            "CS & Math Fundamentals": 80
        },
        "target_certifications": [
            {"title": "AWS Certified Machine Learning - Specialty", "issuer": "Amazon Web Services"},
            {"title": "Google Professional Machine Learning Engineer", "issuer": "Google Cloud"},
            {"title": "Deep Learning Specialization", "issuer": "DeepLearning.AI"}
        ]
    },
    "AI/ML Engineer": {
        "title": "AI/ML Engineer",
        "description": "Designs, trains, deploys, and scales machine learning and generative AI models into production applications.",
        "core_skills": [
            "Python", "PyTorch", "TensorFlow", "Scikit-Learn", "FastAPI", 
            "Docker", "Transformers", "LLMs", "RAG Architecture", "Vector Databases",
            "Git", "SQL", "Pandas", "MLOps", "Model Evaluation"
        ],
        "important_skills": [
            "LangChain", "Hugging Face", "CUDA/GPU Optimization", "Kubernetes",
            "Weights & Biases", "API Design", "ONNX", "Cloud (AWS/GCP/Azure)"
        ],
        "nice_to_have_skills": [
            "C++", "Ray", "Triton Inference Server", "MLflow", "Fine-tuning LoRA/QLoRA"
        ],
        "radar_categories": {
            "Languages (Python/C++)": 90,
            "ML Frameworks (PyTorch/Transformers)": 85,
            "GenAI & RAG Systems": 85,
            "Data Engineering & SQL": 75,
            "MLOps & Deployment (Docker/CI)": 70,
            "CS & Math Fundamentals": 80
        },
        "target_certifications": [
            {"title": "AWS Certified Machine Learning - Specialty", "issuer": "Amazon Web Services"},
            {"title": "Google Professional Machine Learning Engineer", "issuer": "Google Cloud"},
            {"title": "Deep Learning Specialization", "issuer": "DeepLearning.AI"}
        ]
    },
    "Software Engineer": {
        "title": "Software Engineer",
        "description": "Designs, develops, tests, and maintains robust, scalable software systems across frontend, backend, APIs, and databases.",
        "core_skills": [
            "Java", "Python", "C++", "Data Structures", "Algorithms", "Object-Oriented Programming",
            "SQL", "PostgreSQL", "REST APIs", "Git", "Docker", "System Design", "Linux"
        ],
        "important_skills": [
            "Spring Boot", "FastAPI", "Node.js", "Redis", "Microservices",
            "Unit Testing (JUnit/Pytest)", "CI/CD Pipelines", "Cloud Basics (AWS/GCP)"
        ],
        "nice_to_have_skills": [
            "Kubernetes", "Kafka", "GraphQL", "NoSQL", "Distributed Systems"
        ],
        "radar_categories": {
            "Core Programming & OOP": 90,
            "Data Structures & Algorithms": 90,
            "Backend APIs & Frameworks": 80,
            "Databases & SQL": 80,
            "System Design & Architecture": 75,
            "DevOps, Git & Tooling": 75
        },
        "target_certifications": [
            {"title": "Oracle Certified Professional: Java SE Developer", "issuer": "Oracle"},
            {"title": "AWS Certified Developer - Associate", "issuer": "Amazon Web Services"}
        ]
    },
    "Fullstack Software Engineer": {
        "title": "Fullstack Software Engineer",
        "description": "Builds scalable, end-to-end web applications covering user interfaces, REST/GraphQL APIs, databases, and deployment.",
        "core_skills": [
            "JavaScript", "TypeScript", "React", "Node.js", "Python", 
            "FastAPI", "SQL", "PostgreSQL", "HTML5/CSS3", "Tailwind CSS",
            "Git", "REST APIs", "Docker", "Authentication (JWT/OAuth)", "State Management"
        ],
        "important_skills": [
            "Next.js", "Redis", "CI/CD Pipelines", "GraphQL", "Prisma/ORM",
            "Unit Testing (Jest/Pytest)", "AWS/Vercel", "WebSockets"
        ],
        "nice_to_have_skills": [
            "Microservices", "Kubernetes", "Kafka", "Accessibility (a11y)", "System Architecture"
        ],
        "radar_categories": {
            "Frontend (React/TypeScript/CSS)": 85,
            "Backend (Node/FastAPI/APIs)": 85,
            "Databases & Storage (SQL/Redis)": 75,
            "Cloud, Docker & DevOps": 70,
            "Testing & Code Quality": 75,
            "System Design & Architecture": 75
        },
        "target_certifications": [
            {"title": "AWS Certified Developer - Associate", "issuer": "Amazon Web Services"},
            {"title": "Meta Front-End / Back-End Developer Professional", "issuer": "Meta"}
        ]
    },
    "Backend Engineer": {
        "title": "Backend Engineer",
        "description": "Architects high-performance server-side services, data pipelines, distributed systems, and robust database layers.",
        "core_skills": [
            "Python", "Java", "Go", "FastAPI", "SQL", "PostgreSQL",
            "Redis", "Docker", "REST APIs", "Git", "Data Modeling",
            "Authentication & Security", "Asynchronous Programming", "Microservices"
        ],
        "important_skills": [
            "Kafka/RabbitMQ", "gRPC", "Kubernetes", "AWS (EC2/S3/RDS/Lambda)",
            "System Design", "Database Indexing & Query Tuning", "CI/CD", "Pytest/JUnit"
        ],
        "nice_to_have_skills": [
            "Cassandra/DynamoDB", "Elasticsearch", "Prometheus/Grafana", "Distributed Tracing"
        ],
        "radar_categories": {
            "Core Languages (Python/Go/Java)": 90,
            "API & Microservices Architecture": 85,
            "Databases & Caching (SQL/Redis)": 85,
            "Distributed Systems & Messaging": 75,
            "Cloud, Containers & Infrastructure": 75,
            "Security & Performance Tuning": 80
        },
        "target_certifications": [
            {"title": "AWS Certified Solutions Architect - Associate", "issuer": "Amazon Web Services"},
            {"title": "CKA: Certified Kubernetes Administrator", "issuer": "CNCF"}
        ]
    },
    "Data Scientist": {
        "title": "Data Scientist",
        "description": "Applies statistical modeling, exploratory data analysis, predictive machine learning, and business storytelling to extract actionable insights.",
        "core_skills": [
            "Python", "R", "SQL", "Pandas", "NumPy", "Scikit-Learn",
            "Data Visualization (Matplotlib/Seaborn)", "Statistics & Probability",
            "Feature Engineering", "Hypothesis Testing / A/B Testing", "Git"
        ],
        "important_skills": [
            "XGBoost/LightGBM", "Tableau/PowerBI", "PySpark", "BigQuery/Snowflake",
            "Storytelling & Business Metrics", "Time Series Analysis", "NLP Basics"
        ],
        "nice_to_have_skills": [
            "Deep Learning", "Airflow", "Docker", "Causal Inference"
        ],
        "radar_categories": {
            "Statistical Modeling & A/B Testing": 90,
            "Python/R Data Stack (Pandas/Numpy)": 90,
            "SQL & Advanced Data Extraction": 85,
            "Machine Learning Algorithms": 80,
            "Data Storytelling & Visualization": 80,
            "Big Data & Pipeline Tools": 65
        },
        "target_certifications": [
            {"title": "IBM Data Science Professional Certificate", "issuer": "IBM"},
            {"title": "Google Advanced Data Analytics Certificate", "issuer": "Google"}
        ]
    },
    "Cloud & DevOps Engineer": {
        "title": "Cloud & DevOps Engineer",
        "description": "Automates continuous integration/delivery, provisions cloud infrastructure as code, manages container orchestration, and ensures high availability.",
        "core_skills": [
            "Linux", "Bash/Shell", "Docker", "Kubernetes", "AWS/GCP/Azure",
            "Terraform", "CI/CD (GitHub Actions/GitLab)", "Git", "Networking & DNS",
            "Monitoring (Prometheus/Grafana)", "Security & IAM"
        ],
        "important_skills": [
            "Python/Go scripting", "Ansible", "Helm", "ArgoCD / GitOps",
            "ELK/Loki Logging", "Load Balancing", "CloudFormation"
        ],
        "nice_to_have_skills": [
            "Service Mesh (Istio)", "Cost Optimization (FinOps)", "Vault"
        ],
        "radar_categories": {
            "Linux & Shell Scripting": 90,
            "Containers & K8s Orchestration": 85,
            "Infrastructure as Code (Terraform)": 85,
            "CI/CD Automation Pipelines": 85,
            "Cloud Architecture (AWS/GCP)": 85,
            "Observability & Reliability (SRE)": 75
        },
        "target_certifications": [
            {"title": "AWS Certified DevOps Engineer - Professional", "issuer": "Amazon Web Services"},
            {"title": "CKA: Certified Kubernetes Administrator", "issuer": "Linux Foundation"},
            {"title": "HashiCorp Certified: Terraform Associate", "issuer": "HashiCorp"}
        ]
    },
    "Cybersecurity Analyst": {
        "title": "Cybersecurity Analyst",
        "description": "Protects networks, applications, and cloud systems by monitoring threat intelligence, conducting vulnerability assessments, and managing incident response.",
        "core_skills": [
            "Networking (TCP/IP, DNS, OSI)", "Linux/Windows Security", "SIEM (Splunk/Sentinel)",
            "Vulnerability Assessment (Nessus/Nmap)", "Wireshark", "OWASP Top 10",
            "Incident Response Frameworks", "Firewalls/IDS/IPS", "Python/Bash Scripting"
        ],
        "important_skills": [
            "SOC Operations", "Threat Hunting", "Cryptography Basics", "Burp Suite",
            "MITRE ATT&CK Framework", "Endpoint Detection & Response (EDR)"
        ],
        "nice_to_have_skills": [
            "Cloud Security (AWS Security Hub)", "Reverse Engineering", "Penetration Testing"
        ],
        "radar_categories": {
            "Network Protocols & Packet Analysis": 85,
            "Security Operations & SIEM": 85,
            "Vulnerability Management & PenTesting": 80,
            "Threat Intelligence & MITRE ATT&CK": 80,
            "Application & Web Security (OWASP)": 80,
            "Scripting & Automation": 70
        },
        "target_certifications": [
            {"title": "CompTIA Security+", "issuer": "CompTIA"},
            {"title": "Certified Information Systems Security Professional (CISSP)", "issuer": "ISC2"},
            {"title": "Certified Ethical Hacker (CEH)", "issuer": "EC-Council"}
        ]
    }
}

def get_role_benchmark(role_name: str) -> Dict[str, Any]:
    """Retrieve benchmark configuration for a role or match closest."""
    normalized = role_name.strip().lower()
    
    # 1. Exact case-insensitive match
    for key, data in ROLE_BENCHMARKS.items():
        if key.lower() == normalized:
            return data
            
    # 2. Substring matching
    if "software" in normalized or "sde" in normalized or "swe" in normalized:
        return ROLE_BENCHMARKS["Software Engineer"]
    if "full" in normalized or "frontend" in normalized or "web" in normalized:
        return ROLE_BENCHMARKS["Fullstack Software Engineer"]
    if "data" in normalized or "analytics" in normalized:
        return ROLE_BENCHMARKS["Data Scientist"]
    if "devops" in normalized or "cloud" in normalized or "infra" in normalized or "sre" in normalized:
        return ROLE_BENCHMARKS["Cloud & DevOps Engineer"]
    if "security" in normalized or "cyber" in normalized:
        return ROLE_BENCHMARKS["Cybersecurity Analyst"]
    if "ai" in normalized or "ml" in normalized or "machine" in normalized or "deep" in normalized:
        return ROLE_BENCHMARKS["AI Engineer"]
    if "backend" in normalized:
        return ROLE_BENCHMARKS["Backend Engineer"]

    for key, data in ROLE_BENCHMARKS.items():
        if key.lower() in normalized or normalized in key.lower():
            return data
    
    # Generic fallback benchmark for custom roles
    return {
        "title": role_name,
        "description": f"Professional requirements and core competencies for {role_name}.",
        "core_skills": ["Python", "JavaScript", "SQL", "Git", "System Design", "Problem Solving", "APIs", "Data Structures"],
        "important_skills": ["Docker", "Cloud Basics", "Unit Testing", "CI/CD", "Performance Optimization"],
        "nice_to_have_skills": ["Microservices", "Security", "Architecture"],
        "radar_categories": {
            "Core Programming & Languages": 80,
            "Domain-Specific Tools & Frameworks": 80,
            "System Architecture & Design": 75,
            "Data Management & Persistence": 75,
            "DevOps, Testing & Quality": 70,
            "Problem Solving & Collaboration": 80
        },
        "target_certifications": [
            {"title": "Industry Standard Professional Certificate", "issuer": "Leading Tech Provider"}
        ]
    }

def get_all_roles() -> List[str]:
    return list(ROLE_BENCHMARKS.keys())
