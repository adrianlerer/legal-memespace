"""
Data collection and management modules.
"""

from .collectors import LegalTextCollector
from .apis import LegalAPIClient

__all__ = [
    'LegalTextCollector',
    'LegalAPIClient',
]