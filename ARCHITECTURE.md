# StudyForge Project Structure & Architecture Guide

## 🏗️ Project Directory Structure

```
StudyForge/
│
├── 📁 backend/                         # Main backend application
│   ├── 📁 agents/                      # AI Agent modules
│   │   ├── __init__.py                # Agent package exports
│   │   ├── analysis_agent.py          # Content analysis AI agent
│   │   ├── template_matching_agent.py # Template matching AI agent
│   │   ├── generation_agent.py        # Study guide generation AI agent
│   │   └── coordinator.py             # Agent orchestration & workflow
│   │
│   ├── 📁 routes/                      # API endpoints
│   │   ├── __init__.py                # Route registration
│   │   ├── health.py                  # Health check endpoints
│   │   ├── templates.py               # Template management endpoints
│   │   └── guides.py                  # Study guide generation endpoints
│   │
│   ├── 📁 utils/                       # Utilities and helpers
│   │   ├── __init__.py                # Utils package exports
│   │   ├── clients.py                 # Mistral & Qdrant client initialization
│   │   └── logger.py                  # Centralized logging configuration
│   │
│   ├── __init__.py                    # Backend package initialization
│   ├── config.py                      # Global configuration & constants
│   └── app.py                         # Flask application factory
│
├── 📁 frontend/                        # Web interface
│   ├── 📁 templates/                   # HTML templates
│   │   └── index.html                 # Main web interface
│   │
│   └── 📁 static/                      # Static assets
│       ├── 📁 css/
│       │   └── style.css              # Application styles
│       ├── 📁 js/
│       │   └── app.js                 # Frontend JavaScript
│       └── 📁 images/                 # Image assets
│
├── main.py                            # Application entry point
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── run.bat                            # Windows startup script
├── run.sh                             # Linux/Mac startup script
└── README.md                          # Project documentation
```

## 🧠 Agent Architecture

### Overview

The application uses a **modular multi-agent architecture** where specialized AI agents handle different tasks:

```
User Request
    ↓
┌─────────────────────────────────────────────────┐
│           AGENT COORDINATOR                     │
│  Orchestrates workflow and manages data flow   │
└─────┬───────────────────────┬──────────────┬────┘
      ↓                       ↓              ↓
  ┌─────────┐          ┌──────────┐    ┌──────────┐
  │ Analysis│          │ Template │    │Generation│
  │ Agent   │ ─────→   │ Matching │─→ │ Agent    │
  │         │          │ Agent    │    │          │
  └─────────┘          └──────────┘    └──────────┘
      ↓                    ↓                ↓
  Analyze            Match to             Generate
  Content            Template             Guide
```

### 1. Analysis Agent (`backend/agents/analysis_agent.py`)

**Responsibility**: Analyze user-provided content

**Process**:
1. Receives raw content (text, notes, lectures, etc.)
2. Calls Mistral AI to analyze and extract:
   - Topic/Title
   - Key concepts
   - Content type (lecture, case study, textbook, article, notes)
   - Difficulty level (beginner, intermediate, advanced)
   - Estimated study time
3. Returns structured analysis

**Key Methods**:
- `analyze_content(content, content_type)` → analysis dict

**Example Output**:
```json
{
  "status": "success",
  "analysis": {
    "topic": "Quantum Computing Basics",
    "key_concepts": ["superposition", "entanglement", "qubit"],
    "detected_content_type": "lecture",
    "difficulty_level": "intermediate",
    "estimated_study_time": "45 minutes"
  }
}
```

### 2. Template Matching Agent (`backend/agents/template_matching_agent.py`)

**Responsibility**: Match analyzed content to the best template

**Process**:
1. Initializes Qdrant with template embeddings (one-time setup)
2. For each analysis:
   - Creates a query embedding from analysis data
   - Searches Qdrant vector database for similar templates
   - Returns best match with confidence score

**Available Templates**:
- **Lecture Digest**: For university lectures → structured summary
- **Case Study Analyzer**: For business cases → problem analysis
- **Concept Mapper**: For technical content → relationship mapping
- **Exam Prep Sprint**: For exam preparation → focused review

**Key Methods**:
- `initialize()` → Sets up Qdrant collection with embeddings
- `match_template(analysis, selected_template_id)` → template dict

**Example Output**:
```json
{
  "status": "success",
  "matched_template": {
    "id": "concept-mapper",
    "name": "Concept Mapper",
    "sections": ["Core Concepts", "Relationships", "Code Examples", ...]
  },
  "match_score": 0.87,
  "method": "ai_matched"
}
```

### 3. Generation Agent (`backend/agents/generation_agent.py`)

**Responsibility**: Generate customized study guides

**Process**:
1. Receives template and analyzed content
2. Calls Mistral AI with specialized generation prompt
3. AI generates structured content for each template section
4. Applies customization options (length, examples, questions)
5. Returns formatted study guide

**Customization Options**:
- `length`: "short" | "medium" | "long"
- `include_examples`: true | false
- `include_questions`: true | false

**Key Methods**:
- `generate_guide(template_id, analysis, customization)` → guide dict

**Example Output**:
```json
{
  "status": "success",
  "study_guide": {
    "template": "Concept Mapper",
    "topic": "Quantum Computing Basics",
    "content": "## Core Concepts\n\nSuperposition is...",
    "metadata": {
      "word_count": 1245,
      "sections": [...]
    }
  }
}
```

### 4. Agent Coordinator (`backend/agents/coordinator.py`)

**Responsibility**: Orchestrate complete workflow

**Process**:
1. Receives user request
2. Delegates to each agent in sequence:
   - Analysis Agent → analyze content
   - Template Matching Agent → find best template
   - Generation Agent → generate guide
3. Aggregates results and returns complete workflow output

**Key Methods**:
- `process_study_request(content, content_type, template_id, customization)` → workflow dict

## 🔌 API Endpoints

### Health & Status
```
GET /api/health
GET /api/status
```

### Templates
```
GET /api/templates              # List all templates
GET /api/templates/<id>         # Get specific template
```

### Study Guides (Step-by-step)
```
POST /api/analyze               # Step 1: Analyze content
POST /api/match-template        # Step 2: Match template
POST /api/generate-guide        # Step 3: Generate guide
```

### Complete Workflow
```
POST /api/complete-workflow     # All steps in one request
```

## 🔄 Data Flow Examples

### Example 1: Complete Workflow

**Request**:
```bash
POST /api/complete-workflow
{
  "content": "In quantum computing, superposition allows qubits...",
  "customization_options": {
    "length": "medium",
    "include_examples": true,
    "include_questions": true
  }
}
```

**Internal Flow**:
1. **Coordinator** receives request
2. **Coordinator** → **Analysis Agent**: analyze content
3. **Analysis Agent** → Mistral AI: extract information
4. **Analysis Agent** ← Mistral AI: returns analysis
5. **Coordinator** → **Template Matching Agent**: find best template
6. **Template Matching Agent** → Qdrant: semantic search
7. **Template Matching Agent** ← Qdrant: matched template
8. **Coordinator** → **Generation Agent**: generate guide
9. **Generation Agent** → Mistral AI: generate content
10. **Generation Agent** ← Mistral AI: returns guide
11. **Coordinator** ← All agents: aggregate results
12. **Client** ← Coordinator: complete workflow result

**Response**:
```json
{
  "status": "success",
  "workflow": {
    "analysis": { ... },
    "matched_template": { ... },
    "template_match_score": 0.87,
    "study_guide": { ... }
  }
}
```

## 🔧 Adding New Agents

### Step 1: Create Agent Module

Create `backend/agents/your_agent.py`:

```python
from backend.utils.clients import get_mistral_client
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class YourAgent:
    def __init__(self):
        self.mistral_client = get_mistral_client()
    
    def process(self, data):
        """Process data and return results"""
        logger.info("Processing with YourAgent")
        # Your agent logic here
        return {"status": "success", "result": data}

_agent = None

def get_your_agent():
    global _agent
    if _agent is None:
        _agent = YourAgent()
    return _agent
```

### Step 2: Register in Coordinator

Update `backend/agents/coordinator.py`:

```python
def process_workflow(self, ...):
    # ... existing steps ...
    your_agent = get_your_agent()
    result = your_agent.process(data)
    # ... continue ...
```

### Step 3: Create API Routes

Create `backend/routes/your_routes.py`:

```python
from flask import Blueprint, request, jsonify
from backend.agents.your_agent import get_your_agent

your_bp = Blueprint('your_feature', __name__, url_prefix='/api')

@your_bp.route('/your-endpoint', methods=['POST'])
def your_endpoint():
    data = request.get_json()
    agent = get_your_agent()
    result = agent.process(data)
    return jsonify(result), 200
```

### Step 4: Register Routes

Update `backend/routes/__init__.py`:

```python
from backend.routes.your_routes import your_bp

def register_routes(app):
    app.register_blueprint(your_bp)
    # ... other routes ...
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5001
HOST=0.0.0.0

# Mistral AI
MISTRAL_API_KEY=your_key_here

# Qdrant
QDRANT_IN_MEMORY=True
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# Logging
LOG_LEVEL=INFO
```

## 🚀 Deployment Considerations

### Local Development
- Uses in-memory Qdrant (`QDRANT_IN_MEMORY=True`)
- Debug mode enabled
- No authentication required

### Cloud Deployment
- Switch to persistent Qdrant instance
- Use environment-specific .env files
- Add authentication & API key validation
- Implement rate limiting
- Use reverse proxy (nginx/Apache)
- Set up monitoring & logging

## 📊 Dependencies

Key Python packages:
- **Flask**: Web framework
- **Flask-CORS**: Enable cross-origin requests
- **mistralai**: Mistral AI client
- **qdrant-client**: Vector database client
- **python-dotenv**: Environment configuration

## 🔐 Security Notes

1. Never commit `.env` file
2. Use API key validation in production
3. Implement rate limiting
4. Add input validation and sanitization
5. Use HTTPS in production
6. Implement authentication for sensitive endpoints

## 📚 Learning Resources

- [Mistral AI Documentation](https://docs.mistral.ai)
- [Qdrant Documentation](https://qdrant.tech/documentation)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Vector Database Concepts](https://www.pinecone.io/learn/vector-database)
