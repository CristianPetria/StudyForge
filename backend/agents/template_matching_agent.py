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
    
    def find_best_templates(self, query_text, top_k=3, user_preferences=None):
        """
        Find the best matching templates for a given query using Qdrant semantic search
        
        Args:
            query_text (str): Search query describing what the user needs
            top_k (int): Number of top templates to return
            user_preferences (dict): Optional dict with age_group, learning_style, course_type
        
        Returns:
            list: List of suggested templates with match scores
        """
        try:
            if not self.mistral_client:
                logger.warning("Mistral client not available, returning default templates")
                return [
                    {
                        "id": t["id"],
                        "name": t["name"],
                        "description": t["description"],
                        "icon_emoji": t["icon_emoji"],
                        "match_score": 0.5
                    }
                    for t in STUDY_TEMPLATES[:top_k]
                ]
            
            # Build comprehensive search query from form data and description
            enhanced_query = self._build_search_query(query_text, user_preferences)
            logger.info(f"🔍 Finding best templates for query: {enhanced_query[:100]}")
            
            # Get embedding for the enhanced query
            query_embedding_response = self.mistral_client.embeddings.create(
                model="mistral-embed",
                inputs=[enhanced_query]
            )
            query_vector = query_embedding_response.data[0].embedding
            
            # If Qdrant is available and initialized, use semantic search
            if self.qdrant_client and self._initialized:
                try:
                    search_results = self.qdrant_client.search(
                        collection_name=self.template_collection,
                        query_vector=query_vector,
                        limit=top_k
                    )
                    
                    suggested_templates = []
                    for result in search_results:
                        suggested_templates.append({
                            "id": result.payload["template_id"],
                            "name": result.payload["template_name"],
                            "description": result.payload["description"],
                            "icon_emoji": result.payload["icon_emoji"],
                            "match_score": float(result.score),
                            "match_details": {
                                "semantic_match": True,
                                "query_type": user_preferences.get('course_type', 'unknown') if user_preferences else 'unknown',
                                "learning_style": user_preferences.get('learning_style', 'unknown') if user_preferences else 'unknown'
                            }
                        })
                    
                    logger.info(f"✅ Found {len(suggested_templates)} templates via Qdrant semantic search")
                    return suggested_templates
                
                except Exception as e:
                    logger.warning(f"Qdrant semantic search failed: {e}, falling back to keyword matching")
            
            # Fallback: Return templates based on keyword and preference matching
            logger.info("📚 Using fallback keyword-based template matching")
            return self._keyword_based_matching(enhanced_query, query_text, user_preferences, top_k)
        
        except Exception as e:
            logger.error(f"❌ Error finding templates: {str(e)}", exc_info=True)
            # Return default templates on error
            return [
                {
                    "id": t["id"],
                    "name": t["name"],
                    "description": t["description"],
                    "icon_emoji": t["icon_emoji"],
                    "match_score": 0.5
                }
                for t in STUDY_TEMPLATES[:top_k]
            ]
    
    def _build_search_query(self, description, user_preferences=None):
        """
        Build a comprehensive search query from form data and natural language description
        
        Args:
            description (str): User's natural language description
            user_preferences (dict): Form data with age_group, learning_style, course_type
        
        Returns:
            str: Enhanced search query combining all information
        """
        if not user_preferences:
            return description
        
        # Map user preferences to search terms
        age_group = user_preferences.get('age_group', '')
        learning_style = user_preferences.get('learning_style', '')
        course_type = user_preferences.get('course_type', '')
        
        # Build semantic query
        query_parts = [description]
        
        if learning_style:
            learning_style_map = {
                'visual': 'visual diagrams charts infographics',
                'textual': 'notes summaries text-based written content',
                'practical': 'examples exercises hands-on practical applications',
                'mixed': 'diverse mixed multimedia content'
            }
            query_parts.append(learning_style_map.get(learning_style, learning_style))
        
        if course_type:
            course_type_map = {
                'business': 'business marketing economics finance management',
                'science': 'science biology chemistry physics mathematics',
                'technical': 'technical programming engineering APIs documentation',
                'humanities': 'humanities literature history philosophy arts',
                'languages': 'languages linguistics vocabulary grammar',
                'other': 'general content'
            }
            query_parts.append(course_type_map.get(course_type, course_type))
        
        if age_group:
            age_group_map = {
                'high-school': 'high school beginner level introductory',
                'university': 'university advanced college academic',
                'professional': 'professional expert practitioner industry',
                'lifelong': 'lifelong learner general audience'
            }
            query_parts.append(age_group_map.get(age_group, age_group))
        
        enhanced_query = ' '.join(query_parts)
        logger.info(f"📝 Enhanced query: {enhanced_query[:150]}")
        return enhanced_query
    
    def _keyword_based_matching(self, enhanced_query, original_description, user_preferences, top_k):
        """
        Fallback keyword-based matching when Qdrant is unavailable
        
        Args:
            enhanced_query (str): Combined search query
            original_description (str): Original user description
            user_preferences (dict): Form preferences
            top_k (int): Number of templates to return
        
        Returns:
            list: Ranked templates based on keyword matching
        """
        query_lower = enhanced_query.lower()
        keywords = set(word for word in query_lower.split() if len(word) > 3)
        
        scored_templates = []
        for template in STUDY_TEMPLATES:
            score = 0.0
            template_text = f"{template['name']} {template['description']} {template['example_use_case']}".lower()
            
            # Keyword matching
            matching_keywords = sum(1 for keyword in keywords if keyword in template_text)
            score += matching_keywords * 0.1
            
            # Course type matching
            if user_preferences:
                course_type = user_preferences.get('course_type', '')
                if course_type and course_type.lower() in template_text:
                    score += 0.2
                
                # Learning style matching
                learning_style = user_preferences.get('learning_style', '')
                if learning_style == 'visual' and any(term in template_text for term in ['diagram', 'visual', 'chart']):
                    score += 0.15
                elif learning_style == 'practical' and any(term in template_text for term in ['example', 'exercise', 'practice']):
                    score += 0.15
                elif learning_style == 'textual' and any(term in template_text for term in ['summary', 'notes', 'text']):
                    score += 0.15
            
            scored_templates.append({
                "template": template,
                "score": min(score, 1.0)
            })
        
        # Sort by score and return top_k
        scored_templates.sort(key=lambda x: x["score"], reverse=True)
        
        suggested_templates = [
            {
                "id": item["template"]["id"],
                "name": item["template"]["name"],
                "description": item["template"]["description"],
                "icon_emoji": item["template"]["icon_emoji"],
                "match_score": item["score"],
                "match_details": {
                    "semantic_match": False,
                    "matching_method": "keyword_based"
                }
            }
            for item in scored_templates[:top_k]
        ]
        
        logger.info(f"✅ Found {len(suggested_templates)} templates via keyword matching")
        return suggested_templates


# Global agent instance
_template_agent = None


def get_template_matching_agent():
    """Get or create the Template Matching Agent"""
    global _template_agent
    if _template_agent is None:
        _template_agent = TemplateMatchingAgent()
        _template_agent.initialize()
    return _template_agent
