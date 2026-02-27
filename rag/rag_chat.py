"""
RAG ChatBot Module
Combines retrieval and generation for nutrition Q&A
"""
import json
import re
from rag.retriever import RAGRetriever
from llm.prompts import get_chatbot_prompt, get_meal_alternative_prompt

class RAGChatbot:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.retriever = RAGRetriever()
        self.initialized = False
        
    def initialize(self):
        """Initialize the chatbot with RAG components"""
        try:
            print("Initializing RAG chatbot...")
            self.retriever.initialize()
            self.initialized = True
            print("✅ RAG chatbot initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing RAG chatbot: {e}")
            self.initialized = False
    
    def get_response(self, message, user_context=None):
        """
        Generate a response to user message using RAG
        """
        if not self.initialized:
            return "Sorry, the chatbot is not properly initialized. Please try again later."
        
        try:
            # Check if this is a request for meal alternatives
            if self._is_meal_alternative_request(message):
                return self._handle_meal_alternative_request(message, user_context)
            
            # Retrieve relevant documents
            retrieved_docs = self.retriever.retrieve(message, top_k=3)
            
            # Format context for LLM
            rag_context = self._format_retrieved_context(retrieved_docs)
            
            # Combine user context with RAG context
            full_context = self._combine_contexts(user_context, rag_context)
            
            # Generate response using LLM
            prompt = get_chatbot_prompt(message, full_context)
            
            # Get completion with chat-specific settings
            response = self.llm_client.get_completion(
                prompt,
                temperature=0.1,
                max_tokens=400
            )
            
            # Handle different response formats
            if isinstance(response, dict):
                if 'error' in response:
                    return "I apologize, but I'm having trouble processing your question right now. Please try rephrasing or asking again."
                elif 'response' in response:
                    return response['response']
                else:
                    # If response is a dict but not in expected format, try to extract text
                    return str(response)
            elif isinstance(response, str):
                return response
            else:
                return "I apologize, but I couldn't generate a proper response. Please try again."
                
        except Exception as e:
            print(f"Error in get_response: {e}")
            return "I'm sorry, I encountered an error while processing your question. Please try again."
    
    def _is_meal_alternative_request(self, message):
        """Check if the message is asking for meal alternatives"""
        alternative_keywords = [
            'alternative', 'alternatives', 'substitute', 'substitutes', 
            'replace', 'replacement', 'instead of', 'other options',
            'different meal', 'swap', 'change'
        ]
        
        meal_keywords = [
            'breakfast', 'lunch', 'dinner', 'snack', 'meal'
        ]
        
        message_lower = message.lower()
        
        has_alternative_keyword = any(keyword in message_lower for keyword in alternative_keywords)
        has_meal_keyword = any(keyword in message_lower for keyword in meal_keywords)
        
        return has_alternative_keyword and has_meal_keyword
    
    def _handle_meal_alternative_request(self, message, user_context):
        """Handle requests for meal alternatives"""
        if not user_context or 'diet_plan' not in user_context:
            return "I don't have your current diet plan information. Please generate a diet plan first to get meal alternatives."
        
        # Extract meal information from message
        meal_info = self._extract_meal_info_from_message(message, user_context)
        
        if not meal_info:
            return "Could you be more specific about which meal you'd like alternatives for? For example: 'alternatives for Day 1 breakfast' or 'substitute for lunch'."
        
        # Generate alternatives using specific prompt
        alternatives_prompt = get_meal_alternative_prompt(
            meal_info['meal_name'],
            meal_info['day'],
            meal_info['meal_type'],
            user_context.get('diet_preference', 'vegetarian'),
            user_context.get('health_analysis', {}).get('conditions', [])
        )
        
        response = self.llm_client.get_completion(
            alternatives_prompt,
            temperature=0.2,
            max_tokens=400
        )
        
        if isinstance(response, dict):
            return str(response)
        return response
    
    def _extract_meal_info_from_message(self, message, user_context):
        """Extract meal information from user message"""
        message_lower = message.lower()
        
        # Look for day references
        day_pattern = r'day\s*(\d+)'
        day_match = re.search(day_pattern, message_lower)
        day = day_match.group(1) if day_match else '1'
        
        # Look for meal type
        meal_type = None
        if 'breakfast' in message_lower:
            meal_type = 'breakfast'
        elif 'lunch' in message_lower:
            meal_type = 'lunch'
        elif 'dinner' in message_lower:
            meal_type = 'dinner'
        elif 'snack' in message_lower:
            meal_type = 'snack'
        
        # If no specific meal type mentioned, default to breakfast
        if not meal_type:
            meal_type = 'breakfast'
        
        # Get the meal name from user's diet plan
        diet_plan = user_context.get('diet_plan', {})
        day_key = f'day{day}'
        
        if day_key in diet_plan and meal_type in diet_plan[day_key]:
            meal_name = diet_plan[day_key][meal_type].get('name', 'Unknown meal')
            return {
                'day': day,
                'meal_type': meal_type,
                'meal_name': meal_name
            }
        
        return None
    
    def _format_retrieved_context(self, retrieved_docs):
        """Format retrieved documents into context string"""
        if not retrieved_docs:
            return "No specific nutrition information retrieved."
        
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(f"{i}. {doc['topic']}: {doc['content']}")
        
        return "Relevant nutrition information:\n" + "\n".join(context_parts)
    
    def _combine_contexts(self, user_context, rag_context):
        """Combine user's personal context with retrieved RAG context"""
        combined_context = {}
        
        # Add user's personal information
        if user_context:
            combined_context['personal_info'] = {
                'age': user_context.get('age'),
                'diet_preference': user_context.get('diet_preference'),
                'health_metrics': user_context.get('metrics', {}),
                'health_analysis': user_context.get('health_analysis', {}),
                'has_diet_plan': 'diet_plan' in user_context
            }
            
            # Add diet plan summary if available
            if 'diet_plan' in user_context:
                combined_context['diet_plan_summary'] = self._create_diet_plan_summary(user_context['diet_plan'])
        
        # Add RAG context
        combined_context['nutrition_knowledge'] = rag_context
        
        return combined_context
    
    def _create_diet_plan_summary(self, diet_plan):
        """Create a summary of the user's diet plan"""
        summary = {}
        
        for day_key, day_meals in diet_plan.items():
            if day_key.startswith('day') and isinstance(day_meals, dict):
                daily_summary = {}
                total_calories = 0
                
                for meal_type, meal_data in day_meals.items():
                    if isinstance(meal_data, dict) and 'name' in meal_data:
                        daily_summary[meal_type] = {
                            'name': meal_data.get('name'),
                            'calories': meal_data.get('calories', 0)
                        }
                        total_calories += meal_data.get('calories', 0)
                
                daily_summary['total_calories'] = total_calories
                summary[day_key] = daily_summary
        
        return summary
    
    def get_health_metric_explanation(self, metric_type, value, user_context=None):
        """Get specific explanation for a health metric"""
        explanations = {
            'bmi': self._explain_bmi,
            'blood_sugar': self._explain_blood_sugar,
            'cholesterol': self._explain_cholesterol,
            'blood_pressure': self._explain_blood_pressure
        }
        
        if metric_type in explanations:
            return explanations[metric_type](value, user_context)
        else:
            return f"I don't have specific information about {metric_type}. Please consult with a healthcare professional."
    
    def _explain_bmi(self, value, user_context):
        """Explain BMI value"""
        try:
            bmi = float(value)
            if bmi < 18.5:
                category = "underweight"
                advice = "Consider consulting a nutritionist to develop a healthy weight gain plan."
            elif 18.5 <= bmi < 25:
                category = "normal weight"
                advice = "Great! Maintain your current healthy lifestyle and balanced diet."
            elif 25 <= bmi < 30:
                category = "overweight"
                advice = "Focus on portion control, increase physical activity, and choose nutrient-dense foods."
            else:
                category = "obese"
                advice = "Consider consulting healthcare professionals for a comprehensive weight management plan."
            
            return f"Your BMI of {bmi} falls in the {category} category. {advice}"
        except:
            return "I couldn't interpret your BMI value. Please ensure it's a valid number."
    
    def _explain_blood_sugar(self, value, user_context):
        """Explain blood sugar value"""
        try:
            blood_sugar = float(value)
            if blood_sugar < 70:
                return f"Blood sugar of {blood_sugar} mg/dL is low (hypoglycemia). Consider eating a quick-acting carbohydrate and consult your doctor."
            elif 70 <= blood_sugar <= 100:
                return f"Blood sugar of {blood_sugar} mg/dL is in the normal range. Maintain your current diet and lifestyle."
            elif 100 < blood_sugar <= 125:
                return f"Blood sugar of {blood_sugar} mg/dL indicates prediabetes. Focus on low glycemic foods, reduce refined sugars, and increase fiber intake."
            else:
                return f"Blood sugar of {blood_sugar} mg/dL is high and may indicate diabetes. Please consult a healthcare provider immediately."
        except:
            return "I couldn't interpret your blood sugar value. Please ensure it's a valid number in mg/dL."
    
    def _explain_cholesterol(self, value, user_context):
        """Explain cholesterol value"""
        try:
            cholesterol = float(value)
            if cholesterol < 200:
                return f"Total cholesterol of {cholesterol} mg/dL is desirable. Continue eating heart-healthy foods like fish, nuts, and vegetables."
            elif 200 <= cholesterol <= 239:
                return f"Total cholesterol of {cholesterol} mg/dL is borderline high. Reduce saturated fats, increase fiber, and consider omega-3 rich foods."
            else:
                return f"Total cholesterol of {cholesterol} mg/dL is high. Focus on a low-saturated fat diet, increase soluble fiber, and consult your doctor."
        except:
            return "I couldn't interpret your cholesterol value. Please ensure it's a valid number in mg/dL."
    
    def _explain_blood_pressure(self, value, user_context):
        """Explain blood pressure value"""
        try:
            systolic, diastolic = map(int, value.split('/'))
            if systolic < 120 and diastolic < 80:
                return f"Blood pressure {value} mmHg is normal. Continue your healthy lifestyle."
            elif systolic < 130 and diastolic < 80:
                return f"Blood pressure {value} mmHg is elevated. Reduce sodium, increase potassium-rich foods."
            elif systolic < 140 or diastolic < 90:
                return f"Blood pressure {value} mmHg indicates Stage 1 hypertension. Follow DASH diet principles and limit sodium."
            else:
                return f"Blood pressure {value} mmHg indicates Stage 2 hypertension. Please consult a healthcare provider."
        except:
            return "I couldn't interpret your blood pressure value. Please ensure it's in the format 'systolic/diastolic'."
    
    def get_retriever_stats(self):
        """Get statistics about the RAG retriever"""
        if self.initialized:
            return self.retriever.get_statistics()
        return {"error": "Retriever not initialized"}