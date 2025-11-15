"""
Study Guide Generation Agent
Responsible for generating the final study guide using template and analyzed content
"""

import json
from backend.utils.clients import get_mistral_client
from backend.utils.logger import get_logger
from backend.config import STUDY_TEMPLATES

logger = get_logger(__name__)


class GenerationAgent:
    """Agent for generating study guides"""
    
    def __init__(self):
        self.mistral_client = get_mistral_client()
        if not self.mistral_client:
            logger.warning("Generation Agent: Mistral client not available")
    
    def generate_guide(self, template_id, analysis=None, customization=None):
        """
        Generate a study guide for the given template and analysis

        Args:
            template_id (str): ID of the template to use
            analysis (dict): Content analysis results
            customization (dict): Customization options (length, include_examples, include_questions)

        Returns:
            dict: Generated study guide with structured JSON matching guide.html template
        """
        try:
            if not self.mistral_client:
                return {
                    "status": "error",
                    "message": "Mistral AI service not available"
                }

            # Find the template
            template = next(
                (t for t in STUDY_TEMPLATES if t['id'] == template_id),
                None
            )

            if not template:
                return {
                    "status": "error",
                    "message": f"Template '{template_id}' not found"
                }

            analysis = analysis or {}
            customization = customization or {}

            logger.info(f"📝 Generating study guide: {template['name']}")

            # Build the generation prompt
            content_to_study = analysis.get('content', 'No content provided')
            topic = analysis.get('topic', 'General Topic')
            subject = analysis.get('subject', 'General')
            difficulty = analysis.get('difficulty', 'intermediate')
            length_pref = customization.get('length', 'medium')
            include_examples = customization.get('include_examples', True)
            include_questions = customization.get('include_questions', True)

            generation_prompt = f"""You are an expert educational content creator. Generate a comprehensive study guide in EXACT JSON format.

TOPIC: {topic}
SUBJECT: {subject}
DIFFICULTY LEVEL: {difficulty}
LENGTH PREFERENCE: {length_pref}

CONTENT TO STUDY:
{content_to_study}

YOU MUST RETURN ONLY VALID JSON (no markdown, no code blocks, no explanations) with this EXACT structure:

{{
  "title": "Main title for the study guide",
  "subtitle": "Brief subtitle describing the guide",
  "subject": "{subject}",
  "difficulty_level": "{difficulty}",
  "study_time": "Estimated study time (e.g., '2-3 hours')",
  "sections": [
    {{
      "title": "Overview",
      "executive_summary": "A 2-3 sentence summary of the entire topic",
      "key_concepts": [
        {{
          "term": "Concept name",
          "definition": "Brief definition",
          "explanation": "Detailed explanation in 2-3 sentences",
          "importance": "Why this concept matters"
        }}
      ]
    }},
    {{
      "title": "Deep Dive",
      "introduction": "Introduction to the detailed content",
      "subsections": [
        {{
          "heading": "Subsection title",
          "content": "Detailed explanation of this subsection (2-3 paragraphs)"
        }}
      ],
      "formulas": [
        {{
          "name": "Formula name",
          "formula": "The formula itself",
          "variables": {{
            "var1": "Description of variable 1",
            "var2": "Description of variable 2"
          }},
          "example": "A worked example showing the formula in use",
          "when_to_use": "When and why to use this formula"
        }}
      ],
      "examples": [
        {{
          "title": "Example title",
          "scenario": "The scenario or problem",
          "analysis": "Step-by-step analysis",
          "key_takeaway": "Main lesson from this example"
        }}
      ],
      "important_notes": [
        "Important note 1",
        "Important note 2"
      ]
    }},
    {{
      "title": "Real-World Applications & Exam Tips",
      "real_world_uses": [
        {{
          "context": "Industry or field",
          "application": "How it's used in practice",
          "impact": "The real-world impact or benefit"
        }}
      ],
      "exam_tips": [
        "Exam tip 1",
        "Exam tip 2",
        "Exam tip 3"
      ]
    }}
  ],
  "flashcards": [
    {{
      "question": "Question text",
      "answer": "Answer text"
    }}
  ],
  "quiz": [
    {{
      "question": "Quiz question text",
      "options": [
        "Option 1",
        "Option 2",
        "Option 3",
        "Option 4"
      ],
      "correct_index": 0,
      "explanation": "Explanation of why the answer is correct"
    }}
  ]
}}

REQUIREMENTS:
1. Generate {"at least 3-5 key concepts" if length_pref != "short" else "2-3 key concepts"} in the Overview section
2. Create {"2-3 subsections" if length_pref != "short" else "1-2 subsections"} in Deep Dive
3. Include {("formulas if applicable" if include_examples else "no formulas")}
4. Add {"2-3 examples" if include_examples else "1 example"} in Deep Dive
5. Generate {"at least 6-10 flashcards" if include_questions else "3-5 flashcards"}
6. Create {"5-8 quiz questions" if include_questions else "3 quiz questions"}
7. Each quiz question must have exactly 4 options
8. Provide 3-5 real-world applications
9. Include 5-7 exam tips

CRITICAL: Return ONLY the JSON object. No markdown formatting, no ```json```, no explanations before or after."""

            # Call Mistral API
            logger.info("🤖 Calling Mistral API for guide generation...")
            response = self.mistral_client.chat.complete(
                model="mistral-small-latest",  # Using smaller model to avoid rate limits
                messages=[{"role": "user", "content": generation_prompt}],
                response_format={"type": "json_object"}
            )

            generated_content = response.choices[0].message.content
            logger.info(f"✅ Study guide generated: {len(generated_content)} characters")

            # Parse the JSON response
            try:
                study_guide_data = json.loads(generated_content)
                logger.info(f"✅ JSON parsed successfully")
            except json.JSONDecodeError as je:
                logger.error(f"❌ Failed to parse JSON: {str(je)}")
                logger.error(f"Response was: {generated_content[:500]}...")
                return {
                    "status": "error",
                    "message": f"Failed to parse AI response as JSON: {str(je)}"
                }

            return {
                "status": "success",
                "study_guide": {
                    "template": template['name'],
                    "template_id": template_id,
                    "data": study_guide_data,
                    "metadata": {
                        "customization_applied": customization,
                        "word_count": len(generated_content.split())
                    }
                }
            }

        except Exception as e:
            logger.error(f"❌ Error during guide generation: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Guide generation failed: {str(e)}"
            }


# Global agent instance
_generation_agent = None


def get_generation_agent():
    """Get or create the Generation Agent"""
    global _generation_agent
    if _generation_agent is None:
        _generation_agent = GenerationAgent()
    return _generation_agent
