"""
Legal text extractors for specific domains.
"""

from .base_extractor import BaseLegalExtractor
from .anticorruption import AntiCorruptionExtractor
from .text_processing import LegalTextProcessor

__all__ = [
    'BaseLegalExtractor',
    'AntiCorruptionExtractor', 
    'LegalTextProcessor',
]