"""
Core modules for legal memetic analysis.
"""

from .meme_vector import LegalMemeVector
from .similarity import cosine_similarity, legal_memetic_distance, cultural_distance_weighting, temporal_decay_function
from .fitness import calculate_legal_fitness, evolutionary_pressure

__all__ = [
    'LegalMemeVector',
    'cosine_similarity',
    'legal_memetic_distance',
    'cultural_distance_weighting',
    'temporal_decay_function',
    'calculate_legal_fitness',
    'evolutionary_pressure',
]