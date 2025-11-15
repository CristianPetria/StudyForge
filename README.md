# StudyForge - AI-Powered Study Guide Generator

A modular, scalable web application that uses multiple AI agents to analyze study content and generate customized study guides.

## Architecture Overview

```
StudyForge/
├── backend/                    # Backend API server
│   ├── agents/                 # AI agents for different tasks
│   │   ├── analysis_agent.py   # Content analysis agent
│   │   ├── template_matching_agent.py  # Template matching agent
│   │   ├── generation_agent.py # Study guide generation agent
│   │   └── coordinator.py      # Orchestrates agents
│   ├── routes/                 # API endpoints
│   │   ├── health.py           # Health check endpoints
│   │   ├── templates.py        # Template management endpoints
│   │   └── guides.py           # Study guide endpoints
│   ├── utils/                  # Utilities
│   │   ├── clients.py          # AI client initialization
│   │   └── logger.py           # Logging configuration
│   ├── config.py               # Configuration management
│   └── app.py                  # Flask application factory
│
├── frontend/                   # Web interface
│   ├── templates/              # HTML templates
│   │   └── index.html
│   └── static/                 # Static assets
│       ├── css/
│       ├── js/
│       └── images/
│
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── .env.example               # Environment variables template
```

## System Architecture

### Modular Agent System

StudyForge uses independent AI agents for different tasks:

1. **Analysis Agent** - Analyzes user content to extract key information
   - Identifies topic and key concepts
   - Detects content type (lecture, case study, textbook, etc.)
   - Assesses difficulty level and estimated study time

2. **Template Matching Agent** - Matches analyzed content to appropriate templates
   - Uses vector embeddings for semantic matching
   - Supports user-selected templates
   - Provides confidence scores

3. **Generation Agent** - Generates customized study guides
   - Creates structured content for each template section
   - Applies customization options (length, examples, questions)
   - Formats final output

4. **Agent Coordinator** - Orchestrates the complete workflow
   - Manages communication between agents
   - Handles end-to-end workflow: analyze → match → generate

### API Endpoints

#### Health & Status
- `GET /api/health` - Health check
- `GET /api/status` - Detailed service status

#### Templates
- `GET /api/templates` - List all templates
- `GET /api/templates/<template_id>` - Get specific template

#### Study Guides
- `POST /api/analyze` - Analyze content
- `POST /api/match-template` - Match template to content
- `POST /api/generate-guide` - Generate study guide
- `POST /api/complete-workflow` - End-to-end workflow

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- pip (Python package manager)
- Mistral AI API key (get from: https://console.mistral.ai/)
- (Optional) Qdrant instance for production

### 2. Installation

1. Clone the repository:
```bash
git clone <repository_url>
cd StudyForge
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your Mistral API key
```

### 3. Running the Application

**Local Development:**
```bash
python main.py
```

The application will start on `http://localhost:5001`

**With Custom Port:**
```bash
set PORT=8080
python main.py
```

## Usage Examples

### Complete Workflow (Analyze → Match → Generate)

```python
curl -X POST http://localhost:5001/api/complete-workflow \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your study material here...",
    "content_type": "text",
    "customization_options": {
      "length": "medium",
      "include_examples": true,
      "include_questions": true
    }
  }'
```

### Step-by-Step Workflow

1. **Analyze Content:**
```bash
curl -X POST http://localhost:5001/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"content": "Your content here...", "content_type": "text"}'
```

2. **Get Available Templates:**
```bash
curl http://localhost:5001/api/templates
```

3. **Match Template:**
```bash
curl -X POST http://localhost:5001/api/match-template \
  -H "Content-Type: application/json" \
  -d '{"analysis": {...}}'
```

4. **Generate Study Guide:**
```bash
curl -X POST http://localhost:5001/api/generate-guide \
  -H "Content-Type: application/json" \
  -d '{"template_id": "lecture-digest", "analysis": {...}}'
```

## Configuration

Edit `.env` file to configure:

- `MISTRAL_API_KEY` - Your Mistral API key
- `QDRANT_IN_MEMORY` - Use in-memory vector database (True for development)
- `QDRANT_URL` - Qdrant server URL (for production)
- `PORT` - Server port (default: 5001)
- `FLASK_DEBUG` - Debug mode (True/False)

## Adding New Agents

To add a new specialized agent:

1. Create `backend/agents/your_agent.py`:
```python
class YourAgent:
    def __init__(self):
        self.mistral_client = get_mistral_client()
    
    def process(self, data):
        # Your agent logic here
        pass

def get_your_agent():
    global _agent
    if _agent is None:
        _agent = YourAgent()
    return _agent
```

2. Register in coordinator and create corresponding API endpoint in `backend/routes/`

3. Import and use in workflows

## Technology Stack

- **Backend**: Flask (Python)
- **AI**: Mistral AI API
- **Vector DB**: Qdrant
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: RESTful architecture

## Future Enhancements

- [ ] Cloud deployment (AWS, Google Cloud, Azure)
- [ ] PDF and URL content parsing
- [ ] Custom agent types
- [ ] Study guide export formats (PDF, Word, Markdown)
- [ ] Collaborative features
- [ ] Analytics and usage tracking
- [ ] Advanced caching strategies
- [ ] Rate limiting and authentication

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.