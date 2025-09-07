"""
Legal Memespace: Evolutionary Analysis of Legal Systems

This package implements the Extended Phenotype Theory for analyzing
the evolution of legal systems through memetic analysis.

Author: Ignacio Adrián Lerer
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Ignacio Adrián Lerer"
__email__ = "ignacio.lerer@example.com"

from .core.meme_vector import LegalMemeVector
from .core.similarity import cosine_similarity, legal_memetic_distance
from .extractors.anticorruption import AntiCorruptionExtractor

__all__ = [
    'LegalMemeVector',
    'cosine_similarity',
    'legal_memetic_distance',
    'AntiCorruptionExtractor',
]