"""
StudyForge - AI-Powered Study Guide Generator
A Flask application that analyzes user content and generates customized study guides
using Mistral AI and Qdrant vector database.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from mistralai import Mistral
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
import json
import logging
import time

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes (adjust origins in production)
CORS(app)

# Configuration
app.config['MISTRAL_API_KEY'] = os.getenv('MISTRAL_API_KEY')
app.config['QDRANT_URL'] = os.getenv('QDRANT_URL')
app.config['QDRANT_API_KEY'] = os.getenv('QDRANT_API_KEY')

# Initialize Mistral AI client
mistral_client = None
if app.config['MISTRAL_API_KEY']:
    try:
        mistral_client = Mistral(api_key=app.config['MISTRAL_API_KEY'])
        logger.info("✅ Mistral AI client initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Mistral client: {e}")
else:
    logger.warning("⚠️  Mistral API key not found")

# Initialize Qdrant client (in-memory for hackathon speed)
qdrant_client = None
try:
    qdrant_client = QdrantClient(":memory:")
    logger.info("✅ Qdrant in-memory client initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize Qdrant client: {e}")

# ============================================================================
# TEMPLATES LIBRARY
# ============================================================================

STUDY_TEMPLATES = [
    {
        "id": "lecture-digest",
        "name": "Lecture Digest",
        "description": "Transform lengthy university lectures into concise, structured summaries with key concepts, definitions, and examples.",
        "icon_emoji": "=�",
        "example_use_case": "Converting 2-hour economics lecture notes into a 2-page study guide",
        "sections": ["Key Concepts", "Definitions", "Important Examples", "Summary Points"]
    },
    {
        "id": "case-study-analyzer",
        "name": "Case Study Analyzer",
        "description": "Break down business cases into problem statements, stakeholder analysis, solutions, and key takeaways.",
        "icon_emoji": "=�",
        "example_use_case": "Analyzing Harvard Business School cases for strategic management courses",
        "sections": ["Problem Statement", "Stakeholders", "Analysis Framework", "Recommendations", "Key Learnings"]
    },
    {
        "id": "concept-mapper",
        "name": "Concept Mapper",
        "description": "Extract and organize technical concepts with their relationships, dependencies, and practical applications.",
        "icon_emoji": ">�",
        "example_use_case": "Creating study guides for programming documentation or technical papers",
        "sections": ["Core Concepts", "Relationships", "Code Examples", "Use Cases", "Best Practices"]
    },
    {
        "id": "exam-prep-sprint",
        "name": "Exam Prep Sprint",
        "description": "Generate focused exam preparation materials with practice questions, key formulas, and critical review points.",
        "icon_emoji": "<�",
        "example_use_case": "Last-minute review guide for final exams with practice problems",
        "sections": ["Must-Know Topics", "Key Formulas", "Practice Questions", "Common Mistakes", "Quick Review"]
    }
]

# ============================================================================
# QDRANT SETUP - Initialize Template Embeddings
# ============================================================================

def initialize_template_embeddings():
    """
    Initialize Qdrant collection and create embeddings for all templates.
    This runs once at startup for optimal performance.
    """
    if not qdrant_client or not mistral_client:
        logger.warning("⚠️  Cannot initialize embeddings - clients not available")
        return False

    try:
        collection_name = "learning_templates"

        logger.info("🔧 Creating Qdrant collection for templates...")

        # Create collection (1024 dimensions for mistral-embed)
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )

        logger.info(f"📚 Creating embeddings for {len(STUDY_TEMPLATES)} templates...")

        # Prepare all texts to embed
        texts_to_embed = []
        for template in STUDY_TEMPLATES:
            embed_text = f"{template['name']}: {template['description']}. Best for {template['example_use_case']}"
            texts_to_embed.append(embed_text)

        # Get embeddings in a single batch call (more efficient and less rate limiting)
        logger.info("  Calling Mistral embeddings API (batch mode)...")
        try:
            embedding_response = mistral_client.embeddings.create(
                model="mistral-embed",
                inputs=texts_to_embed
            )
        except Exception as e:
            logger.warning(f"  Batch embedding failed, trying with delay: {e}")
            time.sleep(2)
            embedding_response = mistral_client.embeddings.create(
                model="mistral-embed",
                inputs=texts_to_embed
            )

        # Create points for Qdrant
        points = []
        for idx, (template, embedding_data) in enumerate(zip(STUDY_TEMPLATES, embedding_response.data)):
            vector = embedding_data.embedding

            point = PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "template_id": template["id"],
                    "template_name": template["name"],
                    "description": template["description"],
                    "sections": template["sections"],
                    "example_use_case": template["example_use_case"],
                    "icon_emoji": template["icon_emoji"]
                }
            )
            points.append(point)
            logger.info(f"  ✓ Embedded template {idx+1}/{len(STUDY_TEMPLATES)}: {template['name']}")

        # Upload all points to Qdrant
        qdrant_client.upsert(
            collection_name=collection_name,
            points=points
        )

        logger.info(f"✅ Successfully initialized {len(points)} template embeddings in Qdrant")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to initialize template embeddings: {e}", exc_info=True)
        return False

# Initialize embeddings at startup
initialize_template_embeddings()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Serve the main landing page"""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "success",
        "message": "StudyForge API is running",
        "version": "1.0.0"
    }), 200


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """
    GET /api/templates
    Returns the list of available study guide templates

    Response:
        200: List of templates with metadata
    """
    return jsonify({
        "status": "success",
        "templates": STUDY_TEMPLATES,
        "count": len(STUDY_TEMPLATES)
    }), 200


@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    """
    POST /api/analyze
    Analyzes user-provided content (text, PDF, notes) to extract key information

    Expected JSON body:
        {
            "content": "string (user's study material)",
            "content_type": "text|pdf|url"
        }

    Returns:
        200: Analysis results with topic, concepts, content type, etc.
        400: Missing content
        500: Analysis failed
    """
    try:
        data = request.get_json()

        # Validate input
        if not data or 'content' not in data:
            logger.warning("Analysis request missing 'content' field")
            return jsonify({
                "status": "error",
                "message": "Missing 'content' in request body"
            }), 400

        content = data.get('content')
        content_type = data.get('content_type', 'text')

        logger.info(f"📊 Analyzing content: {len(content)} characters")

        # Check if Mistral client is available
        if not mistral_client:
            logger.error("Mistral client not initialized")
            return jsonify({
                "status": "error",
                "message": "Mistral AI service not available. Check API key configuration."
            }), 500

        # Create the analysis prompt
        analysis_prompt = f"""You are an educational content analyzer. Analyze the following text and return ONLY valid JSON (no markdown, no explanations) with this structure:
{{
  "topic": "A concise title for this content",
  "key_concepts": ["Concept 1", "Concept 2", "Concept 3"],
  "content_type": "lecture|case_study|textbook|notes|article",
  "difficulty_level": "beginner|intermediate|advanced",
  "estimated_study_time": "X minutes"
}}

Text to analyze:
{content}"""

        logger.info("🤖 Calling Mistral API for content analysis...")

        # Call Mistral API
        response = mistral_client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ]
        )

        # Extract the response content
        mistral_response = response.choices[0].message.content
        logger.info(f"✅ Mistral response received: {len(mistral_response)} characters")
        logger.debug(f"Raw Mistral response: {mistral_response}")

        # Parse JSON response
        try:
            # Remove potential markdown code blocks
            clean_response = mistral_response.strip()
            if clean_response.startswith('```'):
                # Remove markdown code block markers
                clean_response = clean_response.split('```')[1]
                if clean_response.startswith('json'):
                    clean_response = clean_response[4:]
                clean_response = clean_response.strip()

            analysis_result = json.loads(clean_response)
            logger.info(f"✅ Analysis successful - Topic: {analysis_result.get('topic', 'N/A')}")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Mistral response as JSON: {e}")
            logger.error(f"Response was: {mistral_response}")
            return jsonify({
                "status": "error",
                "message": "Failed to parse AI response. Please try again."
            }), 500

        # Return successful analysis
        return jsonify({
            "status": "success",
            "message": "Content analyzed successfully",
            "analysis": {
                "content_length": len(content),
                "content_type": content_type,
                "topic": analysis_result.get("topic", "Unknown"),
                "key_concepts": analysis_result.get("key_concepts", []),
                "detected_content_type": analysis_result.get("content_type", "unknown"),
                "difficulty_level": analysis_result.get("difficulty_level", "intermediate"),
                "estimated_study_time": analysis_result.get("estimated_study_time", "N/A"),
                "analysis_id": f"analysis_{hash(content) % 1000000}"  # Simple ID generation
            }
        }), 200

    except Exception as e:
        logger.error(f"❌ Error during content analysis: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": f"Analysis failed: {str(e)}"
        }), 500


@app.route('/api/match-template', methods=['POST'])
def match_template():
    """
    POST /api/match-template
    Matches analyzed content to the most appropriate study guide template

    Expected JSON body:
        {
            "analysis": {
                "topic": "...",
                "detected_content_type": "...",
                ...
            },
            "selected_template_id": "optional - if user manually selected"
        }

    Returns:
        200: Matched template with confidence score
        400: Invalid request
        500: Matching failed
    """
    try:
        data = request.get_json()

        # Validate input
        if not data:
            logger.warning("Template matching request missing data")
            return jsonify({
                "status": "error",
                "message": "Request body required"
            }), 400

        selected_template_id = data.get('selected_template_id')
        analysis = data.get('analysis', {})

        # If user manually selected a template, return it immediately
        if selected_template_id:
            logger.info(f"📌 User manually selected template: {selected_template_id}")
            matched_template = next(
                (t for t in STUDY_TEMPLATES if t['id'] == selected_template_id),
                None
            )

            if not matched_template:
                return jsonify({
                    "status": "error",
                    "message": f"Template '{selected_template_id}' not found"
                }), 404

            return jsonify({
                "status": "success",
                "matched_template": matched_template,
                "match_score": 1.0,
                "method": "user_selected"
            }), 200

        # Otherwise, use Qdrant vector matching
        logger.info("🔍 Using AI to match template from analysis...")

        if not qdrant_client or not mistral_client:
            logger.error("Qdrant or Mistral client not available")
            return jsonify({
                "status": "error",
                "message": "AI matching service not available"
            }), 500

        # Create search query from analysis
        content_type = analysis.get('detected_content_type', 'unknown')
        topic = analysis.get('topic', '')
        difficulty = analysis.get('difficulty_level', '')

        query_text = f"{content_type}: {topic}. Difficulty: {difficulty}"
        logger.info(f"  Query: {query_text}")

        # Get embedding for the query
        query_embedding_response = mistral_client.embeddings.create(
            model="mistral-embed",
            inputs=[query_text]
        )
        query_vector = query_embedding_response.data[0].embedding

        # Search in Qdrant for top 2 matches
        search_results = qdrant_client.search(
            collection_name="learning_templates",
            query_vector=query_vector,
            limit=2
        )

        if not search_results:
            logger.warning("No matching templates found, defaulting to first template")
            matched_template = STUDY_TEMPLATES[0]
            match_score = 0.5
        else:
            # Get the best match
            best_match = search_results[0]
            match_score = best_match.score

            logger.info(f"✅ Best match: {best_match.payload['template_name']} (score: {match_score:.3f})")

            # Find the full template data
            matched_template = next(
                (t for t in STUDY_TEMPLATES if t['id'] == best_match.payload['template_id']),
                STUDY_TEMPLATES[0]
            )

            # Log alternative suggestion
            if len(search_results) > 1:
                alt_match = search_results[1]
                logger.info(f"  Alternative: {alt_match.payload['template_name']} (score: {alt_match.score:.3f})")

        return jsonify({
            "status": "success",
            "matched_template": matched_template,
            "match_score": float(match_score),
            "method": "ai_matched"
        }), 200

    except Exception as e:
        logger.error(f"❌ Error during template matching: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": f"Template matching failed: {str(e)}"
        }), 500


@app.route('/api/generate-guide', methods=['POST'])
def generate_study_guide():
    """
    POST /api/generate-guide
    Generates the final study guide using the matched template and analyzed content

    Expected JSON body:
        {
            "analysis_id": "string",
            "template_id": "string",
            "customization_options": {
                "length": "short|medium|long",
                "include_examples": boolean,
                "include_questions": boolean
            }
        }

    TODO: Implement study guide generation
    - Retrieve content analysis from Qdrant
    - Use Mistral AI to generate structured content
    - Format according to template sections
    - Apply customization options
    """
    try:
        data = request.get_json()

        # Validate input
        if not data or 'template_id' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required fields: template_id"
            }), 400

        template_id = data.get('template_id')
        analysis_id = data.get('analysis_id')
        customization = data.get('customization_options', {})

        # Find the template
        template = next((t for t in STUDY_TEMPLATES if t['id'] == template_id), None)
        if not template:
            return jsonify({
                "status": "error",
                "message": f"Template '{template_id}' not found"
            }), 404

        # TODO: Implement study guide generation
        # - Retrieve analyzed content from Qdrant using analysis_id
        # - Use Mistral AI to generate content for each template section
        # - Apply customization options (length, examples, questions)
        # - Format and structure the final output

        # Placeholder response
        return jsonify({
            "status": "success",
            "message": "Study guide generated successfully",
            "study_guide": {
                "template": template['name'],
                "sections": {},  # TODO: Populate with generated content
                "metadata": {
                    "generated_at": None,  # TODO: Add timestamp
                    "word_count": None,
                    "customization_applied": customization
                }
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Check if required environment variables are set
    if not app.config['MISTRAL_API_KEY']:
        print("�  WARNING: MISTRAL_API_KEY not set in environment variables")
    if not app.config['QDRANT_URL']:
        print("�  WARNING: QDRANT_URL not set in environment variables")
    if not app.config['QDRANT_API_KEY']:
        print("�  WARNING: QDRANT_API_KEY not set in environment variables")

    print("=� Starting StudyForge API...")
    print(f"=� Loaded {len(STUDY_TEMPLATES)} study guide templates")

    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=os.getenv('FLASK_DEBUG', 'True') == 'True'
    )
