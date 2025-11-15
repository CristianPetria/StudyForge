"""
Template Matching Agent
Responsible for matching analyzed content to the most appropriate study guide template
"""

from backend.config import STUDY_TEMPLATES
from backend.utils.clients import get_mistral_client, get_qdrant_client
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class TemplateMatchingAgent:
    """Agent for matching content to templates"""
    
    def __init__(self):
        self.mistral_client = get_mistral_client()
        self.qdrant_client = get_qdrant_client()
        self.template_collection = "learning_templates"
        self._initialized = False
    
    def initialize(self):
        """Initialize template embeddings in Qdrant"""
        if self._initialized or not self.mistral_client or not self.qdrant_client:
            return False
        
        try:
            from qdrant_client.models import Distance, VectorParams, PointStruct
            import time
            
            logger.info("🔧 Initializing template embeddings...")
            
            # Create collection
            self.qdrant_client.create_collection(
                collection_name=self.template_collection,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
            )
            
            # Prepare texts to embed
            texts_to_embed = []
            for template in STUDY_TEMPLATES:
                embed_text = f"{template['name']}: {template['description']}. Best for {template['example_use_case']}"
                texts_to_embed.append(embed_text)
            
            logger.info(f"📚 Creating embeddings for {len(STUDY_TEMPLATES)} templates...")
            
            # Get embeddings
            try:
                embedding_response = self.mistral_client.embeddings.create(
                    model="mistral-embed",
                    inputs=texts_to_embed
                )
            except Exception as e:
                logger.warning(f"Batch embedding failed, retrying with delay: {e}")
                time.sleep(2)
                embedding_response = self.mistral_client.embeddings.create(
                    model="mistral-embed",
                    inputs=texts_to_embed
                )
            
            # Create points for Qdrant
            points = []
            for idx, (template, embedding_data) in enumerate(zip(STUDY_TEMPLATES, embedding_response.data)):
                point = PointStruct(
                    id=idx,
                    vector=embedding_data.embedding,
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
                logger.info(f"  ✓ Embedded: {template['name']}")
            
            # Upload to Qdrant
            self.qdrant_client.upsert(
                collection_name=self.template_collection,
                points=points
            )
            
            logger.info(f"✅ Successfully initialized {len(points)} template embeddings")
            self._initialized = True
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to initialize templates: {e}", exc_info=True)
            return False
    
    def match_template(self, analysis=None, selected_template_id=None):
        """
        Match content analysis to the best template
        
        Args:
            analysis (dict): Content analysis results
            selected_template_id (str): User-selected template ID (overrides AI matching)
        
        Returns:
            dict: Matched template and score
        """
        try:
            # If user manually selected a template
            if selected_template_id:
                logger.info(f"📌 User selected template: {selected_template_id}")
                matched_template = next(
                    (t for t in STUDY_TEMPLATES if t['id'] == selected_template_id),
                    None
                )
                
                if not matched_template:
                    return {
                        "status": "error",
                        "message": f"Template '{selected_template_id}' not found"
                    }
                
                return {
                    "status": "success",
                    "matched_template": matched_template,
                    "match_score": 1.0,
                    "method": "user_selected"
                }
            
            # Use AI to match template
            if not self.mistral_client or not self.qdrant_client:
                logger.error("Clients not available for template matching")
                return {
                    "status": "error",
                    "message": "AI matching service not available"
                }
            
            if not self._initialized:
                logger.warning("Template agent not initialized, using fallback")
                return {
                    "status": "success",
                    "matched_template": STUDY_TEMPLATES[0],
                    "match_score": 0.5,
                    "method": "fallback"
                }
            
            logger.info("🔍 Using AI to match template...")
            
            # Create search query
            analysis = analysis or {}
            content_type = analysis.get('detected_content_type', 'unknown')
            topic = analysis.get('topic', '')
            difficulty = analysis.get('difficulty_level', '')
            
            query_text = f"{content_type}: {topic}. Difficulty: {difficulty}"
            logger.info(f"  Query: {query_text}")
            
            # Get embedding for query
            query_embedding_response = self.mistral_client.embeddings.create(
                model="mistral-embed",
                inputs=[query_text]
            )
            query_vector = query_embedding_response.data[0].embedding
            
            # Search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.template_collection,
                query_vector=query_vector,
                limit=2
            )
            
            if not search_results:
                logger.warning("No matching templates found, using default")
                matched_template = STUDY_TEMPLATES[0]
                match_score = 0.5
            else:
                best_match = search_results[0]
                match_score = best_match.score
                logger.info(f"✅ Best match: {best_match.payload['template_name']} (score: {match_score:.3f})")
                
                matched_template = next(
                    (t for t in STUDY_TEMPLATES if t['id'] == best_match.payload['template_id']),
                    STUDY_TEMPLATES[0]
                )
            
            return {
                "status": "success",
                "matched_template": matched_template,
                "match_score": float(match_score),
                "method": "ai_matched"
            }
        
        except Exception as e:
            logger.error(f"❌ Error during template matching: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Template matching failed: {str(e)}"
            }


# Global agent instance
_template_agent = None


def get_template_matching_agent():
    """Get or create the Template Matching Agent"""
    global _template_agent
    if _template_agent is None:
        _template_agent = TemplateMatchingAgent()
        _template_agent.initialize()
    return _template_agent
