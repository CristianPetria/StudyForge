"""
StudyForge Template Definitions
Rich, semantic templates for different learning contexts and content types.
"""

# ============================================================================
# TEMPLATE DEFINITIONS
# ============================================================================

TEMPLATES = [
    {
        "id": "academic_lecture",
        "name": "Academic Lecture Digest",
        "emoji": "📚",
        "description": "Transform dense university lectures into crystal-clear study guides with organized concepts, definitions, and real-world examples. Perfect for STEM courses, social sciences, and humanities.",
        "best_for": [
            "University lectures",
            "Economics & business courses",
            "Science & engineering classes",
            "Psychology & social sciences",
            "Philosophy & humanities",
            "Recorded lecture transcripts"
        ],
        "features": [
            "Hierarchical concept organization",
            "Definition extraction & clarification",
            "Key examples with context",
            "Professor's main arguments highlighted"
        ],
        "color": "#667eea",
        "sections": [
            "Core Concepts & Definitions",
            "Key Theories & Models",
            "Important Examples",
            "Summary & Takeaways"
        ],
        "qdrant_description": "university lecture notes college class academic course professor teaching theoretical concepts definitions examples STEM science economics business social sciences humanities philosophy recorded lectures educational content structured learning course material"
    },
    {
        "id": "case_study",
        "name": "Business Case Analyzer",
        "emoji": "📊",
        "description": "Dissect complex business cases into actionable frameworks. Extract problem statements, analyze stakeholders, evaluate strategic options, and synthesize recommendations like a McKinsey consultant.",
        "best_for": [
            "Harvard Business School cases",
            "MBA case studies",
            "Strategic management scenarios",
            "Marketing case analyses",
            "Corporate decision-making exercises",
            "Consulting frameworks"
        ],
        "features": [
            "Problem decomposition & framing",
            "Stakeholder impact analysis",
            "Strategic framework application",
            "Data-driven recommendations"
        ],
        "color": "#764ba2",
        "sections": [
            "Situation & Problem Statement",
            "Stakeholder Analysis",
            "Strategic Framework & Options",
            "Recommendations & Action Plan",
            "Key Insights & Lessons"
        ],
        "qdrant_description": "business case study Harvard HBS MBA strategic management consulting McKinsey framework analysis stakeholder corporate decision making strategy marketing finance operations problem solving case competition real world scenarios company analysis SWOT Porter competitive advantage"
    },
    {
        "id": "quick_reference",
        "name": "Quick Reference Sheet",
        "emoji": "⚡",
        "description": "Create ultra-condensed cheat sheets with essential formulas, equations, key facts, and critical procedures. Your go-to resource for rapid review before exams or practical application.",
        "best_for": [
            "Mathematics & calculus",
            "Physics & chemistry formulas",
            "Programming syntax guides",
            "Statistical methods",
            "Financial calculations",
            "Medical procedures & protocols"
        ],
        "features": [
            "Formula extraction & organization",
            "One-page visual layout",
            "Color-coded by topic",
            "Quick lookup structure"
        ],
        "color": "#f59e0b",
        "sections": [
            "Essential Formulas & Equations",
            "Key Facts & Constants",
            "Procedures & Algorithms",
            "Common Mistakes to Avoid"
        ],
        "qdrant_description": "cheat sheet formulas equations quick reference mathematics physics chemistry statistics programming code syntax financial calculations medical procedures exam prep fast review one page summary essential facts algorithms methods condensed guide lookup table formula sheet"
    },
    {
        "id": "historical_timeline",
        "name": "Historical Timeline Builder",
        "emoji": "📜",
        "description": "Convert historical narratives into chronological timelines with cause-and-effect relationships. Track events, figures, movements, and their interconnections across time periods.",
        "best_for": [
            "World history courses",
            "Art history movements",
            "Scientific revolutions",
            "Political science & government",
            "Cultural studies",
            "Biography & autobiography"
        ],
        "features": [
            "Chronological event sequencing",
            "Cause-and-effect linking",
            "Key figures & their roles",
            "Thematic connections across periods"
        ],
        "color": "#8b5cf6",
        "sections": [
            "Timeline of Key Events",
            "Important Figures & Leaders",
            "Causes & Consequences",
            "Thematic Connections",
            "Historical Significance"
        ],
        "qdrant_description": "history timeline chronology events dates historical narrative world history art history political science revolution war biography historical figures cause effect sequence periods movements cultural studies government past timeline historical context important dates sequential historical analysis"
    },
    {
        "id": "exam_prep",
        "name": "Exam Preparation Sprint",
        "emoji": "🎯",
        "description": "High-intensity exam prep with practice questions, must-know topics, memory techniques, and strategic test-taking tips. Optimized for last-minute cramming and comprehensive review.",
        "best_for": [
            "Final exams & midterms",
            "Standardized tests (SAT, GRE, GMAT)",
            "Professional certifications",
            "Medical board exams",
            "Bar exam preparation",
            "Quick review sessions"
        ],
        "features": [
            "Priority topic ranking",
            "Practice question generation",
            "Memory aids & mnemonics",
            "Time management strategies"
        ],
        "color": "#ef4444",
        "sections": [
            "Must-Know Topics (Ranked)",
            "Practice Questions & Answers",
            "Key Formulas & Facts",
            "Memory Techniques",
            "Test-Taking Strategy",
            "Common Exam Traps"
        ],
        "qdrant_description": "exam preparation test prep final exam midterm practice questions review study guide cramming certification standardized test SAT GRE GMAT LSAT MCAT bar exam professional certification quiz practice test taking strategy memory techniques mnemonics high priority topics exam tips test anxiety time management exam readiness"
    }
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_all_templates():
    """
    Returns all available study guide templates.

    Returns:
        list: List of all template dictionaries
    """
    return TEMPLATES


def get_template_by_id(template_id):
    """
    Retrieve a specific template by its ID.

    Args:
        template_id (str): The unique identifier of the template

    Returns:
        dict: Template dictionary if found, None otherwise
    """
    for template in TEMPLATES:
        if template['id'] == template_id:
            return template
    return None


def get_template_names():
    """
    Get a list of all template names for display purposes.

    Returns:
        list: List of tuples (id, name, emoji)
    """
    return [(t['id'], t['name'], t['emoji']) for t in TEMPLATES]


def get_templates_by_subject(subject_keyword):
    """
    Find templates that match a specific subject area.

    Args:
        subject_keyword (str): Keyword to search in 'best_for' field

    Returns:
        list: List of matching templates
    """
    matching_templates = []
    keyword_lower = subject_keyword.lower()

    for template in TEMPLATES:
        for subject in template['best_for']:
            if keyword_lower in subject.lower():
                matching_templates.append(template)
                break

    return matching_templates


def get_template_qdrant_texts():
    """
    Get texts optimized for Qdrant embedding, used for semantic matching.

    Returns:
        list: List of tuples (template_id, qdrant_text)
    """
    return [
        (t['id'], t['qdrant_description'])
        for t in TEMPLATES
    ]


def validate_template(template):
    """
    Validate that a template has all required fields.

    Args:
        template (dict): Template to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = [
        'id', 'name', 'emoji', 'description', 'best_for',
        'features', 'color', 'sections', 'qdrant_description'
    ]

    for field in required_fields:
        if field not in template:
            return False, f"Missing required field: {field}"

    # Validate types
    if not isinstance(template['best_for'], list):
        return False, "'best_for' must be a list"

    if not isinstance(template['features'], list):
        return False, "'features' must be a list"

    if not isinstance(template['sections'], list):
        return False, "'sections' must be a list"

    if len(template['features']) != 4:
        return False, "'features' must contain exactly 4 items"

    # Validate color format (basic hex check)
    if not template['color'].startswith('#') or len(template['color']) != 7:
        return False, "'color' must be a valid hex color code (e.g., #667eea)"

    return True, None


# Validate all templates on import
if __name__ == "__main__":
    print("🔍 Validating StudyForge templates...")

    for template in TEMPLATES:
        is_valid, error = validate_template(template)
        if is_valid:
            print(f"  ✅ {template['name']}")
        else:
            print(f"  ❌ {template['name']}: {error}")

    print(f"\n📊 Total templates: {len(TEMPLATES)}")
    print("\n📋 Template Summary:")
    for tid, name, emoji in get_template_names():
        print(f"  {emoji} {name} ({tid})")
