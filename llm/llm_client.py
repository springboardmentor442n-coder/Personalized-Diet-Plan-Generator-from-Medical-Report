"""
LLM Client Module
Groq API client for health analysis and diet plan generation
"""
import json
import os
from groq import Groq
import time

class LLMClient:
    def __init__(self, api_key=None, model=None):
        """
        Initialize LLM client with Groq API
        """
        # Get configuration from environment variables with defaults
        self.api_key = api_key or os.getenv('GROQ_API_KEY', 'your-groq-api-key-here')
        self.model = model or os.getenv('GROQ_MODEL', 'llama3-8b-8192')
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
        
        # Performance settings
        self.temperature = 0  # For consistent, deterministic results
        self.max_tokens = 2000
        self.timeout = 30
        
    def get_completion(self, prompt, temperature=None, max_tokens=None, retry_count=3):
        """
        Get completion from LLM with retry logic for JSON parsing
        """
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        for attempt in range(retry_count):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a medical AI assistant. Always respond with valid JSON only. No additional text or explanations outside the JSON structure."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=self.timeout
                )
                
                content = response.choices[0].message.content.strip()
                
                # Try to parse as JSON to validate
                try:
                    json_result = json.loads(content)
                    return json_result
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract JSON from the response
                    json_content = self._extract_json_from_response(content)
                    if json_content:
                        return json.loads(json_content)
                    else:
                        if attempt < retry_count - 1:
                            print(f"JSON parsing failed on attempt {attempt + 1}, retrying...")
                            time.sleep(1)
                            continue
                        else:
                            print(f"Failed to parse JSON after {retry_count} attempts")
                            return {"error": "Failed to parse LLM response as JSON", "raw_response": content}
                            
            except Exception as e:
                print(f"LLM API error on attempt {attempt + 1}: {e}")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    return {"error": f"LLM API error: {str(e)}"}
        
        return {"error": "Max retry attempts reached"}
    
    def _extract_json_from_response(self, content):
        """
        Extract JSON from response that might have additional text
        """
        import re
        
        # Look for JSON patterns in the response
        json_patterns = [
            r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Simple nested JSON
            r'\{.*\}',  # Any content between braces
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                try:
                    json.loads(match)
                    return match
                except:
                    continue
        
        return None
    
    def test_connection(self):
        """
        Test the Groq API connection with a simple request
        """
        try:
            test_prompt = "Return a JSON object with a single key 'status' and value 'connected'."
            result = self.get_completion(test_prompt)
            
            if isinstance(result, dict) and result.get('status') == 'connected':
                return True, "Connection successful"
            else:
                return False, f"Unexpected response: {result}"
                
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def set_model(self, model_name):
        """
        Set the Groq model to use
        Available models: llama3-8b-8192, llama3-70b-8192, mixtral-8x7b-32768, gemma-7b-it
        """
        available_models = [
            'llama3-8b-8192',
            'llama3-70b-8192', 
            'mixtral-8x7b-32768',
            'gemma-7b-it'
        ]
        
        if model_name in available_models:
            self.model = model_name
            return True
        else:
            print(f"Model {model_name} not available. Available models: {available_models}")
            return False
    
    def get_health_analysis(self, text, age, prompt_template):
        """
        Specific method for health analysis
        """
        prompt = prompt_template.format(text=text, age=age)
        return self.get_completion(prompt, max_tokens=800)
    
    def get_diet_plan(self, age, diet_preference, metrics, health_analysis, prompt_template, feedback=None):
        """
        Specific method for diet plan generation
        """
        prompt = prompt_template.format(
            age=age,
            diet_preference=diet_preference,
            metrics=json.dumps(metrics) if metrics else "No metrics available",
            health_analysis=json.dumps(health_analysis) if health_analysis else "No analysis available",
            feedback=feedback if feedback else ""
        )
        return self.get_completion(prompt, max_tokens=1500)
    
    def get_chat_response(self, message, context, prompt_template):
        """
        Specific method for chatbot responses
        """
        prompt = prompt_template.format(
            message=message,
            context=json.dumps(context) if context else "No context available"
        )
        return self.get_completion(prompt, temperature=0.1, max_tokens=800)