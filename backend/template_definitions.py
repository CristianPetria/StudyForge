"""
StudyForge Template Definitions
Rich, semantic templates for different learning contexts and content types.
"""

# ============================================================================
# TEMPLATE DEFINITIONS
# ============================================================================

TEMPLATES = [
    {
        "id": "generic_study_guide",
        "name": "Universal Study Guide",
        "emoji": "✨",
        "description": "A flexible, all-purpose study guide that adapts to any subject or topic. Perfect when you're not sure which template to choose or need a balanced approach covering all aspects of learning.",
        "best_for": [
            "Any subject or topic",
            "Mixed content types",
            "General study materials",
            "Self-paced learning",
            "Personal notes organization",
            "Diverse learning needs"
        ],
        "features": [
            "Adaptive content structure",
            "Balanced overview and details",
            "Flexible section organization",
            "Universal applicability"
        ],
        "color": "#6366f1",
        "sections": [
            "Overview & Introduction",
            "Key Concepts",
            "Detailed Explanation",
            "Practice & Review"
        ],
        "qdrant_description": "general purpose universal flexible adaptable any topic subject versatile all-purpose generic study guide comprehensive balanced mixed content self-paced learning personal notes organization diverse needs fallback default standard"
    },
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
    },
    {
        "id": "language_learning",
        "name": "Language Learning Companion",
        "emoji": "🌍",
        "description": "Master new languages with structured vocabulary, grammar rules, common phrases, and cultural context. Includes pronunciation tips and practical conversation scenarios.",
        "best_for": [
            "Foreign language study",
            "Vocabulary building",
            "Grammar fundamentals",
            "Conversation practice",
            "Travel preparation",
            "Language certification prep"
        ],
        "features": [
            "Vocabulary categorization",
            "Grammar rule explanations",
            "Practical phrases & dialogues",
            "Cultural context notes"
        ],
        "color": "#10b981",
        "sections": [
            "Essential Vocabulary",
            "Grammar Foundations",
            "Common Phrases & Expressions",
            "Cultural Notes",
            "Practice Conversations"
        ],
        "qdrant_description": "language learning foreign languages vocabulary grammar phrases conversation practice pronunciation cultural context travel preparation French Spanish German Italian Chinese Japanese Korean Arabic Russian Portuguese language certification DELF DELE HSK JLPT beginner intermediate advanced ESL linguistics"
    },
    {
        "id": "technical_documentation",
        "name": "Technical Documentation Guide",
        "emoji": "💻",
        "description": "Break down complex technical documentation, API references, and programming concepts into digestible guides with code examples and best practices.",
        "best_for": [
            "API documentation",
            "Programming tutorials",
            "Software architecture",
            "Code libraries & frameworks",
            "System design documents",
            "Developer onboarding"
        ],
        "features": [
            "Code snippet organization",
            "API endpoint summaries",
            "Best practices highlights",
            "Error handling patterns"
        ],
        "color": "#3b82f6",
        "sections": [
            "Overview & Setup",
            "Core Concepts & Architecture",
            "API Reference",
            "Code Examples",
            "Best Practices",
            "Troubleshooting"
        ],
        "qdrant_description": "technical documentation programming code API reference software development web development mobile development backend frontend DevOps cloud computing databases JavaScript Python Java C++ React Node Angular Vue Django Flask Spring REST GraphQL microservices containers Docker Kubernetes AWS Azure GCP system design architecture patterns algorithms data structures"
    },
    {
        "id": "scientific_research",
        "name": "Research Paper Analyzer",
        "emoji": "🔬",
        "description": "Distill academic research papers into clear summaries highlighting methodology, findings, and implications. Perfect for literature reviews and research synthesis.",
        "best_for": [
            "Academic research papers",
            "Scientific journals",
            "Literature reviews",
            "Thesis research",
            "Medical studies",
            "Experimental reports"
        ],
        "features": [
            "Methodology breakdown",
            "Key findings extraction",
            "Statistical analysis summary",
            "Research implications"
        ],
        "color": "#8b5cf6",
        "sections": [
            "Research Overview",
            "Methodology",
            "Key Findings",
            "Analysis & Discussion",
            "Implications & Future Research"
        ],
        "qdrant_description": "research paper scientific study academic journal peer review methodology findings results analysis statistics hypothesis experiment data clinical trial literature review meta-analysis biology chemistry physics medicine neuroscience psychology sociology anthropology environmental science"
    },
    {
        "id": "creative_writing",
        "name": "Literature & Writing Analysis",
        "emoji": "📖",
        "description": "Analyze literary works, creative writing techniques, narrative structures, and thematic elements. Includes character analysis and stylistic device breakdowns.",
        "best_for": [
            "Novel analysis",
            "Poetry interpretation",
            "Creative writing techniques",
            "Literary criticism",
            "Drama & plays",
            "Screenwriting fundamentals"
        ],
        "features": [
            "Character development analysis",
            "Theme identification",
            "Literary device explanations",
            "Narrative structure breakdown"
        ],
        "color": "#ec4899",
        "sections": [
            "Plot Summary",
            "Character Analysis",
            "Themes & Motifs",
            "Literary Devices",
            "Critical Perspectives"
        ],
        "qdrant_description": "literature creative writing novels poetry drama plays Shakespeare fiction non-fiction literary analysis character development plot structure themes symbolism metaphor narrative techniques screenwriting storytelling English literature American literature world literature classics contemporary literature"
    },
    {
        "id": "mathematics_problem_solving",
        "name": "Math Problem Solver",
        "emoji": "🔢",
        "description": "Step-by-step mathematical problem solving with formula explanations, worked examples, and practice problems across all levels of mathematics.",
        "best_for": [
            "Algebra & calculus",
            "Geometry & trigonometry",
            "Statistics & probability",
            "Linear algebra",
            "Differential equations",
            "Applied mathematics"
        ],
        "features": [
            "Formula derivations",
            "Step-by-step solutions",
            "Visual diagrams",
            "Practice problem sets"
        ],
        "color": "#f59e0b",
        "sections": [
            "Formulas & Theorems",
            "Worked Examples",
            "Problem-Solving Strategies",
            "Practice Problems",
            "Common Mistakes"
        ],
        "qdrant_description": "mathematics math algebra calculus geometry trigonometry statistics probability linear algebra differential equations number theory discrete math applied mathematics mathematical proofs problem solving equations functions derivatives integrals matrices vectors"
    },
    {
        "id": "medical_clinical",
        "name": "Medical Study Guide",
        "emoji": "⚕️",
        "description": "Comprehensive medical and clinical study guides covering anatomy, pathology, pharmacology, and clinical procedures with diagnostic criteria and treatment protocols.",
        "best_for": [
            "Medical school courses",
            "Nursing education",
            "Clinical procedures",
            "Pharmacology",
            "Anatomy & physiology",
            "Board exam preparation"
        ],
        "features": [
            "Anatomical diagrams",
            "Disease pathophysiology",
            "Drug mechanisms",
            "Clinical decision trees"
        ],
        "color": "#dc2626",
        "sections": [
            "Anatomical Overview",
            "Pathophysiology",
            "Clinical Presentation",
            "Diagnostic Criteria",
            "Treatment & Management"
        ],
        "qdrant_description": "medical medicine healthcare clinical anatomy physiology pathology pharmacology nursing doctor physician USMLE NCLEX medical school diagnosis treatment patient care surgery internal medicine pediatrics cardiology neurology emergency medicine medical terminology disease conditions drugs medications clinical practice evidence-based medicine"
    },
    {
        "id": "data_science",
        "name": "Data Science & Analytics",
        "emoji": "📈",
        "description": "Master data science concepts including machine learning, statistical analysis, data visualization, and predictive modeling with practical applications.",
        "best_for": [
            "Machine learning concepts",
            "Statistical modeling",
            "Data visualization",
            "Big data processing",
            "AI fundamentals",
            "Business analytics"
        ],
        "features": [
            "Algorithm explanations",
            "Statistical methods",
            "Code implementations",
            "Real-world applications"
        ],
        "color": "#06b6d4",
        "sections": [
            "Concepts & Terminology",
            "Statistical Foundations",
            "Algorithms & Models",
            "Implementation Examples",
            "Applications & Use Cases"
        ],
        "qdrant_description": "data science machine learning artificial intelligence AI deep learning neural networks statistics analytics big data Python R SQL pandas numpy scikit-learn TensorFlow PyTorch data visualization tableau power BI predictive modeling regression classification clustering natural language processing computer vision"
    },
    {
        "id": "legal_studies",
        "name": "Legal Studies & Law",
        "emoji": "⚖️",
        "description": "Analyze legal concepts, case law, statutes, and legal reasoning. Includes case briefs, legal principles, and jurisdictional comparisons.",
        "best_for": [
            "Law school courses",
            "Legal case analysis",
            "Constitutional law",
            "Contract law",
            "Criminal law",
            "Bar exam preparation"
        ],
        "features": [
            "Case brief format",
            "Legal principle extraction",
            "Precedent analysis",
            "Jurisdictional notes"
        ],
        "color": "#78350f",
        "sections": [
            "Legal Principles",
            "Case Analysis",
            "Statutory Interpretation",
            "Legal Reasoning",
            "Practical Applications"
        ],
        "qdrant_description": "law legal studies constitutional law contract law criminal law civil procedure evidence torts property law administrative law international law case law statutes legal reasoning case briefs IRAC legal analysis bar exam LSAT law school attorney lawyer legal practice judicial opinions precedent jurisdiction"
    },
    {
        "id": "book_summary_pro",
        "name": "Non-Fiction Book Summary",
        "emoji": "📖",
        "description": "Distills an entire non-fiction book or long article into its core ideas, actionable takeaways, and supporting arguments. Perfect for business books or self-help.",
        "best_for": [
            "Business books",
            "Self-help & productivity",
            "Biographies",
            "Long-form articles",
            "Academic papers"
        ],
        "features": [
            "Core thesis extraction",
            "Actionable takeaways",
            "Key arguments (3-5)",
            "Author's main points"
        ],
        "color": "#10b981",
        "sections": [
            "Author's Core Thesis",
            "Top 5 Key Ideas",
            "Actionable Takeaways",
            "Supporting Arguments & Examples",
            "Concluding Summary"
        ],
        "qdrant_description": "book summary non-fiction business book self-help productivity biography article abstract thesis key ideas takeaways arguments author's point Blinkist-style reading notes main ideas"
    },
    {
        "id": "math_concept_solver",
        "name": "Math Concept Solver",
        "emoji": "🧮",
        "description": "Breaks down complex math problems and concepts. Explains the 'why' behind the formulas and provides step-by-step solutions.",
        "best_for": [
            "Calculus problems",
            "Algebra concepts",
            "Geometry proofs",
            "Statistics homework",
            "Trigonometry"
        ],
        "features": [
            "Step-by-step problem solving",
            "Core theorem/formula explanation",
            "Common mistakes",
            "Practice problem generation"
        ],
        "color": "#3182ce",
        "sections": [
            "Core Concept & Definition",
            "Key Formulas & Theorems",
            "Step-by-Step Solved Example",
            "Common Pitfalls to Avoid",
            "Practice Problems"
        ],
        "qdrant_description": "math mathematics calculus algebra geometry statistics trigonometry problem solver step-by-step solution formula theorem proof homework help practice problems equations"
    },
    {
        "id": "historical_analysis",
        "name": "Historical Analysis Deep Dive",
        "emoji": "🏛️",
        "description": "Goes beyond dates to analyze historical events. Focuses on cause & effect, primary sources, key figures, and long-term impact.",
        "best_for": [
            "History essays",
            "AP History prep",
            "Analyzing primary sources",
            "Understanding historical context",
            "Government & Civics"
        ],
        "features": [
            "Cause & Effect analysis",
            "Key figures & perspectives",
            "Primary source interpretation",
            "Long-term significance"
        ],
        "color": "#b7791f",
        "sections": [
            "Historical Context & Overview",
            "Key Figures & Factions",
            "Cause & Effect Analysis",
            "Long-Term Significance & Impact",
            "Primary Source Spotlight"
        ],
        "qdrant_description": "history analysis essay deep dive cause and effect primary source key figures historical event context impact significance AP History government civics historical documents"
    },
    {
        "id": "marketing_plan_builder",
        "name": "Marketing Plan Builder",
        "emoji": "📈",
        "description": "Converts marketing theory or case studies into a structured marketing plan. Focuses on the 4Ps, SWOT, and target audience.",
        "best_for": [
            "Marketing class notes",
            "Business school projects",
            "SWOT analysis",
            "Marketing strategy",
            "Case studies"
        ],
        "features": [
            "SWOT analysis generation",
            "Target audience persona",
            "Marketing Mix (4Ps) breakdown",
            "Campaign ideas"
        ],
        "color": "#d53f8c",
        "sections": [
            "Executive Summary & Goals",
            "SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)",
            "Target Audience & Persona",
            "Marketing Mix (Product, Price, Place, Promotion)",
            "Key Performance Indicators (KPIs)"
        ],
        "qdrant_description": "marketing plan strategy business school SWOT analysis 4Ps product price place promotion target audience persona campaign KPIs marketing mix business strategy"
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
