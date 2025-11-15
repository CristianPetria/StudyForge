# StudyForge - Project Structure & Agent Communication Guide

## 📦 Complete Project Structure

```
StudyForge/
│
├── 📄 main.py                    ← Application entry point (run this)
├── 📄 requirements.txt           ← Python dependencies
├── 📄 .env.example               ← Environment variables template
├── 📄 run.bat                    ← Windows startup script
├── 📄 run.sh                     ← Linux/Mac startup script
├── 📄 README.md                  ← Project overview & setup guide
├── 📄 ARCHITECTURE.md            ← Detailed architecture documentation
├── 📄 QUICKSTART.md              ← Quick reference guide
│
├── 📁 backend/                   ← Backend API server (core logic)
│   │
│   ├── 📄 config.py              ← Central configuration & constants
│   ├── 📄 app.py                 ← Flask application factory
│   ├── 📄 __init__.py            ← Backend package initialization
│   │
│   ├── 📁 agents/                ← AI Agent modules
│   │   ├── 📄 __init__.py
│   │   ├── 📄 analysis_agent.py          ← Analyzes study content
│   │   ├── 📄 template_matching_agent.py ← Matches to templates
│   │   ├── 📄 generation_agent.py        ← Generates study guides
│   │   └── 📄 coordinator.py             ← Orchestrates workflow
│   │
│   ├── 📁 routes/                ← API endpoint definitions
│   │   ├── 📄 __init__.py
│   │   ├── 📄 health.py          ← Health check endpoints
│   │   ├── 📄 templates.py       ← Template endpoints
│   │   └── 📄 guides.py          ← Guide generation endpoints
│   │
│   └── 📁 utils/                 ← Utility modules
│       ├── 📄 __init__.py
│       ├── 📄 clients.py         ← AI client initialization
│       └── 📄 logger.py          ← Centralized logging
│
└── 📁 frontend/                  ← Web interface
    ├── 📁 templates/             ← HTML files
    │   └── 📄 index.html         ← Main web page
    └── 📁 static/                ← Static assets
        ├── 📁 css/
        │   └── 📄 style.css
        ├── 📁 js/
        │   └── 📄 app.js
        └── 📁 images/
```

## 🧠 Agent System Overview

### Four Independent Agents

Your system has **four specialized AI agents** that work together:

```
┌──────────────────────────────────────────────────────────────────────┐
│                      USER REQUEST                                     │
│              (Content to analyze and convert to study guide)          │
└─────────────────────────────┬──────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────────┐
│                   AGENT COORDINATOR                                   │
│          (Orchestrates workflow between agents)                      │
└────┬─────────────────────────────┬──────────────────────────┬────────┘
     ↓                             ↓                          ↓
┌──────────────┐         ┌─────────────────┐       ┌──────────────────┐
│  ANALYSIS    │         │ TEMPLATE        │       │  GENERATION      │
│   AGENT      │  ─────→ │ MATCHING AGENT  │ ────→ │  AGENT           │
│              │         │                 │       │                  │
└──────────────┘         └─────────────────┘       └──────────────────┘
 Extract info:           Match to template:        Generate guide:
 • Topic                 • Uses embeddings        • Create sections
 • Concepts              • Qdrant search          • Apply options
 • Difficulty            • Returns match          • Format output
 • Time estimate         • Confidence score       • Return guide
```

## 📡 Agent Communication Flow

### 1️⃣ Analysis Agent (`backend/agents/analysis_agent.py`)

**What it does**: Analyzes user content

**Input**:
```python
{
    "content": "Your study material text...",
    "content_type": "text"  # or "pdf", "url"
}
```

**Process**:
1. Receives raw content
2. Sends to Mistral AI for analysis
3. Parses JSON response
4. Extracts structured information

**Output**:
```python
{
    "status": "success",
    "analysis": {
        "topic": "Quantum Computing",
        "key_concepts": ["superposition", "entanglement", "quantum gates"],
        "detected_content_type": "lecture",
        "difficulty_level": "intermediate",
        "estimated_study_time": "45 minutes",
        "analysis_id": "analysis_12345"
    }
}
```

**Mistral AI Calls**: 1 (chat.complete)

---

### 2️⃣ Template Matching Agent (`backend/agents/template_matching_agent.py`)

**What it does**: Finds the best template for the content

**Initialization** (one-time):
1. Takes all 4 templates
2. Embeds them with Mistral
3. Stores in Qdrant vector database

**Input**:
```python
{
    "analysis": {
        "topic": "Quantum Computing",
        "detected_content_type": "lecture",
        ...
    }
    # OR user selected manually:
    # "selected_template_id": "lecture-digest"
}
```

**Process**:
1. If user selected template → return immediately
2. Otherwise:
   - Create query from analysis
   - Embed query with Mistral
   - Search Qdrant for similar templates
   - Return best match with score

**Output**:
```python
{
    "status": "success",
    "matched_template": {
        "id": "concept-mapper",
        "name": "Concept Mapper",
        "description": "Extract and organize technical concepts...",
        "sections": ["Core Concepts", "Relationships", "Code Examples"]
    },
    "match_score": 0.87,
    "method": "ai_matched"  # or "user_selected"
}
```

**Available Templates**:
1. **lecture-digest** - For lectures → structured summary
2. **case-study-analyzer** - For business cases → analysis
3. **concept-mapper** - For technical content → relationships
4. **exam-prep-sprint** - For exams → focused review

**Mistral AI Calls**: 1 embedding call (for query)

---

### 3️⃣ Generation Agent (`backend/agents/generation_agent.py`)

**What it does**: Generates the final study guide

**Input**:
```python
{
    "template_id": "concept-mapper",
    "analysis": {
        "content": "Original study material",
        "topic": "Quantum Computing",
        ...
    },
    "customization_options": {
        "length": "medium",           # "short", "medium", "long"
        "include_examples": true,
        "include_questions": true
    }
}
```

**Process**:
1. Loads template structure
2. Creates generation prompt
3. Sends to Mistral AI
4. AI generates content for each section
5. Applies customization options
6. Returns formatted guide

**Output**:
```python
{
    "status": "success",
    "study_guide": {
        "template": "Concept Mapper",
        "topic": "Quantum Computing",
        "content": "## Core Concepts\n\nSuperposition is...\n\n## Relationships\n...",
        "metadata": {
            "word_count": 1245,
            "customization_applied": {...},
            "sections": ["Core Concepts", "Relationships", ...]
        }
    }
}
```

**Mistral AI Calls**: 1 (chat.complete)

---

### 4️⃣ Agent Coordinator (`backend/agents/coordinator.py`)

**What it does**: Orchestrates the complete workflow

**Input**:
```python
{
    "content": "Study material...",
    "content_type": "text",
    "template_id": null,  # Optional
    "customization": {"length": "medium", ...}
}
```

**Process**:
```
1. Call Analysis Agent
   └─ Get: analysis
   
2. Call Template Matching Agent
   └─ Pass: analysis
   └─ Get: matched_template, match_score
   
3. Call Generation Agent
   └─ Pass: template_id, analysis, customization
   └─ Get: study_guide
   
4. Aggregate all results
   └─ Return: Complete workflow result
```

**Output**:
```python
{
    "status": "success",
    "workflow": {
        "analysis": {...},
        "matched_template": {...},
        "template_match_score": 0.87,
        "study_guide": {...}
    }
}
```

---

## 🔌 API Routes

### Health Check
```
GET /api/health
GET /api/status
```

### Templates
```
GET /api/templates           # List all templates
GET /api/templates/<id>      # Get specific template
```

### Study Guides

**Option 1: Complete Workflow (One Request)**
```
POST /api/complete-workflow
Body: {
  "content": "...",
  "customization_options": {...}
}
Returns: Complete workflow result
```

**Option 2: Step-by-Step**
```
1. POST /api/analyze
   Body: {"content": "..."}
   Returns: analysis

2. POST /api/match-template
   Body: {"analysis": {...}}
   Returns: matched_template

3. POST /api/generate-guide
   Body: {"template_id": "...", "analysis": {...}}
   Returns: study_guide
```

---

## 🔄 Complete Request/Response Cycle

### Example: Complete Workflow

**Frontend sends**:
```bash
curl -X POST http://localhost:5001/api/complete-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Quantum computing uses superposition...",
    "content_type": "text",
    "customization_options": {
      "length": "medium",
      "include_examples": true,
      "include_questions": true
    }
  }'
```

**Backend processes**:
```
1. Flask receives request
   ↓
2. Routes to /api/complete-workflow endpoint
   ↓
3. Coordinator is created (if not exists)
   ↓
4. Coordinator.process_study_request() is called
   ↓
5. Step 1: Analysis Agent analyzes content
   → Calls Mistral: analyze content
   → Returns: {topic, concepts, difficulty, ...}
   ↓
6. Step 2: Template Matching Agent matches template
   → Creates query embedding (Mistral)
   → Searches Qdrant vector database
   → Returns: best matching template
   ↓
7. Step 3: Generation Agent generates guide
   → Calls Mistral: generate structured guide
   → Applies customization options
   → Returns: formatted study guide
   ↓
8. Coordinator aggregates results
   ↓
9. Returns complete response
```

**Backend responds**:
```json
{
  "status": "success",
  "workflow": {
    "analysis": {
      "topic": "Quantum Computing",
      "key_concepts": ["superposition", "entanglement"],
      "difficulty_level": "intermediate",
      "estimated_study_time": "45 minutes"
    },
    "matched_template": {
      "id": "concept-mapper",
      "name": "Concept Mapper",
      "sections": ["Core Concepts", "Relationships", ...]
    },
    "template_match_score": 0.87,
    "study_guide": {
      "template": "Concept Mapper",
      "topic": "Quantum Computing",
      "content": "## Core Concepts\n\n...",
      "metadata": {
        "word_count": 1245,
        "customization_applied": {...}
      }
    }
  }
}
```

---

## 🛠️ Configuration Hierarchy

```
System Configuration
    ↓
┌─────────────────────────────────────────┐
│ backend/config.py                       │
│ (Loads from .env)                       │
├─────────────────────────────────────────┤
│ • API Keys (MISTRAL_API_KEY)            │
│ • Database (QDRANT_URL)                 │
│ • Server Settings (HOST, PORT)          │
│ • Model Names (MISTRAL_CHAT_MODEL)      │
│ • Collection Names (QDRANT_TEMPLATE...) │
│ • Templates Definitions                 │
└─────────────────────────────────────────┘
    ↓
Imported by all modules:
├── backend/utils/clients.py       (Initializes AI clients)
├── backend/utils/logger.py        (Sets up logging)
├── backend/agents/*.py            (Uses config values)
└── backend/routes/*.py            (Uses config values)
```

---

## 🚀 How to Run

### 1. Setup
```bash
# Windows
run.bat

# Linux/Mac
bash run.sh
```

### 2. Configure
```bash
# Copy example config
cp .env.example .env

# Edit .env and add your Mistral API key
# MISTRAL_API_KEY=your_key_here
```

### 3. Start
```bash
python main.py
```

### 4. Test
```bash
# Check health
curl http://localhost:5001/api/health

# Get templates
curl http://localhost:5001/api/templates

# Run complete workflow
curl -X POST http://localhost:5001/api/complete-workflow \
  -H "Content-Type: application/json" \
  -d '{"content": "Your study material..."}'
```

---

## 🔐 Agent Initialization

Agents use **lazy initialization** for efficiency:

```python
# First call creates the agent
agent = get_analysis_agent()  # Creates instance, initializes Mistral client

# Subsequent calls return same instance
agent = get_analysis_agent()  # Returns existing instance (no reinit)
```

This pattern saves resources and is thread-safe.

---

## 📊 Data Flow Summary

```
Request → Flask Route → Agent/Coordinator → Mistral API → Qdrant → Response

Typical calls per request:
- 3 Mistral AI calls (analysis, matching embedding, generation)
- 1 Qdrant search (template matching)
```

---

## 🆕 Adding Features

### Add a New Agent
1. Create `backend/agents/new_agent.py`
2. Implement agent class with `process()` method
3. Add getter function with lazy initialization
4. Register in `coordinator.py`
5. Create route in `backend/routes/new_routes.py`
6. Register route in `backend/routes/__init__.py`

### Add a New Template
1. Edit `backend/config.py`
2. Add to `STUDY_TEMPLATES` list
3. Template Matching Agent automatically indexes it

### Add a New Route
1. Create `backend/routes/new_routes.py`
2. Define Blueprint with endpoints
3. Register in `backend/routes/__init__.py`

---

## 📝 Summary

| Component | Purpose | Location | Files |
|-----------|---------|----------|-------|
| **Analysis Agent** | Analyzes content | `backend/agents/` | `analysis_agent.py` |
| **Template Matcher** | Matches templates | `backend/agents/` | `template_matching_agent.py` |
| **Generation Agent** | Generates guides | `backend/agents/` | `generation_agent.py` |
| **Coordinator** | Orchestrates workflow | `backend/agents/` | `coordinator.py` |
| **Configuration** | Centralized config | `backend/` | `config.py` |
| **Clients** | AI client setup | `backend/utils/` | `clients.py` |
| **Logging** | Log management | `backend/utils/` | `logger.py` |
| **Routes** | API endpoints | `backend/routes/` | `*.py` |
| **Frontend** | Web interface | `frontend/` | HTML, CSS, JS |

---

**Your StudyForge project is now production-ready with a scalable, modular architecture!** 🎉
