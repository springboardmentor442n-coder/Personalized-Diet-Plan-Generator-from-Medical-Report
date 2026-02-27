"""
JSON Export Utility
Handles exporting results to JSON files
"""
import json
import os
from datetime import datetime
from typing import Dict, Any

def export_to_json(result_data: Dict[Any, Any], session_id: str, output_dir: str = 'outputs'):
    """
    Export result data to a JSON file
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        timestamp = result_data.get('timestamp', datetime.now().isoformat())
        version = result_data.get('version', 1)
        
        # Clean timestamp for filename (remove invalid characters)
        clean_timestamp = timestamp.replace(':', '-').split('.')[0]
        filename = f"{session_id}_{clean_timestamp}_v{version}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Prepare export data with metadata
        export_data = {
            'export_info': {
                'exported_at': datetime.now().isoformat(),
                'application': 'AI-NutriCare',
                'version': '1.0.0',
                'session_id': session_id
            },
            'patient_info': {
                'age': result_data.get('age'),
                'diet_preference': result_data.get('diet_preference'),
                'session_version': result_data.get('version', 1)
            },
            'health_data': {
                'extracted_metrics': result_data.get('metrics', {}),
                'ai_health_analysis': result_data.get('health_analysis', {})
            },
            'diet_plan': result_data.get('diet_plan', {}),
            'generation_info': {
                'timestamp': result_data.get('timestamp'),
                'feedback_applied': result_data.get('feedback', ''),
                'plan_version': result_data.get('version', 1)
            }
        }
        
        # Add nutrition summary if available
        if 'diet_plan' in result_data and result_data['diet_plan']:
            nutrition_summary = calculate_nutrition_summary(result_data['diet_plan'])
            export_data['nutrition_summary'] = nutrition_summary
        
        # Write to file with proper formatting
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Result exported to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Error exporting to JSON: {e}")
        return None

def calculate_nutrition_summary(diet_plan: Dict[Any, Any]) -> Dict[str, Any]:
    """
    Calculate nutrition summary for the entire diet plan
    """
    try:
        total_calories = 0
        total_meals = 0
        daily_totals = []
        
        # Process each day
        for day_key, day_meals in diet_plan.items():
            if not day_key.startswith('day') or not isinstance(day_meals, dict):
                continue
                
            day_calories = 0
            day_carb_calories = 0
            day_protein_calories = 0
            day_fat_calories = 0
            
            # Process each meal
            for meal_type, meal_data in day_meals.items():
                if not isinstance(meal_data, dict):
                    continue
                    
                calories = meal_data.get('calories', 0)
                carbs_pct = meal_data.get('carbs', 0)
                protein_pct = meal_data.get('protein', 0)
                fat_pct = meal_data.get('fat', 0)
                
                if calories > 0:
                    day_calories += calories
                    day_carb_calories += (carbs_pct * calories / 100)
                    day_protein_calories += (protein_pct * calories / 100)
                    day_fat_calories += (fat_pct * calories / 100)
                    total_meals += 1
            
            if day_calories > 0:
                daily_totals.append({
                    'day': day_key,
                    'total_calories': day_calories,
                    'carbs_calories': round(day_carb_calories, 1),
                    'protein_calories': round(day_protein_calories, 1),
                    'fat_calories': round(day_fat_calories, 1),
                    'carbs_percentage': round((day_carb_calories / day_calories) * 100, 1) if day_calories > 0 else 0,
                    'protein_percentage': round((day_protein_calories / day_calories) * 100, 1) if day_calories > 0 else 0,
                    'fat_percentage': round((day_fat_calories / day_calories) * 100, 1) if day_calories > 0 else 0
                })
                
                total_calories += day_calories
        
        # Calculate weekly averages
        num_days = len(daily_totals)
        avg_daily_calories = round(total_calories / num_days, 1) if num_days > 0 else 0
        
        # Calculate average macro distribution
        total_carb_calories = sum(day['carbs_calories'] for day in daily_totals)
        total_protein_calories = sum(day['protein_calories'] for day in daily_totals)
        total_fat_calories = sum(day['fat_calories'] for day in daily_totals)
        
        avg_carbs_pct = round((total_carb_calories / total_calories) * 100, 1) if total_calories > 0 else 0
        avg_protein_pct = round((total_protein_calories / total_calories) * 100, 1) if total_calories > 0 else 0
        avg_fat_pct = round((total_fat_calories / total_calories) * 100, 1) if total_calories > 0 else 0
        
        return {
            'weekly_summary': {
                'total_calories': total_calories,
                'average_daily_calories': avg_daily_calories,
                'total_meals_planned': total_meals,
                'days_covered': num_days
            },
            'macro_distribution': {
                'carbohydrates': f"{avg_carbs_pct}%",
                'protein': f"{avg_protein_pct}%",
                'fat': f"{avg_fat_pct}%"
            },
            'daily_breakdown': daily_totals,
            'meal_categories': {
                'breakfast_meals': total_meals // 4 if total_meals >= 4 else 0,
                'lunch_meals': total_meals // 4 if total_meals >= 4 else 0,
                'snack_meals': total_meals // 4 if total_meals >= 4 else 0,
                'dinner_meals': total_meals // 4 if total_meals >= 4 else 0
            }
        }
        
    except Exception as e:
        print(f"Error calculating nutrition summary: {e}")
        return {
            'error': 'Could not calculate nutrition summary',
            'message': str(e)
        }

def export_session_history(session_data: Dict[Any, Any], output_dir: str = 'outputs'):
    """
    Export complete session history including all versions
    """
    try:
        session_id = session_data.get('session_id', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"session_history_{session_id}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        os.makedirs(output_dir, exist_ok=True)
        
        export_data = {
            'export_info': {
                'exported_at': datetime.now().isoformat(),
                'export_type': 'session_history',
                'application': 'AI-NutriCare'
            },
            'session_data': session_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filepath
        
    except Exception as e:
        print(f"Error exporting session history: {e}")
        return None

def validate_json_export(filepath: str) -> bool:
    """
    Validate that the exported JSON file is valid
    """
    try:
        if not os.path.exists(filepath):
            return False
            
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        
        return True
        
    except (json.JSONDecodeError, IOError):
        return False

def get_export_statistics(output_dir: str = 'outputs') -> Dict[str, Any]:
    """
    Get statistics about exported files
    """
    try:
        if not os.path.exists(output_dir):
            return {
                'total_files': 0,
                'total_size_mb': 0,
                'files': []
            }
        
        files = []
        total_size = 0
        
        for filename in os.listdir(output_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(output_dir, filename)
                file_size = os.path.getsize(filepath)
                file_mtime = os.path.getmtime(filepath)
                
                files.append({
                    'filename': filename,
                    'size_bytes': file_size,
                    'size_kb': round(file_size / 1024, 1),
                    'modified': datetime.fromtimestamp(file_mtime).isoformat(),
                    'is_valid': validate_json_export(filepath)
                })
                
                total_size += file_size
        
        return {
            'total_files': len(files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'files': sorted(files, key=lambda x: x['modified'], reverse=True)
        }
        
    except Exception as e:
        print(f"Error getting export statistics: {e}")
        return {
            'error': str(e)
        }

def cleanup_old_exports(output_dir: str = 'outputs', max_files: int = 50):
    """
    Clean up old export files to keep only the most recent ones
    """
    try:
        if not os.path.exists(output_dir):
            return 0
        
        # Get all JSON files with their modification times
        files_with_times = []
        for filename in os.listdir(output_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(output_dir, filename)
                mtime = os.path.getmtime(filepath)
                files_with_times.append((filepath, mtime))
        
        # Sort by modification time (newest first)
        files_with_times.sort(key=lambda x: x[1], reverse=True)
        
        # Delete excess files
        deleted_count = 0
        if len(files_with_times) > max_files:
            files_to_delete = files_with_times[max_files:]
            for filepath, _ in files_to_delete:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except OSError as e:
                    print(f"Error deleting {filepath}: {e}")
        
        return deleted_count
        
    except Exception as e:
        print(f"Error cleaning up exports: {e}")
        return 0