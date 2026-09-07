import uuid
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from ..models.profile import StudentProfile
from ..models.agents import (
    InterviewQuestion,
    InterviewFeedback,
    InterviewSession
)
from ..data.role_benchmarks import get_role_benchmark

class InterviewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="AI Mock Interviewer & Simulation Agent",
            role_description="a seasoned engineering hiring manager conducting rigorous technical and behavioral interviews."
        )

    def create_session(self, profile: StudentProfile, count: int = 3) -> InterviewSession:
        target_role = profile.target_career.role_title
        benchmark = get_role_benchmark(target_role)
        sample_q = benchmark.get("sample_interview_questions", [])

        skills_str = ', '.join(profile.skills.all_technical_skills())
        projs_str = str([p.title for p in profile.projects])

        prompt = f"""
Generate {count} realistic, challenging interview questions for a student interviewing for: '{target_role}'.
Student skills: {skills_str}
Projects: {projs_str}

Include 1 Core Technical Deep-Dive, 1 System Design / Architecture, and 1 Behavioral (STAR).

Return strictly valid JSON matching this schema:
{{
    "questions": [
        {{
            "question_id": "q1",
            "category": "Technical",
            "difficulty": "Medium",
            "question_text": "The full interview question prompt",
            "context_hint": "A subtle hint to guide the candidate",
            "sample_structure": "Recommended response structure"
        }}
    ]
}}
"""

        raw_llm = self._invoke_llm(prompt, json_mode=True)
        parsed = self._parse_json_response(raw_llm)

        questions = []
        if parsed and "questions" in parsed and len(parsed["questions"]) > 0:
            for q in parsed["questions"]:
                questions.append(InterviewQuestion(
                    question_id=str(uuid.uuid4())[:8],
                    category=q.get("category", "Technical"),
                    difficulty=q.get("difficulty", "Medium"),
                    question_text=q.get("question_text", "Explain your technical approach."),
                    context_hint=q.get("context_hint", ""),
                    sample_structure=q.get("sample_structure", "")
                ))
        else:
            for q in sample_q[:count]:
                questions.append(InterviewQuestion(
                    question_id=str(uuid.uuid4())[:8],
                    category=q.get("category", "Technical"),
                    difficulty=q.get("difficulty", "Medium"),
                    question_text=q.get("question_text", "Explain a complex technical topic."),
                    context_hint=q.get("context_hint", ""),
                    sample_structure=q.get("sample_structure", "")
                ))

        session = InterviewSession(
            session_id=str(uuid.uuid4())[:8],
            target_role=target_role,
            questions=questions,
            current_question_index=0,
            transcripts=[],
            average_score=0.0,
            completed=False
        )
        return session

    def evaluate_answer(
        self,
        question: InterviewQuestion,
        student_answer: str,
        target_role: str
    ) -> InterviewFeedback:
        prompt = f"""
Evaluate this student's response in an interview for the role: '{target_role}'.

Question: "{question.question_text}"
Category: {question.category} ({question.difficulty})
Candidate Answer: "{student_answer}"

Provide a critical yet constructive evaluation.

Return strictly valid JSON matching this schema:
{{
    "score_overall": 80,
    "score_technical_accuracy": 80,
    "score_structure_clarity": 80,
    "score_impact_star": 80,
    "what_went_well": [
        "Specific strength 1", "Specific strength 2"
    ],
    "areas_to_improve": [
        "Constructive critique 1", "Missing keyword or detail 2"
    ],
    "model_answer": "A concise, 3-4 sentence exemplary answer demonstrating mastery.",
    "coaching_tip": "One memorable takeaway for next interview round."
}}
"""

        raw_llm = self._invoke_llm(prompt, json_mode=True)
        parsed = self._parse_json_response(raw_llm)

        if parsed and "score_overall" in parsed:
            return InterviewFeedback(
                score_overall=int(parsed.get("score_overall", 75)),
                score_technical_accuracy=int(parsed.get("score_technical_accuracy", 75)),
                score_structure_clarity=int(parsed.get("score_structure_clarity", 75)),
                score_impact_star=int(parsed.get("score_impact_star", 75)),
                what_went_well=parsed.get("what_went_well", ["Demonstrated clear communication."]),
                areas_to_improve=parsed.get("areas_to_improve", ["Add more quantitative metrics."]),
                model_answer=parsed.get("model_answer", "A model answer demonstrating structured breakdown and trade-offs."),
                coaching_tip=parsed.get("coaching_tip", "Always state trade-offs explicitly before settling on a solution.")
            )

        # Fallback Heuristic Evaluator
        return self._heuristic_evaluation(question, student_answer)

    def _heuristic_evaluation(self, question: InterviewQuestion, answer: str) -> InterviewFeedback:
        words = len(answer.split())
        
        if words < 15:
            tech_acc = 50
            clarity = 55
            impact = 45
            overall = 50
            critique = ["Answer was too brief. Expand with concrete technical mechanisms and trade-offs."]
            praise = ["Direct attempt at the prompt."]
        elif words < 50:
            tech_acc = 72
            clarity = 75
            impact = 70
            overall = 72
            critique = ["Good initial direction; incorporate specific edge cases, scaling limits, or metrics."]
            praise = ["Clear core idea and focused vocabulary."]
        else:
            tech_acc = 86
            clarity = 88
            impact = 84
            overall = 86
            critique = ["Consider summarizing key takeaways at the end to reinforce your thesis."]
            praise = ["Thorough explanation with strong depth and structured reasoning.", "Effective use of terminology."]

        return InterviewFeedback(
            score_overall=overall,
            score_technical_accuracy=tech_acc,
            score_structure_clarity=clarity,
            score_impact_star=impact,
            what_went_well=praise,
            areas_to_improve=critique,
            model_answer=f"When approaching '{question.question_text}', an ideal response frames the objective, steps through architectural components with explicit trade-offs (e.g. latency vs consistency), and quantifies production impact.",
            coaching_tip="Structure your answers with the 3-step cadence: 1. State the core premise -> 2. Walk through key mechanisms -> 3. Discuss real-world edge cases."
        )

interview_agent = InterviewAgent()
