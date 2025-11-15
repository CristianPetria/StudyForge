# StudyForge - Visual Architecture Diagrams

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│                    (HTML/CSS/JavaScript)                        │
│              http://localhost:5001 (Web Interface)              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    HTTP Requests/Responses
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    FLASK WEB SERVER                              │
│                  (backend/app.py)                               │
│                 Listening on Port 5001                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                     REST API Endpoints
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   ┌────────────┐       ┌────────────┐      ┌─────────────┐
   │  Health    │       │ Templates  │      │   Guides    │
   │  Routes    │       │   Routes   │      │   Routes    │
   └────────────┘       └────────────┘      └─────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    Agent Coordinator
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │  Analysis    │  │  Template    │  │  Generation  │
   │   Agent      │  │  Matching    │  │    Agent     │
   │              │  │   Agent      │  │              │
   └──────────────┘  └──────────────┘  └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    External Services
                             │
        ┌────────────────────┼────────────────────┐
        │                    │
        ▼                    ▼
   ┌──────────────┐  ┌──────────────┐
   │  Mistral AI  │  │   Qdrant     │
   │  (Cloud API) │  │ (Vector DB)  │
   └──────────────┘  └──────────────┘
```

## 2. Request Processing Flow

```
USER BROWSER
    │
    │ POST /api/complete-workflow
    │ {content: "...", customization: {...}}
    │
    ▼
FLASK ROUTE (backend/routes/guides.py)
    │
    │ Extract request data
    │ Validate input
    │
    ▼
COORDINATOR (backend/agents/coordinator.py)
    │
    ├─────────────────────────────────────────────┐
    │                                             │
    ▼                                             │
[STEP 1] Analysis Agent                         │
    │                                             │
    ├─ Receives: raw content                      │
    ├─ Calls: Mistral AI /chat/complete           │
    ├─ Extracts: topic, concepts, difficulty     │
    │                                             │
    └─ Returns: analysis dict ─────────────────────┤
                                                  │
    ├─────────────────────────────────────────────┤
    │                                             │
    ▼                                             │
[STEP 2] Template Matching Agent                │
    │                                             │
    ├─ Receives: analysis dict                    │
    ├─ Creates: query embedding (Mistral)        │
    ├─ Searches: Qdrant vector database          │
    ├─ Finds: best matching template             │
    │                                             │
    └─ Returns: matched_template + score ────────┤
                                                  │
    ├─────────────────────────────────────────────┤
    │                                             │
    ▼                                             │
[STEP 3] Generation Agent                       │
    │                                             │
    ├─ Receives: template + analysis             │
    ├─ Calls: Mistral AI /chat/complete          │
    ├─ Generates: content for each section       │
    ├─ Applies: customization options            │
    │                                             │
    └─ Returns: study_guide dict ────────────────┤
                                                  │
    ▼
COORDINATOR AGGREGATES RESULTS
    │
    │ Combines:
    │ - analysis
    │ - matched_template
    │ - template_match_score
    │ - study_guide
    │
    ▼
FLASK ROUTE FORMATS RESPONSE
    │
    │ JSON Response:
    │ {
    │   "status": "success",
    │   "workflow": {...}
    │ }
    │
    ▼
USER BROWSER
    │
    ▼ Display Results
```

## 3. Agent Interaction Diagram

```
                    AGENT COORDINATOR
                   (Process Manager)
                    
                    workflow_request
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │  Analysis  │  │  Template  │  │ Generation │
    │   Agent    │  │  Matching  │  │   Agent    │
    │            │  │   Agent    │  │            │
    └────────────┘  └────────────┘  └────────────┘
           │                │                │
           │ analysis       │ match          │ guide
           │                │                │
           └────────────────┼────────────────┘
                            │
                    Coordinator Returns:
                    {
                      analysis,
                      matched_template,
                      template_match_score,
                      study_guide
                    }
                            │
                            ▼
                    API Response to Client
```

## 4. Data Flow Through Agents

```
┌─────────────────────────────────────────────────────────────────┐
│                   Raw User Input                                │
│            "Quantum computing is using..."                      │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
                    ╔════════════════════╗
                    ║ ANALYSIS AGENT     ║
                    ╚════════════════════╝
                              │
    Call Mistral:             │
    "Analyze this content"     │
                              ▼
    ┌──────────────────────────────────────┐
    │ ANALYSIS OUTPUT                      │
    ├──────────────────────────────────────┤
    │ {                                    │
    │   "topic": "Quantum Computing",      │
    │   "key_concepts": [...],             │
    │   "difficulty": "intermediate",      │
    │   "content_type": "lecture"          │
    │ }                                    │
    └──────────────────────────────────────┘
                              │
                              ▼
                    ╔════════════════════╗
                    ║ TEMPLATE MATCHING  ║
                    ║     AGENT          ║
                    ╚════════════════════╝
                              │
    Create embedding,         │
    Search Qdrant:            │
    "Find similar templates"   │
                              ▼
    ┌──────────────────────────────────────┐
    │ TEMPLATE OUTPUT                      │
    ├──────────────────────────────────────┤
    │ {                                    │
    │   "id": "concept-mapper",            │
    │   "name": "Concept Mapper",          │
    │   "sections": [...],                 │
    │   "match_score": 0.87                │
    │ }                                    │
    └──────────────────────────────────────┘
                              │
                              ▼
                    ╔════════════════════╗
                    ║ GENERATION AGENT   ║
                    ╚════════════════════╝
                              │
    Call Mistral:             │
    "Generate guide with      │
     template sections"        │
                              ▼
    ┌──────────────────────────────────────┐
    │ FINAL OUTPUT                         │
    ├──────────────────────────────────────┤
    │ {                                    │
    │   "template": "Concept Mapper",      │
    │   "topic": "Quantum Computing",      │
    │   "content": "## Core Concepts...",  │
    │   "metadata": {                      │
    │     "word_count": 1245,              │
    │     "sections": [...]                │
    │   }                                  │
    │ }                                    │
    └──────────────────────────────────────┘
```

## 5. API Endpoint Structure

```
/api
├── /health
│   └─ GET → Health check
│
├── /status
│   └─ GET → Service status
│
├── /templates
│   ├─ GET → List all templates
│   └─ GET /<id> → Get specific template
│
├── /analyze
│   └─ POST → Analyze content
│       Input: {content, content_type}
│       Output: {analysis}
│
├── /match-template
│   └─ POST → Match template to content
│       Input: {analysis, [selected_template_id]}
│       Output: {matched_template, match_score}
│
├── /generate-guide
│   └─ POST → Generate study guide
│       Input: {template_id, analysis, customization}
│       Output: {study_guide}
│
└── /complete-workflow
    └─ POST → Full workflow (analyze → match → generate)
        Input: {content, customization}
        Output: {complete workflow result}
```

## 6. Configuration Hierarchy

```
            Environment (.env file)
                    │
                    ▼
            ╔═══════════════════╗
            ║ backend/config.py ║
            ╚═══════════════════╝
            Contains:
            • API_KEYS
            • DATABASE_URLS
            • MODEL_NAMES
            • TEMPLATES
            • LOG_LEVEL
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    Agents      Routes       Utils
    (use         (use         (use
     config)     config)      config)
```

## 7. Agent Lifecycle

```
Application Start
    │
    ▼
┌──────────────────────────────┐
│ Import backend modules       │
│ - config.py (loads .env)     │
│ - clients.py (init clients)  │
│ - agents (lazy init)         │
└──────────────────────────────┘
    │
    ▼
┌──────────────────────────────┐
│ First Request Arrives        │
│ POST /api/complete-workflow  │
└──────────────────────────────┘
    │
    ▼
┌──────────────────────────────┐
│ Coordinator Needed           │
│ → Check: _coordinator == None│
│ → Create: AgentCoordinator() │
│ → Initialize agents          │
└──────────────────────────────┘
    │
    ▼
┌──────────────────────────────┐
│ Process Request              │
│ Agents handle workflow       │
└──────────────────────────────┘
    │
    ▼
┌──────────────────────────────┐
│ Subsequent Requests          │
│ → Use existing agents        │
│ → No reinitialization        │
└──────────────────────────────┘
```

## 8. Database Architecture

```
┌────────────────────────────────────────────┐
│            QDRANT VECTOR DATABASE          │
│                                            │
│  Collection: "learning_templates"         │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ Vector Points (Embeddings)           │ │
│  ├──────────────────────────────────────┤ │
│  │ Point 0 (ID: 0)                      │ │
│  │ Template: "lecture-digest"           │ │
│  │ Vector: [1024 dimensions]            │ │
│  ├──────────────────────────────────────┤ │
│  │ Point 1 (ID: 1)                      │ │
│  │ Template: "case-study-analyzer"      │ │
│  │ Vector: [1024 dimensions]            │ │
│  ├──────────────────────────────────────┤ │
│  │ Point 2 (ID: 2)                      │ │
│  │ Template: "concept-mapper"           │ │
│  │ Vector: [1024 dimensions]            │ │
│  ├──────────────────────────────────────┤ │
│  │ Point 3 (ID: 3)                      │ │
│  │ Template: "exam-prep-sprint"         │ │
│  │ Vector: [1024 dimensions]            │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  Used For: Vector Similarity Search       │
│  Each request creates query embedding,    │
│  finds most similar template               │
└────────────────────────────────────────────┘
```

## 9. Error Handling Flow

```
Request
  │
  ▼
Validation
  │
  ├─ NO Valid? → Return 400 (Bad Request)
  │
  ▼
YES
  │
  ▼
Agent Processing
  │
  ├─ Error? → Log error
  │           Return 500 (Internal Error)
  │
  ▼
Success
  │
  ├─ Format response
  ├─ HTTP 200 (Success)
  │
  ▼
Client Receives Response
```

## 10. Deployment Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Single Machine                                      │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │ • Python Flask Server (port 5001)                  │  │
│  │ • In-Memory Qdrant                                 │  │
│  │ • Mistral AI (cloud)                               │  │
│  │ • Debug Mode ON                                    │  │
│  └─────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                    PRODUCTION (Future)                      │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Load Balancer (nginx)                               │  │
│  └──────────┬──────────────────────┬──────────────────┘  │
│             │                      │                     │
│     ┌───────▼──────┐      ┌────────▼────────┐           │
│     │ Flask API #1 │      │  Flask API #2   │           │
│     └───────┬──────┘      └────────┬────────┘           │
│             │                      │                     │
│     ┌───────▼──────────────────────▼────────┐           │
│     │  Persistent Qdrant Instance            │           │
│     │  (Remote Database)                     │           │
│     └────────────────────────────────────────┘           │
│                      │                                    │
│     ┌────────────────┘                                   │
│     │                                                    │
│     ▼                                                    │
│  Mistral AI (Cloud)                                      │
└────────────────────────────────────────────────────────────┘
```

---

**These diagrams show the complete architecture, data flow, and system organization of StudyForge!**
