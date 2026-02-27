"""
Session Manager Utility
Handles session management and caching logic
"""
from typing import Dict, Optional, Any
from database.db import DatabaseManager

class SessionManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        
    def save_result(self, session_id: str, result_data: Dict[str, Any]) -> bool:
        """
        Save a result to the database
        """
        return self.db_manager.save_result(session_id, result_data)
    
    def get_cached_result(self, session_id: str, age: Optional[int] = None, diet_preference: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get cached result for a session, with optional parameter matching
        """
        # First, try to get the exact session
        result = self.db_manager.get_session_result(session_id)
        
        if result:
            # If we have specific parameters, check if they match
            if age is not None and diet_preference is not None:
                if result.get('age') == age and result.get('diet_preference') == diet_preference:
                    return result
                else:
                    # Parameters don't match, look for a matching session
                    cached_result = self.db_manager.check_cached_result(session_id, age, diet_preference)
                    return cached_result
            else:
                # No parameters specified, return the session result
                return result
        
        # If no exact session found and we have parameters, search for matching parameters
        if age is not None and diet_preference is not None:
            return self.db_manager.check_cached_result(session_id, age, diet_preference)
        
        return None
    
    def create_session_cache_key(self, age: int, diet_preference: str, metrics: Dict[str, Any] = None) -> str:
        """
        Create a cache key based on session parameters
        This helps identify similar sessions for caching
        """
        # Create a simple hash-like key based on parameters
        key_parts = [
            f"age:{age}",
            f"diet:{diet_preference}"
        ]
        
        # Add significant metrics if available
        if metrics:
            if 'bmi' in metrics:
                # Round BMI to nearest integer for caching
                bmi_rounded = round(float(metrics['bmi']))
                key_parts.append(f"bmi:{bmi_rounded}")
            
            if 'blood_sugar' in metrics:
                # Categorize blood sugar for caching
                blood_sugar = float(metrics['blood_sugar'])
                if blood_sugar < 100:
                    bs_category = 'normal'
                elif blood_sugar < 126:
                    bs_category = 'prediabetic'
                else:
                    bs_category = 'diabetic'
                key_parts.append(f"bs:{bs_category}")
        
        return "_".join(key_parts)
    
    def should_use_cache(self, session_id: str, age: int, diet_preference: str, metrics: Dict[str, Any] = None) -> bool:
        """
        Determine if we should use cached results for the given parameters
        """
        cached_result = self.get_cached_result(session_id, age, diet_preference)
        
        if not cached_result:
            return False
        
        # Check if the cached result is recent enough (within 24 hours for same session)
        # or if parameters match exactly
        cached_age = cached_result.get('age')
        cached_diet = cached_result.get('diet_preference')
        
        # Exact parameter match
        if cached_age == age and cached_diet == diet_preference:
            return True
        
        # Similar parameters (age within 5 years, same diet preference)
        if cached_diet == diet_preference and abs(cached_age - age) <= 5:
            return True
        
        return False
    
    def invalidate_session_cache(self, session_id: str) -> bool:
        """
        Invalidate (delete) cached results for a session
        """
        return self.db_manager.delete_session(session_id)
    
    def get_session_history(self, session_id: str) -> list:
        """
        Get all versions of results for a session
        """
        try:
            # Get all results for the session
            import sqlite3
            conn = sqlite3.connect(self.db_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT version, metrics, health_analysis, diet_plan, feedback, created_at
                FROM results 
                WHERE session_id = ? 
                ORDER BY version ASC
            ''', (session_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            history = []
            for row in rows:
                version, metrics_json, health_analysis_json, diet_plan_json, feedback, created_at = row
                
                # Parse JSON fields
                import json
                try:
                    metrics = json.loads(metrics_json) if metrics_json else {}
                    health_analysis = json.loads(health_analysis_json) if health_analysis_json else {}
                    diet_plan = json.loads(diet_plan_json) if diet_plan_json else {}
                except json.JSONDecodeError:
                    metrics = health_analysis = diet_plan = {}
                
                history.append({
                    'version': version,
                    'metrics': metrics,
                    'health_analysis': health_analysis,
                    'diet_plan': diet_plan,
                    'feedback': feedback,
                    'created_at': created_at
                })
            
            return history
            
        except Exception as e:
            print(f"Error getting session history: {e}")
            return []
    
    def get_similar_sessions(self, age: int, diet_preference: str, limit: int = 5) -> list:
        """
        Find sessions with similar parameters for potential reuse
        """
        try:
            sessions = self.db_manager.get_all_sessions()
            similar_sessions = []
            
            for session in sessions:
                session_age = session.get('age')
                session_diet = session.get('diet_preference')
                
                if session_diet == diet_preference:
                    age_diff = abs(session_age - age) if session_age else float('inf')
                    
                    # Consider sessions with age within 10 years as similar
                    if age_diff <= 10:
                        similarity_score = 10 - age_diff  # Higher score for closer age
                        session['similarity_score'] = similarity_score
                        similar_sessions.append(session)
            
            # Sort by similarity score (descending) and limit results
            similar_sessions.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
            return similar_sessions[:limit]
            
        except Exception as e:
            print(f"Error finding similar sessions: {e}")
            return []
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about session usage and caching
        """
        try:
            db_stats = self.db_manager.get_database_stats()
            sessions = self.db_manager.get_all_sessions()
            
            # Analyze session patterns
            age_groups = {'<30': 0, '30-50': 0, '>50': 0}
            diet_preferences = {'vegetarian': 0, 'non-vegetarian': 0}
            
            for session in sessions:
                age = session.get('age', 0)
                if age < 30:
                    age_groups['<30'] += 1
                elif age <= 50:
                    age_groups['30-50'] += 1
                else:
                    age_groups['>50'] += 1
                
                diet_pref = session.get('diet_preference', 'unknown')
                if diet_pref in diet_preferences:
                    diet_preferences[diet_pref] += 1
            
            return {
                'database_stats': db_stats,
                'session_count': len(sessions),
                'age_distribution': age_groups,
                'diet_preference_distribution': diet_preferences,
                'cache_efficiency': self._calculate_cache_efficiency(sessions)
            }
            
        except Exception as e:
            print(f"Error getting session statistics: {e}")
            return {}
    
    def _calculate_cache_efficiency(self, sessions: list) -> Dict[str, Any]:
        """
        Calculate cache hit/miss efficiency
        This is a simplified calculation based on session patterns
        """
        try:
            if not sessions:
                return {'efficiency': 0, 'potential_cache_hits': 0}
            
            # Group sessions by parameters to identify potential cache hits
            parameter_groups = {}
            
            for session in sessions:
                age = session.get('age')
                diet_pref = session.get('diet_preference')
                
                # Create a key for similar parameters (age groups of 5 years)
                age_group = (age // 5) * 5 if age else 0
                key = f"{age_group}_{diet_pref}"
                
                if key not in parameter_groups:
                    parameter_groups[key] = []
                parameter_groups[key].append(session)
            
            # Calculate potential cache hits
            potential_hits = 0
            total_sessions = len(sessions)
            
            for group_sessions in parameter_groups.values():
                if len(group_sessions) > 1:
                    # If multiple sessions with similar parameters, count as potential cache hits
                    potential_hits += len(group_sessions) - 1
            
            efficiency = (potential_hits / total_sessions * 100) if total_sessions > 0 else 0
            
            return {
                'efficiency_percentage': round(efficiency, 1),
                'potential_cache_hits': potential_hits,
                'total_sessions': total_sessions,
                'unique_parameter_groups': len(parameter_groups)
            }
            
        except Exception as e:
            print(f"Error calculating cache efficiency: {e}")
            return {'error': str(e)}
    
    def optimize_cache(self) -> Dict[str, Any]:
        """
        Perform cache optimization by cleaning up old or redundant sessions
        """
        try:
            initial_stats = self.db_manager.get_database_stats()
            
            # Clean up old sessions (handled by DatabaseManager)
            self.db_manager._cleanup_old_sessions()
            
            final_stats = self.db_manager.get_database_stats()
            
            return {
                'optimization_completed': True,
                'sessions_before': initial_stats.get('session_count', 0),
                'sessions_after': final_stats.get('session_count', 0),
                'sessions_removed': initial_stats.get('session_count', 0) - final_stats.get('session_count', 0),
                'space_saved_mb': round(initial_stats.get('db_size_mb', 0) - final_stats.get('db_size_mb', 0), 2)
            }
            
        except Exception as e:
            print(f"Error optimizing cache: {e}")
            return {'error': str(e)}
    
    def export_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Export all data for a specific session
        """
        try:
            # Get session result
            session_result = self.get_cached_result(session_id)
            if not session_result:
                return None
            
            # Get session history
            session_history = self.get_session_history(session_id)
            
            from datetime import datetime
            return {
                'session_id': session_id,
                'current_result': session_result,
                'version_history': session_history,
                'export_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error exporting session data: {e}")
            return None