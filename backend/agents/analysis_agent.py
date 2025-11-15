"""
Analysis Agent
Responsible for analyzing user-provided content and extracting key information
"""

import json
import logging
from backend.utils.clients import get_mistral_client
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class AnalysisAgent:
    """Agent for analyzing study content"""
    
    def __init__(self):
        self.mistral_client = get_mistral_client()
        if not self.mistral_client:
            logger.warning("Analysis Agent: Mistral client not available")
    
    def analyze_content(self, content, content_type='text'):
        """
        Analyze user-provided content
        
        Args:
            content (str): The content to analyze
            content_type (str): Type of content (text, pdf, url)
        
        Returns:
            dict: Analysis results or error
        """
        try:
            if not self.mistral_client:
                return {
                    "status": "error",
                    "message": "Mistral AI service not available"
                }
            
            logger.info(f"📊 Analyzing content: {len(content)} characters")
            
            # Create analysis prompt
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
            
            # Call Mistral API
            logger.info("🤖 Calling Mistral API...")
            response = self.mistral_client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": analysis_prompt}]
            )
            
            mistral_response = response.choices[0].message.content
            logger.info(f"✅ Mistral response received: {len(mistral_response)} characters")
            
            # Parse JSON response
            clean_response = mistral_response.strip()
            if clean_response.startswith('```'):
                clean_response = clean_response.split('```')[1]
                if clean_response.startswith('json'):
                    clean_response = clean_response[4:]
                clean_response = clean_response.strip()
            
            analysis_result = json.loads(clean_response)
            logger.info(f"✅ Analysis successful - Topic: {analysis_result.get('topic', 'N/A')}")
            
            return {
                "status": "success",
                "analysis": {
                    "content_length": len(content),
                    "content_type": content_type,
                    "topic": analysis_result.get("topic", "Unknown"),
                    "key_concepts": analysis_result.get("key_concepts", []),
                    "detected_content_type": analysis_result.get("content_type", "unknown"),
                    "difficulty_level": analysis_result.get("difficulty_level", "intermediate"),
                    "estimated_study_time": analysis_result.get("estimated_study_time", "N/A"),
                    "analysis_id": f"analysis_{hash(content) % 1000000}"
                }
            }
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Mistral response as JSON: {e}")
            return {
                "status": "error",
                "message": "Failed to parse AI response"
            }
        
        except Exception as e:
            logger.error(f"❌ Error during analysis: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Analysis failed: {str(e)}"
            }


# Global agent instance
_analysis_agent = None


def get_analysis_agent():
    """Get or create the Analysis Agent"""
    global _analysis_agent
    if _analysis_agent is None:
        _analysis_agent = AnalysisAgent()
    return _analysis_agent
