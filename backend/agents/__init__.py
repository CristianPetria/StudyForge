"""
Backend agents package
Initializes all AI agents for different tasks
"""

from backend.agents.analysis_agent import get_analysis_agent
from backend.agents.template_matching_agent import get_template_matching_agent
from backend.agents.generation_agent import get_generation_agent
from backend.agents.coordinator import get_coordinator

__all__ = [
    'get_analysis_agent',
    'get_template_matching_agent', 
    'get_generation_agent',
    'get_coordinator'
]
