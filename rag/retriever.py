"""
RAG Retriever Module
Handles document retrieval for the nutrition chatbot
"""
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class RAGRetriever:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None
        self.knowledge_base = []
        self.embeddings = None
        self.embeddings_file = 'rag/embeddings.pkl'
        self.knowledge_file = 'rag/knowledge_base.json'
        
    def initialize(self):
        """Initialize the retriever with model and knowledge base"""
        # Load the sentence transformer model
        print("Loading sentence transformer model...")
        self.model = SentenceTransformer(self.model_name)
        
        # Load or create knowledge base
        self._load_or_create_knowledge_base()
        
        # Load or create embeddings
        self._load_or_create_embeddings()
        
        print(f"RAG Retriever initialized with {len(self.knowledge_base)} documents")
    
    def _load_or_create_knowledge_base(self):
        """Load existing knowledge base or create a new one"""
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
        else:
            self.knowledge_base = self._create_nutrition_knowledge_base()
            self._save_knowledge_base()
    
    def _create_nutrition_knowledge_base(self):
        """Create a comprehensive nutrition knowledge base"""
        knowledge_docs = [
            # BMI and Weight Management
            {
                "topic": "BMI Normal Range",
                "content": "A normal BMI range is 18.5-24.9. BMI below 18.5 is underweight, 25-29.9 is overweight, and 30+ is obese. BMI is calculated as weight (kg) divided by height (m) squared.",
                "category": "health_metrics"
            },
            {
                "topic": "BMI Interpretation",
                "content": "BMI limitations: doesn't distinguish muscle from fat, may not apply to athletes or elderly. Consider waist circumference and body composition for complete assessment.",
                "category": "health_metrics"
            },
            
            # Blood Sugar
            {
                "topic": "Blood Sugar Normal Range",
                "content": "Normal fasting blood sugar: 70-100 mg/dL. Prediabetes: 100-125 mg/dL. Diabetes: 126+ mg/dL. Random blood sugar over 200 mg/dL with symptoms indicates diabetes.",
                "category": "health_metrics"
            },
            {
                "topic": "Blood Sugar Management",
                "content": "Control blood sugar with: complex carbohydrates, fiber-rich foods, regular meals, portion control, limit refined sugars, include protein and healthy fats.",
                "category": "health_metrics"
            },
            
            # Cholesterol
            {
                "topic": "Cholesterol Levels",
                "content": "Total cholesterol: <200 mg/dL desirable, 200-239 borderline high, 240+ high. LDL: <100 optimal, HDL: 40+ men, 50+ women. Manage with omega-3s, fiber, limit saturated fats.",
                "category": "health_metrics"
            },
            
            # Calorie Guidelines
            {
                "topic": "Daily Calorie Needs",
                "content": "Adult women: 1,600-2,400 calories/day. Adult men: 2,000-3,000 calories/day. Varies by age, activity level, height, weight. Sedentary adults need fewer calories.",
                "category": "calories"
            },
            {
                "topic": "Age-Based Calorie Needs",
                "content": "Ages 19-30: Higher calorie needs. Ages 31-50: Moderate needs. Ages 51+: Lower needs due to slower metabolism. Adjust portions accordingly.",
                "category": "calories"
            },
            
            # Macronutrients
            {
                "topic": "Macronutrient Balance",
                "content": "Healthy macro distribution: 45-65% carbs, 10-35% protein, 20-35% fat. Adjust based on health conditions - diabetics may need lower carbs, athletes need more protein.",
                "category": "macronutrients"
            },
            {
                "topic": "Carbohydrate Guidelines",
                "content": "Choose complex carbs: whole grains, vegetables, legumes. Limit simple sugars. For diabetes, count carbs and choose low glycemic index foods.",
                "category": "macronutrients"
            },
            {
                "topic": "Protein Requirements",
                "content": "Adults need 0.8g protein per kg body weight. Athletes: 1.2-2.0g/kg. Older adults: 1.0-1.2g/kg. Complete proteins from eggs, dairy, meat, quinoa, soy.",
                "category": "macronutrients"
            },
            
            # Vegetarian Nutrition
            {
                "topic": "Vegetarian Protein Sources",
                "content": "Excellent vegetarian proteins: lentils, chickpeas, quinoa, tofu, paneer, Greek yogurt, nuts, seeds. Combine legumes with grains for complete protein.",
                "category": "vegetarian"
            },
            {
                "topic": "Vegetarian Meal Ideas",
                "content": "Vegetarian breakfast: oatmeal with nuts, vegetable upma, idli sambar. Lunch: quinoa bowls, dal rice, paneer curry. Dinner: vegetable khichdi, lentil soups.",
                "category": "vegetarian"
            },
            
            # Non-Vegetarian Nutrition
            {
                "topic": "Lean Protein Sources",
                "content": "Lean proteins: chicken breast, fish (salmon, tuna), eggs, turkey. Fish provides omega-3 fatty acids. Choose grilled, baked, or steamed over fried preparations.",
                "category": "non_vegetarian"
            },
            
            # Meal Timing
            {
                "topic": "Meal Timing",
                "content": "Eat every 3-4 hours. Don't skip breakfast. Have largest meal at lunch when metabolism is highest. Light dinner 2-3 hours before bed. Include healthy snacks.",
                "category": "meal_timing"
            },
            
            # Food Alternatives
            {
                "topic": "Healthy Food Swaps",
                "content": "White rice → Brown rice/quinoa. White bread → Whole grain bread. Fried foods → Grilled/baked. Sugary drinks → Water/herbal tea. Refined oil → Olive oil.",
                "category": "alternatives"
            },
            {
                "topic": "Breakfast Alternatives",
                "content": "Oatmeal alternatives: quinoa porridge, chia pudding, smoothie bowls. Bread alternatives: whole grain options, lettuce wraps, sweet potato slices.",
                "category": "alternatives"
            },
            {
                "topic": "Snack Alternatives",
                "content": "Healthy snacks: nuts, fruits, Greek yogurt, hummus with vegetables, roasted chickpeas, homemade energy balls, vegetable soups.",
                "category": "alternatives"
            },
            
            # Health Conditions
            {
                "topic": "Diabetes Diet",
                "content": "Diabetes diet: Focus on low glycemic foods, count carbohydrates, eat regular meals, include fiber, limit sugars, choose lean proteins, monitor portions.",
                "category": "conditions"
            },
            {
                "topic": "Hypertension Diet",
                "content": "High blood pressure diet: Reduce sodium, increase potassium (bananas, oranges), choose DASH diet, limit processed foods, include whole grains, lean proteins.",
                "category": "conditions"
            },
            {
                "topic": "Heart Health",
                "content": "Heart-healthy diet: Omega-3 rich foods, limit saturated fats, include nuts, olive oil, fish, vegetables, fruits, whole grains. Avoid trans fats.",
                "category": "conditions"
            },
            
            # Hydration
            {
                "topic": "Hydration Guidelines",
                "content": "Drink 8-10 glasses of water daily. More if active or in hot weather. Signs of good hydration: pale yellow urine, no excessive thirst, good energy levels.",
                "category": "hydration"
            },
            
            # Portion Control
            {
                "topic": "Portion Control",
                "content": "Use smaller plates, fill half with vegetables, quarter with protein, quarter with carbs. Use hand as guide: palm-sized protein, fist-sized vegetables, cupped-hand carbs.",
                "category": "portions"
            }
        ]
        
        return knowledge_docs
    
    def _save_knowledge_base(self):
        """Save knowledge base to file"""
        os.makedirs('rag', exist_ok=True)
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
    
    def _load_or_create_embeddings(self):
        """Load existing embeddings or create new ones"""
        if os.path.exists(self.embeddings_file) and len(self.knowledge_base) > 0:
            try:
                with open(self.embeddings_file, 'rb') as f:
                    self.embeddings = pickle.load(f)
                
                # Check if embeddings match knowledge base size
                if len(self.embeddings) != len(self.knowledge_base):
                    print("Embeddings size mismatch, regenerating...")
                    self._create_embeddings()
            except Exception as e:
                print(f"Error loading embeddings: {e}, regenerating...")
                self._create_embeddings()
        else:
            self._create_embeddings()
    
    def _create_embeddings(self):
        """Create embeddings for the knowledge base"""
        if not self.knowledge_base:
            self.embeddings = np.array([])
            return
        
        print("Creating embeddings for knowledge base...")
        # Combine topic and content for better embedding
        texts = []
        for doc in self.knowledge_base:
            combined_text = f"{doc['topic']} {doc['content']}"
            texts.append(combined_text)
        
        # Generate embeddings
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Save embeddings
        os.makedirs('rag', exist_ok=True)
        with open(self.embeddings_file, 'wb') as f:
            pickle.dump(self.embeddings, f)
        
        print(f"Created and saved embeddings for {len(texts)} documents")
    
    def retrieve(self, query, top_k=3):
        """
        Retrieve the most relevant documents for a query
        """
        if not self.knowledge_base or len(self.embeddings) == 0:
            return []
        
        # Encode the query
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top-k most similar documents
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        retrieved_docs = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Threshold for relevance
                doc = self.knowledge_base[idx].copy()
                doc['similarity'] = float(similarities[idx])
                retrieved_docs.append(doc)
        
        return retrieved_docs
    
    def add_document(self, topic, content, category="general"):
        """Add a new document to the knowledge base"""
        new_doc = {
            "topic": topic,
            "content": content,
            "category": category
        }
        
        self.knowledge_base.append(new_doc)
        
        # Update embeddings
        combined_text = f"{topic} {content}"
        new_embedding = self.model.encode([combined_text])
        
        if len(self.embeddings) == 0:
            self.embeddings = new_embedding
        else:
            self.embeddings = np.vstack([self.embeddings, new_embedding])
        
        # Save updated knowledge base and embeddings
        self._save_knowledge_base()
        with open(self.embeddings_file, 'wb') as f:
            pickle.dump(self.embeddings, f)
        
        return True
    
    def get_statistics(self):
        """Get statistics about the knowledge base"""
        categories = {}
        for doc in self.knowledge_base:
            category = doc.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
        
        return {
            'total_documents': len(self.knowledge_base),
            'categories': categories,
            'embeddings_loaded': len(self.embeddings) > 0 if hasattr(self, 'embeddings') and self.embeddings is not None else False
        }