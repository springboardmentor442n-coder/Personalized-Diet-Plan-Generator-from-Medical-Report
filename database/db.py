"""
Database Manager Module
Handles SQLite database operations for session management and caching
"""
import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class DatabaseManager:
    def __init__(self, db_path='ai_nutricare.db'):
        self.db_path = db_path
        self.max_sessions = 20  # Keep only 20 most recent sessions
        
    def init_db(self):
        """Initialize the database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    age INTEGER,
                    diet_preference TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    metrics TEXT,  -- JSON string
                    health_analysis TEXT,  -- JSON string
                    diet_plan TEXT,  -- JSON string
                    feedback TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_session_id 
                ON results (session_id)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_session_created 
                ON sessions (created_at)
            ''')
            
            conn.commit()
            conn.close()
            
            # Clean up old sessions on startup
            self._cleanup_old_sessions()
            
            print("✅ Database initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            return False
    
    def save_session(self, session_id: str, age: int, diet_preference: str):
        """Save or update a session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert or update session
            cursor.execute('''
                INSERT OR REPLACE INTO sessions 
                (session_id, age, diet_preference, created_at, last_accessed)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (session_id, age, diet_preference))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def save_result(self, session_id: str, result_data: Dict):
        """Save a diet plan result"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # First, ensure session exists
            self.save_session(
                session_id, 
                result_data.get('age'),
                result_data.get('diet_preference')
            )
            
            # Get the next version number for this session
            cursor.execute('''
                SELECT MAX(version) FROM results WHERE session_id = ?
            ''', (session_id,))
            
            max_version = cursor.fetchone()[0]
            next_version = (max_version or 0) + 1
            
            # Save the result
            cursor.execute('''
                INSERT INTO results 
                (session_id, version, metrics, health_analysis, diet_plan, feedback, created_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                session_id,
                next_version,
                json.dumps(result_data.get('metrics', {})),
                json.dumps(result_data.get('health_analysis', {})),
                json.dumps(result_data.get('diet_plan', {})),
                result_data.get('feedback', '')
            ))
            
            # Update session last_accessed
            cursor.execute('''
                UPDATE sessions SET last_accessed = CURRENT_TIMESTAMP 
                WHERE session_id = ?
            ''', (session_id,))
            
            conn.commit()
            conn.close()
            
            # Clean up old sessions periodically
            self._cleanup_old_sessions()
            
            return True
            
        except Exception as e:
            print(f"Error saving result: {e}")
            return False
    
    def get_session_result(self, session_id: str, version: Optional[int] = None) -> Optional[Dict]:
        """Get the latest result for a session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if version:
                # Get specific version
                cursor.execute('''
                    SELECT s.age, s.diet_preference, r.version, r.metrics, 
                           r.health_analysis, r.diet_plan, r.feedback, r.created_at
                    FROM sessions s
                    JOIN results r ON s.session_id = r.session_id
                    WHERE s.session_id = ? AND r.version = ?
                ''', (session_id, version))
            else:
                # Get latest version
                cursor.execute('''
                    SELECT s.age, s.diet_preference, r.version, r.metrics, 
                           r.health_analysis, r.diet_plan, r.feedback, r.created_at
                    FROM sessions s
                    JOIN results r ON s.session_id = r.session_id
                    WHERE s.session_id = ?
                    ORDER BY r.version DESC
                    LIMIT 1
                ''', (session_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                age, diet_preference, version, metrics_json, health_analysis_json, diet_plan_json, feedback, created_at = row
                
                # Parse JSON fields
                try:
                    metrics = json.loads(metrics_json) if metrics_json else {}
                    health_analysis = json.loads(health_analysis_json) if health_analysis_json else {}
                    diet_plan = json.loads(diet_plan_json) if diet_plan_json else {}
                except json.JSONDecodeError:
                    metrics = health_analysis = diet_plan = {}
                
                return {
                    'session_id': session_id,
                    'age': age,
                    'diet_preference': diet_preference,
                    'version': version,
                    'metrics': metrics,
                    'health_analysis': health_analysis,
                    'diet_plan': diet_plan,
                    'feedback': feedback,
                    'timestamp': created_at
                }
            
            return None
            
        except Exception as e:
            print(f"Error getting session result: {e}")
            return None
    
    def check_cached_result(self, session_id: str, age: int, diet_preference: str) -> Optional[Dict]:
        """Check if there's a cached result for the same inputs"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Look for exact match of session parameters
            cursor.execute('''
                SELECT s.session_id, s.age, s.diet_preference, r.version, r.metrics, 
                       r.health_analysis, r.diet_plan, r.feedback, r.created_at
                FROM sessions s
                JOIN results r ON s.session_id = r.session_id
                WHERE (s.session_id = ? OR (s.age = ? AND s.diet_preference = ?))
                ORDER BY r.created_at DESC
                LIMIT 1
            ''', (session_id, age, diet_preference))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                found_session_id, found_age, found_diet_pref, version, metrics_json, health_analysis_json, diet_plan_json, feedback, created_at = row
                
                # Parse JSON fields
                try:
                    metrics = json.loads(metrics_json) if metrics_json else {}
                    health_analysis = json.loads(health_analysis_json) if health_analysis_json else {}
                    diet_plan = json.loads(diet_plan_json) if diet_plan_json else {}
                except json.JSONDecodeError:
                    return None
                
                return {
                    'session_id': found_session_id,
                    'age': found_age,
                    'diet_preference': found_diet_pref,
                    'version': version,
                    'metrics': metrics,
                    'health_analysis': health_analysis,
                    'diet_plan': diet_plan,
                    'feedback': feedback,
                    'timestamp': created_at
                }
            
            return None
            
        except Exception as e:
            print(f"Error checking cached result: {e}")
            return None
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all sessions with their latest results"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.session_id, s.age, s.diet_preference, s.created_at, s.last_accessed,
                       MAX(r.version) as latest_version
                FROM sessions s
                LEFT JOIN results r ON s.session_id = r.session_id
                GROUP BY s.session_id
                ORDER BY s.last_accessed DESC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            sessions = []
            for row in rows:
                session_id, age, diet_preference, created_at, last_accessed, latest_version = row
                sessions.append({
                    'session_id': session_id,
                    'age': age,
                    'diet_preference': diet_preference,
                    'created_at': created_at,
                    'last_accessed': last_accessed,
                    'latest_version': latest_version or 0
                })
            
            return sessions
            
        except Exception as e:
            print(f"Error getting all sessions: {e}")
            return []
    
    def _cleanup_old_sessions(self):
        """Remove old sessions to keep only the most recent ones"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get count of sessions
            cursor.execute('SELECT COUNT(*) FROM sessions')
            session_count = cursor.fetchone()[0]
            
            if session_count > self.max_sessions:
                # Get sessions to delete (oldest ones)
                sessions_to_delete = session_count - self.max_sessions
                
                cursor.execute('''
                    SELECT session_id FROM sessions 
                    ORDER BY last_accessed ASC 
                    LIMIT ?
                ''', (sessions_to_delete,))
                
                old_sessions = cursor.fetchall()
                
                # Delete old sessions and their results
                for (old_session_id,) in old_sessions:
                    cursor.execute('DELETE FROM results WHERE session_id = ?', (old_session_id,))
                    cursor.execute('DELETE FROM sessions WHERE session_id = ?', (old_session_id,))
                
                conn.commit()
                print(f"Cleaned up {len(old_sessions)} old sessions")
            
            conn.close()
            
        except Exception as e:
            print(f"Error cleaning up old sessions: {e}")
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a specific session and all its results"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete results first (foreign key dependency)
            cursor.execute('DELETE FROM results WHERE session_id = ?', (session_id,))
            results_deleted = cursor.rowcount
            
            # Delete session
            cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
            sessions_deleted = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            if sessions_deleted > 0:
                print(f"Deleted session {session_id} and {results_deleted} results")
                return True
            else:
                print(f"Session {session_id} not found")
                return False
                
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get session count
            cursor.execute('SELECT COUNT(*) FROM sessions')
            session_count = cursor.fetchone()[0]
            
            # Get result count
            cursor.execute('SELECT COUNT(*) FROM results')
            result_count = cursor.fetchone()[0]
            
            # Get database file size
            db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
            
            # Get oldest and newest sessions
            cursor.execute('SELECT MIN(created_at), MAX(created_at) FROM sessions')
            date_range = cursor.fetchone()
            
            conn.close()
            
            return {
                'session_count': session_count,
                'result_count': result_count,
                'db_size_bytes': db_size,
                'db_size_mb': round(db_size / (1024 * 1024), 2),
                'oldest_session': date_range[0],
                'newest_session': date_range[1],
                'max_sessions': self.max_sessions
            }
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {}