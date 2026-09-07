import sqlite3
import json
from typing import Optional, Dict, Any, List
from pathlib import Path
from ..config import DATABASE_PATH
from ..models.profile import StudentProfile
from ..data.sample_profiles import SAMPLE_PROFILES

class StorageService:
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS state_store (
                    profile_id TEXT,
                    state_key TEXT,
                    state_value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (profile_id, state_key)
                )
            """)
            conn.commit()

            # Ensure default profile exists with clean initial state
            cursor.execute("SELECT id FROM profiles WHERE id = 'default_student'")
            if not cursor.fetchone():
                default_profile = StudentProfile(
                    id="default_student",
                    name="",
                    degree="B.Tech",
                    branch="Computer Science Engineering",
                    year_of_study="3rd Year",
                    cgpa=None,
                    current_skills=[],
                    projects=[],
                    certifications=[],
                    career_interests=[],
                    target_career="Software Engineer",
                    dream_company="",
                    job_description="",
                    resume_filename="",
                    raw_resume_text="",
                    readiness_score=0.0
                )
                cursor.execute(
                    "INSERT INTO profiles (id, data) VALUES (?, ?)",
                    ("default_student", default_profile.model_dump_json())
                )
                conn.commit()

    def get_profile(self, profile_id: str = "default_student") -> Optional[StudentProfile]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM profiles WHERE id = ?", (profile_id,))
            row = cursor.fetchone()
            if row:
                data_dict = json.loads(row["data"])
                return StudentProfile(**data_dict)
            
            if profile_id == "default_student":
                profile = StudentProfile(
                    id="default_student",
                    name="",
                    target_career="Software Engineer",
                    readiness_score=0.0,
                    resume_filename="",
                    current_skills=[],
                    projects=[],
                    certifications=[]
                )
                self.save_profile(profile)
                return profile
            return None

    def save_profile(self, profile: StudentProfile) -> StudentProfile:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            profile_json = profile.model_dump_json()
            cursor.execute("""
                INSERT INTO profiles (id, data, updated_at) 
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(id) DO UPDATE SET 
                    data = excluded.data, 
                    updated_at = CURRENT_TIMESTAMP
            """, (profile.id, profile_json))
            conn.commit()
        return profile

    def get_state(self, state_key: str, profile_id: str = "default_student") -> Optional[Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT state_value FROM state_store WHERE profile_id = ? AND state_key = ?",
                (profile_id, state_key)
            )
            row = cursor.fetchone()
            if row:
                return json.loads(row["state_value"])
            return None

    def save_state(self, state_key: str, value: Any, profile_id: str = "default_student"):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            val_json = json.dumps(value)
            cursor.execute("""
                INSERT INTO state_store (profile_id, state_key, state_value, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(profile_id, state_key) DO UPDATE SET 
                    state_value = excluded.state_value,
                    updated_at = CURRENT_TIMESTAMP
            """, (profile_id, state_key, val_json))
            conn.commit()

storage_service = StorageService()
