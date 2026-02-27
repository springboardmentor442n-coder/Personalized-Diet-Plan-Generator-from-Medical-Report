# 🥗 AI-NutriCare: Personalized Diet Plan Generator

A comprehensive Flask web application that generates personalized 7-day diet plans from medical reports using AI, featuring OCR text extraction, health analysis, and an intelligent nutrition chatbot.

## ✨ Features

### 🎯 Core Functionality
- **Medical Report Analysis**: Upload PDF/image files for OCR text extraction
- **Health Metrics Extraction**: Automatically extract BMI, blood sugar, cholesterol levels
- **AI Health Analysis**: LLM-powered interpretation of health conditions and risk assessment
- **7-Day Diet Plans**: Personalized meal plans with calories and macro distribution
- **Vegetarian/Non-Vegetarian Support**: Strict dietary preference validation
- **Plan Regeneration**: Improve plans with feedback-based regeneration

### 🤖 AI-Powered Features
- **RAG Chatbot**: Nutrition Q&A with context awareness
- **Meal Alternatives**: Suggest substitute meals based on preferences
- **Health Metric Explanations**: Detailed interpretations of medical values
- **Performance Optimized**: Fast response times with caching

### 💾 Data Management
- **SQLite Caching**: Store up to 20 recent sessions for instant loading
- **JSON Export**: Download complete diet plans and health analysis
- **Session Management**: Track plan versions and applied feedback
- **Automatic Cleanup**: Maintain optimal database performance

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Groq API key (free at https://console.groq.com/)

### Installation

1. **Clone/Extract the project**
```bash
cd AI-NutriCare
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your Groq API credentials
# Set your GROQ_API_KEY and choose a model
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

## 🔧 Configuration

### Groq API Configuration

#### Get Free API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Generate your API key

#### Available Models
```env
# Fast and efficient (recommended)
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-8b-8192

# Higher quality responses (slower)
GROQ_MODEL=llama3-70b-8192

# Good balance of speed and quality
GROQ_MODEL=mixtral-8x7b-32768

# Google's Gemma model
GROQ_MODEL=gemma-7b-it
```

### Performance Tuning
```env
# Adjust these for your needs
LLM_MAX_TOKENS=2000
LLM_TIMEOUT=30
MAX_SESSIONS=20
RAG_TOP_K=3
```

## 📖 Usage Guide

### 1. Generate Diet Plan
1. **Upload Medical Report** (Optional): PDF, PNG, or JPG files
2. **Enter Patient Details**: Age (required) and diet preference
3. **Click "Generate Diet Plan"**: AI analyzes and creates personalized plan
4. **Review Results**: View extracted metrics, health analysis, and 7-day plan

### 2. Regenerate with Feedback
1. **Provide Feedback**: Describe desired changes (e.g., "more protein", "Indian cuisine")
2. **Click "Regenerate Plan"**: AI creates improved version based on feedback
3. **Compare Versions**: Each regeneration is saved as a new version

### 3. Use Nutrition Chatbot
1. **Click "Open Chatbot"**: Access AI nutrition assistant
2. **Ask Questions**: 
   - "What does my BMI indicate?"
   - "Alternatives for Day 1 breakfast?"
   - "How many calories should I eat daily?"
3. **Get Personalized Answers**: Based on your health profile and diet plan

### 4. Export Results
1. **Click "Download as JSON"**: Get complete diet plan and analysis
2. **File Location**: Saved in `outputs/` folder with timestamp and version

## 🏗️ Architecture

### Project Structure
```
AI-NutriCare/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/             # HTML UI templates
│   ├── index.html         # Home page
│   ├── result.html        # Diet plan results
│   └── chat.html          # Chatbot interface
├── static/
│   └── style.css          # Custom styling
├── ocr/
│   └── extractor.py       # PDF/image text extraction
├── extraction/
│   └── metric_parser.py   # Health metrics parsing
├── llm/
│   ├── llm_client.py      # OpenAI-compatible API client
│   └── prompts.py         # AI prompt templates
├── diet/
│   ├── generator.py       # Diet plan generation
│   └── validator.py       # Plan validation & macros
├── rag/
│   ├── retriever.py       # Document retrieval system
│   └── rag_chat.py        # Chatbot with RAG
├── database/
│   └── db.py              # SQLite session management
├── utils/
│   ├── json_exporter.py   # Export functionality
│   └── session_manager.py # Caching logic
└── outputs/               # Generated JSON exports
```

### Key Components

#### 🔍 OCR & Extraction
- **PDF Processing**: `pdfplumber` for digital PDFs
- **Image OCR**: `pytesseract` for scanned documents
- **Metric Parsing**: Regex-based extraction of health values

#### 🧠 LLM Integration  
- **Groq API**: Fast, efficient language models
- **Structured Prompts**: JSON-only responses for consistency
- **Error Handling**: Retry logic and fallback mechanisms

#### 🍽️ Diet Generation
- **Age-based Recommendations**: Calorie needs by age group
- **Dietary Restrictions**: Strict vegetarian/non-vegetarian validation
- **Nutritional Balance**: Proper macro distribution (carbs/protein/fat)
- **Variety Enforcement**: Diverse meals across 7 days

#### 💬 RAG Chatbot
- **Knowledge Base**: Curated nutrition information
- **Semantic Search**: `sentence-transformers` for relevant retrieval
- **Context Awareness**: Personal health data integration
- **Meal Alternatives**: Suggest substitutions on request

#### 💾 Performance Optimization
- **Session Caching**: Instant loading for repeat users
- **Database Cleanup**: Automatic old session removal
- **JSON Validation**: Robust response parsing
- **Fallback Plans**: Pre-built diet plans if AI fails

## 📊 Health Metrics Supported

### Extracted Metrics
- **BMI**: Body Mass Index calculation and interpretation
- **Blood Sugar**: Fasting/random glucose levels (mg/dL)
- **Cholesterol**: Total cholesterol levels (mg/dL)
- **Blood Pressure**: Systolic/diastolic readings (mmHg)
- **Weight & Height**: With automatic BMI calculation

### Health Analysis
- **Risk Assessment**: Low/Medium/High health risk categorization
- **Condition Detection**: Diabetes, hypertension, obesity identification
- **Dietary Recommendations**: Personalized nutrition advice

## 🍽️ Diet Plan Features

### Meal Structure
- **4 Meals/Day**: Breakfast, Lunch, Snack, Dinner
- **7-Day Coverage**: Complete weekly meal planning
- **Calorie Targets**: Age-appropriate calorie distribution
- **Macro Balance**: Carbs (45-65%), Protein (10-35%), Fat (20-35%)

### Dietary Preferences
- **Vegetarian**: No meat, fish, eggs, or animal products (except dairy)
- **Non-Vegetarian**: Includes both veg and non-veg options
- **Validation**: Strict checking for dietary compliance

### Customization
- **Feedback Integration**: Regenerate with specific requests
- **Version Tracking**: Multiple plan versions per session
- **Alternative Suggestions**: Chatbot provides meal substitutes

## 🛠️ Troubleshooting

### Common Issues

#### 1. OCR Not Working
```bash
# Install Tesseract OCR
# Windows: Download from GitHub releases
# Linux: sudo apt install tesseract-ocr
# Mac: brew install tesseract
```

#### 2. LLM API Errors
- Check Groq API key in `.env` file
- Verify model name is supported
- Ensure sufficient API credits
- Check network connectivity

#### 3. Database Issues
- Delete `ai_nutricare.db` to reset
- Check write permissions in project folder
- Ensure SQLite is available

#### 4. Missing Dependencies
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Performance Tips

#### Speed Optimization
- Use faster models (llama3-8b-8192 vs llama3-70b-8192)
- Enable caching for repeat users
- Reduce `LLM_MAX_TOKENS` if responses are too long
- Clean up old sessions regularly

#### Memory Management
- Lower `MAX_SESSIONS` if memory constrained
- Use smaller sentence transformer models
- Clear browser cache if UI appears slow

## 🔒 Security Considerations

### API Keys
- Never commit `.env` file to version control
- Use strong, unique API keys
- Rotate keys periodically
- Monitor API usage and costs

### File Uploads
- 16MB file size limit enforced
- Only PDF, PNG, JPG files accepted
- Files deleted after processing
- No persistent file storage

### Session Management
- Automatic cleanup of old sessions (20 max)
- No personal data stored beyond session
- SQLite database stays local

## 🚀 Production Deployment

### Environment Setup
```bash
# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=False

# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Configuration Updates
```env
# Production settings in .env
FLASK_SECRET_KEY=your-strong-secret-key
FLASK_DEBUG=False
LLM_TIMEOUT=60
MAX_SESSIONS=50
```

### Security Headers
Consider adding reverse proxy (nginx) with:
- HTTPS/SSL certificates
- Security headers (CSRF, XSS protection)
- Rate limiting
- File upload restrictions

## 📈 Monitoring

### Application Logs
- Check console output for errors
- Monitor API call success rates
- Track session cache hit rates
- Watch database growth

### Performance Metrics
- LLM response times
- OCR processing duration
- Database query performance
- RAG retrieval accuracy

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Install dev dependencies
4. Make changes with tests
5. Submit pull request

### Code Style
- Follow PEP 8 for Python
- Use type hints where possible
- Add docstrings to functions
- Include error handling

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Groq for fast LLM inference
- Tesseract OCR team
- Sentence Transformers library
- Flask community
- Medical nutrition research

---

## 📞 Support

For issues, questions, or contributions:
1. Check existing GitHub issues
2. Create new issue with details
3. Include error logs and configuration
4. Provide steps to reproduce problems

**🎉 Enjoy creating personalized nutrition plans with AI-NutriCare!**