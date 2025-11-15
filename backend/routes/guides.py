"""
Study Guide API routes
Endpoints for analyzing content, matching templates, and generating guides
"""

import uuid
from flask import Blueprint, request, jsonify, render_template
from backend.agents.coordinator import get_coordinator
from backend.agents.analysis_agent import get_analysis_agent
from backend.agents.template_matching_agent import get_template_matching_agent
from backend.agents.generation_agent import get_generation_agent
from backend.utils.logger import get_logger

logger = get_logger(__name__)

guides_bp = Blueprint('guides', __name__, url_prefix='/api')

# In-memory storage for generated guides (in production, use a database)
_generated_guides = {}


@guides_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    POST /api/analyze
    Analyzes user-provided content and extracts key information
    
    Request body:
        {
            "content": "string",
            "content_type": "text|pdf|url" (optional)
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            logger.warning("Analyze: Missing 'content' field")
            return jsonify({
                "status": "error",
                "message": "Missing 'content' in request body"
            }), 400
        
        content = data['content']
        content_type = data.get('content_type', 'text')
        
        agent = get_analysis_agent()
        result = agent.analyze_content(content, content_type)
        
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "message": "Content analyzed successfully",
                "analysis": result['analysis']
            }), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@guides_bp.route('/match-template', methods=['POST'])
def match_template():
    """
    POST /api/match-template
    Matches analyzed content to the most appropriate template
    
    Request body:
        {
            "analysis": {...},
            "selected_template_id": "optional"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("Match-template: No request body")
            return jsonify({
                "status": "error",
                "message": "Request body required"
            }), 400
        
        analysis = data.get('analysis', {})
        selected_template_id = data.get('selected_template_id')
        
        agent = get_template_matching_agent()
        result = agent.match_template(analysis, selected_template_id)
        
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "matched_template": result['matched_template'],
                "match_score": result['match_score'],
                "method": result['method']
            }), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in match_template endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@guides_bp.route('/generate-guide', methods=['POST'])
def generate_guide():
    """
    POST /api/generate-guide
    Generates the final study guide
    
    Request body:
        {
            "template_id": "string",
            "analysis": {...},
            "customization_options": {
                "length": "short|medium|long",
                "include_examples": boolean,
                "include_questions": boolean
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'template_id' not in data:
            logger.warning("Generate-guide: Missing 'template_id'")
            return jsonify({
                "status": "error",
                "message": "Missing required field: template_id"
            }), 400
        
        template_id = data['template_id']
        analysis = data.get('analysis', {})
        customization = data.get('customization_options', {})
        
        agent = get_generation_agent()
        result = agent.generate_guide(template_id, analysis, customization)
        
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "study_guide": result['study_guide']
            }), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in generate_guide endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@guides_bp.route('/complete-workflow', methods=['POST'])
def complete_workflow():
    """
    POST /api/complete-workflow
    Orchestrates the complete workflow: analyze -> match -> generate

    Request body:
        {
            "content": "string",
            "content_type": "text|pdf|url",
            "template_id": "optional - if not provided, AI will match",
            "customization_options": {...}
        }

    Returns:
        {
            "status": "success",
            "guide_id": "uuid",
            "guide_url": "/api/guide/{guide_id}",
            "workflow": {...}
        }
    """
    try:
        data = request.get_json()

        if not data or 'content' not in data:
            logger.warning("Complete-workflow: Missing 'content'")
            return jsonify({
                "status": "error",
                "message": "Missing 'content' in request body"
            }), 400

        content = data['content']
        content_type = data.get('content_type', 'text')
        template_id = data.get('template_id')
        customization = data.get('customization_options', {})

        coordinator = get_coordinator()
        result = coordinator.process_study_request(
            content,
            content_type,
            template_id,
            customization
        )

        if result['status'] == 'success':
            # Generate a unique ID for this guide
            guide_id = str(uuid.uuid4())

            # Extract the study guide data from the workflow result
            study_guide = result['workflow'].get('study_guide', {})

            # Store the guide
            _generated_guides[guide_id] = {
                "id": guide_id,
                "template": study_guide.get('template', 'Unknown'),
                "template_id": study_guide.get('template_id'),
                "data": study_guide.get('data', {}),
                "audio_url": None,  # TODO: Implement audio generation
                "metadata": study_guide.get('metadata', {}),
                "created_at": None  # TODO: Add timestamp
            }

            logger.info(f"✅ Guide stored with ID: {guide_id}")

            return jsonify({
                "status": "success",
                "message": "Study guide generated successfully",
                "guide_id": guide_id,
                "guide_url": f"/api/guide/{guide_id}",
                "workflow": result['workflow']
            }), 200
        else:
            return jsonify(result), 500

    except Exception as e:
        logger.error(f"Error in complete_workflow endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@guides_bp.route('/guide/<guide_id>/json', methods=['GET'])
def view_guide_json(guide_id):
    """
    GET /api/guide/<guide_id>/json
    Returns the raw guide data as JSON for debugging
    """
    try:
        if guide_id in _generated_guides:
            return jsonify(_generated_guides[guide_id]), 200
        else:
            return jsonify({"status": "error", "message": "Guide not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@guides_bp.route('/guide/<guide_id>/edit', methods=['POST'])
def edit_guide(guide_id):
    """
    POST /api/guide/<guide_id>/edit
    Edit a specific section of the guide using Mistral AI

    Request body:
        {
            "section_path": "sections[0].key_concepts[0].explanation",
            "instruction": "Make this more concise",
            "current_content": "..."
        }
    """
    try:
        if guide_id not in _generated_guides:
            return jsonify({
                "status": "error",
                "message": "Guide not found"
            }), 404

        data = request.get_json()
        instruction = data.get('instruction', '')
        current_content = data.get('current_content', '')
        section_path = data.get('section_path', '')

        if not instruction or not current_content:
            return jsonify({
                "status": "error",
                "message": "Missing required fields: instruction and current_content"
            }), 400

        logger.info(f"🎨 Editing guide {guide_id}, instruction: {instruction[:50]}...")

        # Use Mistral to edit the content
        from backend.utils.clients import get_mistral_client
        mistral_client = get_mistral_client()

        if not mistral_client:
            return jsonify({
                "status": "error",
                "message": "Mistral AI service not available"
            }), 503

        edit_prompt = f"""You are an expert educational content editor. Edit the following content based on the user's instruction.

USER INSTRUCTION: {instruction}

CURRENT CONTENT:
{current_content}

Return ONLY the edited content, without any explanations or markdown formatting. Keep the same style and educational tone."""

        response = mistral_client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": edit_prompt}]
        )

        edited_content = response.choices[0].message.content.strip()
        logger.info(f"✅ Content edited successfully")

        # Update the guide in storage
        guide = _generated_guides[guide_id]
        # TODO: Apply the edit to the specific section_path

        return jsonify({
            "status": "success",
            "edited_content": edited_content,
            "original_content": current_content
        }), 200

    except Exception as e:
        logger.error(f"Error editing guide: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@guides_bp.route('/guide/<guide_id>', methods=['GET'])
def view_guide(guide_id):
    """
    GET /api/guide/<guide_id>
    Renders the study guide HTML template with guide data

    Retrieves stored guide or serves test data for demo purposes
    """
    try:
        logger.info(f"Viewing guide: {guide_id}")

        # Check if this is a real generated guide
        if guide_id in _generated_guides:
            guide = _generated_guides[guide_id]
            logger.info(f"✅ Found generated guide: {guide_id}")

            # Debug: Log the structure to see what we have
            logger.info(f"Guide structure: template={guide.get('template')}, data keys={list(guide.get('data', {}).keys())}")

            return render_template('guide.html', guide=guide)

        # Otherwise, serve test data for demo/testing
        logger.info(f"⚠️ Guide {guide_id} not found, serving test data")
        test_guide = {
            "id": guide_id,
            "template": "Academic Concept",
            "audio_url": None,  # No audio for now
            "data": {
                "title": "Understanding Machine Learning Fundamentals",
                "subtitle": "A comprehensive guide to the basics of ML",
                "sections": [
                    {
                        # Section 0: Overview
                        "title": "Overview",
                        "executive_summary": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. This guide explores the fundamental concepts, types of learning, and key algorithms that form the foundation of modern ML systems.",
                        "key_concepts": [
                            {
                                "term": "Supervised Learning",
                                "definition": "A type of machine learning where the algorithm learns from labeled training data.",
                                "explanation": "In supervised learning, we provide the model with input-output pairs, and it learns to map inputs to outputs. Think of it as learning with a teacher who provides the correct answers.",
                                "importance": "Supervised learning is the most common type of ML and powers applications like spam detection, image recognition, and recommendation systems."
                            },
                            {
                                "term": "Training Data",
                                "definition": "The dataset used to teach a machine learning model to make predictions.",
                                "explanation": "Training data consists of examples that the model uses to identify patterns and relationships. The quality and quantity of training data directly impacts model performance.",
                                "importance": "High-quality training data is essential for building accurate models. The principle 'garbage in, garbage out' is especially true in ML."
                            },
                            {
                                "term": "Model",
                                "definition": "A mathematical representation of a real-world process, learned from data.",
                                "explanation": "A model is the output of the ML training process. It encapsulates the patterns learned from the training data and can make predictions on new, unseen data.",
                                "importance": "The model is what you deploy in production to solve real-world problems. Understanding model types helps you choose the right approach for your task."
                            }
                        ]
                    },
                    {
                        # Section 1: Deep Dive
                        "title": "Deep Dive",
                        "introduction": "Let's explore the technical details of machine learning, including the mathematical foundations, different types of algorithms, and how to evaluate model performance.",
                        "subsections": [
                            {
                                "heading": "Types of Machine Learning",
                                "content": "Machine learning can be categorized into three main types: supervised learning (learning from labeled data), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through trial and error with rewards). Each type is suited for different kinds of problems and has its own set of algorithms and techniques."
                            },
                            {
                                "heading": "The Learning Process",
                                "content": "Machine learning follows a systematic process: (1) Data Collection - gathering relevant data, (2) Data Preprocessing - cleaning and preparing data, (3) Model Selection - choosing the right algorithm, (4) Training - fitting the model to data, (5) Evaluation - testing performance, and (6) Deployment - putting the model into production. Understanding this workflow is crucial for successful ML projects."
                            }
                        ],
                        "formulas": [
                            {
                                "name": "Mean Squared Error (MSE)",
                                "formula": "MSE = (1/n) * Σ(y_actual - y_predicted)²",
                                "variables": {
                                    "n": "Number of observations",
                                    "y_actual": "Actual value from the dataset",
                                    "y_predicted": "Value predicted by the model"
                                },
                                "example": "If you have 3 predictions [2, 4, 6] and actual values [1, 5, 5], MSE = (1/3) * [(1-2)² + (5-4)² + (5-6)²] = (1/3) * [1 + 1 + 1] = 1.0",
                                "when_to_use": "Use MSE when you want to penalize larger errors more heavily. It's commonly used in regression problems."
                            }
                        ],
                        "examples": [
                            {
                                "title": "Email Spam Detection",
                                "scenario": "An email service wants to automatically filter spam messages from legitimate emails.",
                                "analysis": "This is a supervised learning classification problem. We can train a model using historical emails labeled as 'spam' or 'not spam'. Features might include word frequencies, sender information, and email metadata. A Naive Bayes or Logistic Regression classifier would be appropriate.",
                                "key_takeaway": "Supervised learning excels at classification tasks when you have labeled historical data showing the correct categorization."
                            }
                        ],
                        "important_notes": [
                            "Always split your data into training, validation, and test sets to avoid overfitting and get accurate performance metrics.",
                            "Feature engineering (creating meaningful input variables) is often more important than choosing the fanciest algorithm.",
                            "Start simple! A basic model that works is better than a complex model that doesn't. You can always iterate and improve."
                        ]
                    },
                    {
                        # Section 2: Applications
                        "title": "Real-World Applications & Exam Tips",
                        "real_world_uses": [
                            {
                                "context": "Healthcare - Disease Diagnosis",
                                "application": "ML models analyze medical images (X-rays, MRIs) to detect diseases like cancer, often matching or exceeding human expert performance.",
                                "impact": "Faster diagnosis, reduced healthcare costs, and improved patient outcomes through early detection."
                            },
                            {
                                "context": "Finance - Fraud Detection",
                                "application": "Banks use ML to identify fraudulent transactions by detecting unusual patterns in spending behavior in real-time.",
                                "impact": "Prevents billions in fraud losses annually and protects customer accounts from unauthorized access."
                            },
                            {
                                "context": "Transportation - Autonomous Vehicles",
                                "application": "Self-driving cars use ML for object detection, path planning, and decision-making based on sensor data.",
                                "impact": "Potential to reduce traffic accidents, improve transportation efficiency, and provide mobility to those unable to drive."
                            }
                        ],
                        "exam_tips": [
                            "Understand the difference between supervised, unsupervised, and reinforcement learning - this is often tested.",
                            "Be able to explain overfitting and underfitting with examples. Know techniques to address each.",
                            "Memorize common evaluation metrics (accuracy, precision, recall, F1-score) and when to use each.",
                            "Practice explaining how specific algorithms work (e.g., linear regression, decision trees) in plain English.",
                            "Know the bias-variance tradeoff and how it relates to model complexity."
                        ]
                    }
                ],
                "flashcards": [
                    {
                        "question": "What is the difference between supervised and unsupervised learning?",
                        "answer": "Supervised learning uses labeled data (input-output pairs) to train models, while unsupervised learning finds patterns in unlabeled data without predefined categories."
                    },
                    {
                        "question": "What is overfitting?",
                        "answer": "Overfitting occurs when a model learns the training data too well, including noise and outliers, resulting in poor performance on new, unseen data."
                    },
                    {
                        "question": "What is the purpose of a validation set?",
                        "answer": "A validation set is used to tune hyperparameters and make decisions during model development, keeping the test set completely separate for final evaluation."
                    },
                    {
                        "question": "What does the term 'feature' mean in machine learning?",
                        "answer": "A feature is an individual measurable property or characteristic of the data used as input to train a machine learning model."
                    },
                    {
                        "question": "What is gradient descent?",
                        "answer": "Gradient descent is an optimization algorithm used to minimize the loss function by iteratively adjusting model parameters in the direction of steepest descent."
                    },
                    {
                        "question": "What is cross-validation?",
                        "answer": "Cross-validation is a technique where the dataset is split into multiple subsets, and the model is trained and validated multiple times to get a more reliable performance estimate."
                    }
                ],
                "quiz": [
                    {
                        "question": "Which type of machine learning would you use for categorizing emails as spam or not spam?",
                        "options": [
                            "Supervised Learning",
                            "Unsupervised Learning",
                            "Reinforcement Learning",
                            "Semi-supervised Learning"
                        ],
                        "correct_index": 0,
                        "explanation": "Email spam detection is a supervised learning task because we have labeled examples of spam and non-spam emails that we can use to train the model."
                    },
                    {
                        "question": "What is the main risk of using your test set multiple times during model development?",
                        "options": [
                            "The model will take longer to train",
                            "You might overfit to the test set and get overly optimistic performance estimates",
                            "The model will become less accurate",
                            "It will use more memory"
                        ],
                        "correct_index": 1,
                        "explanation": "Using the test set multiple times can lead to overfitting to the test set, where you inadvertently tune your model to perform well on that specific data, leading to unreliable performance estimates."
                    },
                    {
                        "question": "Which metric is most appropriate for evaluating a model on an imbalanced dataset?",
                        "options": [
                            "Accuracy",
                            "Mean Squared Error",
                            "F1-Score",
                            "R-squared"
                        ],
                        "correct_index": 2,
                        "explanation": "F1-Score is better for imbalanced datasets because it considers both precision and recall, whereas accuracy can be misleading when one class is much more common than others."
                    }
                ]
            }
        }

        return render_template('guide.html', guide=test_guide)

    except Exception as e:
        logger.error(f"Error in view_guide endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
