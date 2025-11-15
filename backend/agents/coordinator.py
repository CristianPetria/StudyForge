"""
Agent coordinator for orchestrating different AI agents
Manages the flow between analysis, template matching, and guide generation
"""

from backend.agents.analysis_agent import get_analysis_agent
from backend.agents.template_matching_agent import get_template_matching_agent
from backend.agents.generation_agent import get_generation_agent
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class AgentCoordinator:
    """Orchestrates communication between different agents"""
    
    def __init__(self):
        self.analysis_agent = get_analysis_agent()
        self.template_agent = get_template_matching_agent()
        self.generation_agent = get_generation_agent()
    
    def process_study_request(self, content, content_type='text', 
                            template_id=None, customization=None):
        """
        Complete end-to-end study guide generation workflow
        
        Args:
            content (str): User's content to analyze
            content_type (str): Type of content
            template_id (str): Optional pre-selected template
            customization (dict): Customization options
        
        Returns:
            dict: Complete workflow result
        """
        logger.info("🚀 Starting complete study guide workflow")
        
        # Step 1: Analyze content
        logger.info("Step 1/3: Analyzing content...")
        analysis_result = self.analysis_agent.analyze_content(content, content_type)
        
        if analysis_result['status'] != 'success':
            return analysis_result
        
        analysis = analysis_result['analysis']
        logger.info(f"✅ Content analyzed - Topic: {analysis['topic']}")
        
        # Step 2: Match template
        logger.info("Step 2/3: Matching template...")
        template_result = self.template_agent.match_template(analysis, template_id)
        
        if template_result['status'] != 'success':
            return template_result
        
        matched_template = template_result['matched_template']
        logger.info(f"✅ Template matched: {matched_template['name']}")
        
        # Step 3: Generate study guide
        logger.info("Step 3/3: Generating study guide...")
        
        # Prepare analysis dict with content for generation
        analysis_with_content = {**analysis, 'content': content}
        generation_result = self.generation_agent.generate_guide(
            matched_template['id'],
            analysis_with_content,
            customization
        )
        
        if generation_result['status'] != 'success':
            return generation_result
        
        logger.info("✅ Study guide generated successfully")
        
        # Return complete workflow result
        return {
            "status": "success",
            "workflow": {
                "analysis": analysis,
                "matched_template": matched_template,
                "template_match_score": template_result['match_score'],
                "study_guide": generation_result['study_guide']
            }
        }


# Global coordinator instance
_coordinator = None


def get_coordinator():
    """Get or create the Agent Coordinator"""
    global _coordinator
    if _coordinator is None:
        _coordinator = AgentCoordinator()
    return _coordinator
