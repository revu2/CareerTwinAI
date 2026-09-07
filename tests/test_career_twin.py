import unittest
import io
from fastapi.testclient import TestClient

from backend.main import app
from backend.models.profile import StudentProfile
from backend.agents.profile_agent import profile_agent
from backend.agents.skill_gap_agent import skill_gap_agent
from backend.agents.roadmap_agent import roadmap_agent
from backend.agents.project_agent import project_agent
from backend.agents.simulation_agent import simulation_agent
from backend.agents.strategist_agent import strategist_agent
from backend.agents.orchestrator import orchestrator
from backend.data.sample_profiles import SAMPLE_PROFILES

class TestCareerTwinSystem(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.revathi_profile = SAMPLE_PROFILES["revathi_ai"]
        self.unnamed_profile = StudentProfile(
            id="test_unnamed",
            name="",
            degree="B.Tech",
            branch="Computer Science Engineering",
            year_of_study="3rd Year",
            cgpa=8.5,
            current_skills=["Python", "SQL", "Git"],
            projects=["Web Project"],
            target_career="AI Engineer"
        )

    def test_health_and_status(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "healthy")

        res_status = self.client.get("/api/status")
        self.assertEqual(res_status.status_code, 200)
        data = res_status.json()
        self.assertIn("mode", data)
        self.assertIn("is_demo_mode", data)

    def test_sample_profiles(self):
        res = self.client.post("/api/profile/sample/revathi_ai")
        self.assertEqual(res.status_code, 200)
        profile = res.json()
        self.assertEqual(profile["name"], "Revathi")
        self.assertEqual(profile["target_career"], "AI Engineer")

    def test_deterministic_scoring_and_breakdown(self):
        out1 = profile_agent.analyze_profile(self.revathi_profile)
        out2 = profile_agent.analyze_profile(self.revathi_profile)
        
        # Test exact determinism: same input produces exact same score
        self.assertEqual(out1.readiness_estimate, out2.readiness_estimate)
        self.assertIsNotNone(out1.breakdown)
        self.assertGreater(out1.breakdown.required_skills_score, 0)
        self.assertGreater(out1.breakdown.projects_experience_score, 0)
        self.assertGreater(out1.breakdown.education_certs_score, 0)
        self.assertGreater(out1.breakdown.role_gaps_score, 0)
        
        # Breakdown sum matches readiness estimate
        expected_total = round(
            out1.breakdown.required_skills_score + 
            out1.breakdown.projects_experience_score + 
            out1.breakdown.education_certs_score + 
            out1.breakdown.role_gaps_score, 
            1
        )
        self.assertAlmostEqual(out1.readiness_estimate, expected_total, places=1)

    def test_career_goal_and_jd_update(self):
        res = self.client.post("/api/career-goal", json={
            "target_career": "Fullstack Software Engineer",
            "job_description": "Looking for React, TypeScript, Node.js, and PostgreSQL expertise."
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["target_role"], "Fullstack Software Engineer")
        self.assertIsNotNone(data["profile_agent_output"]["breakdown"])

    def test_resume_upload_endpoint(self):
        sample_resume_txt = (
            "Alex Smith\n"
            "B.Tech in Computer Science Engineering, 2026. CGPA: 8.8\n"
            "Skills: Python, PyTorch, SQL, FastAPI, Docker, Git\n"
            "Projects:\n"
            "• Built an automated multimodal RAG assistant using FastAPI and PyTorch.\n"
            "• Developed a real-time object detection model with YOLO and OpenCV.\n"
            "Certifications:\n"
            "• Deep Learning Specialization Coursera\n"
        )
        file_obj = io.BytesIO(sample_resume_txt.encode("utf-8"))
        res = self.client.post(
            "/api/resume/upload",
            files={"file": ("alex_resume.txt", file_obj, "text/plain")}
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["filename"], "alex_resume.txt")
        self.assertIn("Python", data["profile"]["current_skills"])

    def test_agent_2_skill_gap_agent(self):
        gap = skill_gap_agent.analyze_gaps(self.revathi_profile)
        self.assertIsNotNone(gap)
        self.assertGreater(len(gap.missing_skills), 0)
        self.assertGreater(len(gap.priority_skills), 0)

    def test_agent_3_roadmap_agent(self):
        gap = skill_gap_agent.analyze_gaps(self.revathi_profile)
        roadmap = roadmap_agent.generate_roadmap(self.revathi_profile, gap)
        self.assertEqual(len(roadmap.phases), 5)
        self.assertEqual(roadmap.phases[0].phase_name, "Phase 1: Foundation")
        self.assertEqual(roadmap.phases[4].phase_name, "Phase 5: Interview and Placement Preparation")

    def test_agent_4_project_agent(self):
        gap = skill_gap_agent.analyze_gaps(self.revathi_profile)
        projects = project_agent.recommend_projects(self.revathi_profile, gap)
        self.assertGreaterEqual(len(projects.recommended_projects), 3)

    def test_agent_6_future_simulation_agent(self):
        gap = skill_gap_agent.analyze_gaps(self.revathi_profile)
        sim = simulation_agent.simulate_future(
            profile=self.revathi_profile,
            gap_output=gap,
            selected_actions=[
                "Learn Machine Learning & Deep Learning (PyTorch, TensorFlow)",
                "Build & Deploy 2 Production AI Projects (RAG & Computer Vision)"
            ]
        )
        self.assertIsNotNone(sim)
        self.assertGreater(sim.future_simulated_twin.readiness_score, sim.current_twin.readiness_score)
        self.assertGreater(sim.score_improvement, 20.0)

    def test_agent_5_strategist_agent(self):
        p_out = profile_agent.analyze_profile(self.revathi_profile)
        g_out = skill_gap_agent.analyze_gaps(self.revathi_profile)
        r_out = roadmap_agent.generate_roadmap(self.revathi_profile, g_out)
        proj_out = project_agent.recommend_projects(self.revathi_profile, g_out)
        s_out = simulation_agent.simulate_future(self.revathi_profile, g_out, ["Learn Deep Learning"])
        
        strat = strategist_agent.formulate_strategy(self.revathi_profile, p_out, g_out, r_out, proj_out, s_out)
        self.assertIsNotNone(strat)
        self.assertGreater(len(strat.immediate_next_steps), 0)

    def test_full_orchestrator_pipeline(self):
        res = self.client.post("/api/orchestrate")
        self.assertEqual(res.status_code, 200)
        result = res.json()
        self.assertEqual(len(result["executed_agents"]), 6)

if __name__ == "__main__":
    unittest.main()
