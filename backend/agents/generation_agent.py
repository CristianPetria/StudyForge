"""
Study Guide Generation Agent
Responsible for generating the final study guide using template and analyzed content
"""

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
            dict: Generated study guide or error
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
            length_pref = customization.get('length', 'medium')
            include_examples = customization.get('include_examples', True)
            include_questions = customization.get('include_questions', True)
            
            sections_prompt = "\n".join([f"- {section}" for section in template['sections']])
            
            generation_prompt = f"""Create a study guide for the following topic using the template sections.

Topic: {topic}
Length preference: {length_pref}
Include Examples: {include_examples}
Include Practice Questions: {include_questions}

Template Sections:
{sections_prompt}

Content to study:
{content_to_study}

Generate a comprehensive study guide with all the template sections filled in. 
Return the response as structured text with clear section headers."""
            
            # Call Mistral API
            logger.info("🤖 Calling Mistral API for guide generation...")
            response = self.mistral_client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": generation_prompt}]
            )
            
            generated_content = response.choices[0].message.content
            logger.info(f"✅ Study guide generated: {len(generated_content)} characters")
            
            return {
                "status": "success",
                "study_guide": {
                    "template": template['name'],
                    "topic": topic,
                    "content": generated_content,
                    "metadata": {
                        "customization_applied": customization,
                        "word_count": len(generated_content.split()),
                        "sections": template['sections']
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
