"""
Base Legal Extractor

This module provides the abstract base class for all legal text extractors
in the Legal Memespace framework. It defines the common interface and
shared functionality for domain-specific feature extraction.

Author: Ignacio Adrián Lerer
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union, Tuple
import numpy as np
import re
import logging
from dataclasses import dataclass
from datetime import datetime

from ..core.meme_vector import LegalMemeVector, LegalContext

logger = logging.getLogger(__name__)


@dataclass
class ExtractionConfig:
    """Configuration for legal text extraction."""
    
    include_structural: bool = True
    include_semantic: bool = True
    include_domain_specific: bool = True
    normalize_features: bool = True
    feature_weights: Optional[Dict[str, float]] = None
    custom_patterns: Optional[Dict[str, str]] = None


class BaseLegalExtractor(ABC):
    """
    Abstract base class for legal text feature extractors.
    
    This class defines the common interface that all domain-specific
    extractors must implement, following the Extended Phenotype Theory
    framework for legal evolution analysis.
    """
    
    def __init__(
        self,
        config: Optional[ExtractionConfig] = None,
        custom_patterns: Optional[Dict[str, str]] = None
    ):
        """
        Initialize the base extractor.
        
        Args:
            config: Extraction configuration
            custom_patterns: Custom regex patterns for extraction
        """
        self.config = config or ExtractionConfig()
        self.custom_patterns = custom_patterns or {}
        self.feature_names: List[str] = []
        self._compiled_patterns: Dict[str, re.Pattern] = {}
        
        # Compile regex patterns for efficiency
        self._compile_patterns()
        
        logger.info(f"Initialized {self.__class__.__name__}")
    
    def _compile_patterns(self):
        """Compile regex patterns for efficient matching."""
        # Common legal patterns
        default_patterns = {
            'section_reference': r'§\s*\d+(?:\.\d+)*|\bsection\s+\d+(?:\.\d+)*',
            'article_reference': r'\barticle\s+\d+(?:\.\d+)*',
            'paragraph_reference': r'\bparagraph\s+\d+(?:\.\d+)*|\b\(\d+\)',
            'subsection_reference': r'\bsubsection\s+\d+(?:\.\d+)*',
            'monetary_amount': r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\b\d{1,3}(?:,\d{3})*\s*dollars?',
            'percentage': r'\d+(?:\.\d+)?%',
            'time_period': r'\b\d+\s*(?:days?|weeks?|months?|years?)',
            'legal_citation': r'\b\d+\s+[A-Z][a-z]+\s+\d+',
            'criminal_penalty': r'\bimprisonment\b|\bfine\b|\bpenalty\b|\bsanctions?\b',
            'compliance_terms': r'\bcompliance\b|\bdue\s+diligence\b|\binternal\s+controls?\b'
        }
        
        # Merge with custom patterns
        all_patterns = {**default_patterns, **self.custom_patterns}
        
        for name, pattern in all_patterns.items():
            try:
                self._compiled_patterns[name] = re.compile(pattern, re.IGNORECASE)
            except re.error as e:
                logger.warning(f"Failed to compile pattern '{name}': {e}")
    
    @abstractmethod
    def extract_domain_features(self, meme_vector: LegalMemeVector) -> np.ndarray:
        """
        Extract domain-specific features from the legal text.
        
        Args:
            meme_vector: Legal meme vector to extract features from
            
        Returns:
            Domain-specific feature array
        """
        pass
    
    @abstractmethod
    def get_feature_names(self) -> List[str]:
        """
        Get the names of features extracted by this extractor.
        
        Returns:
            List of feature names
        """
        pass
    
    def extract_all_features(self, meme_vector: LegalMemeVector) -> Dict[str, np.ndarray]:
        """
        Extract all configured feature types from the legal text.
        
        Args:
            meme_vector: Legal meme vector to extract features from
            
        Returns:
            Dictionary mapping feature type names to feature arrays
        """
        features = {}
        
        if self.config.include_structural:
            features['structural'] = self.extract_structural_features(meme_vector)
        
        if self.config.include_semantic:
            features['semantic'] = self.extract_semantic_features(meme_vector)
        
        if self.config.include_domain_specific:
            features['domain'] = self.extract_domain_features(meme_vector)
        
        # Normalize features if requested
        if self.config.normalize_features:
            features = self._normalize_features(features)
        
        return features
    
    def extract_structural_features(self, meme_vector: LegalMemeVector) -> np.ndarray:
        """
        Extract common structural features from legal text.
        
        Args:
            meme_vector: Legal meme vector to extract features from
            
        Returns:
            Structural feature array
        """
        text = meme_vector.text
        features = []
        
        # Basic text statistics
        features.extend([
            len(text),                          # Text length
            len(text.split()),                  # Word count
            len(text.split('.')),               # Sentence count
            text.count('('),                    # Parentheses count
            text.count('['),                    # Bracket count
            text.count(';'),                    # Semicolon count
            text.count(','),                    # Comma count
        ])
        
        # Legal document structure
        features.extend([
            len(self._find_pattern_matches('section_reference', text)),
            len(self._find_pattern_matches('article_reference', text)),
            len(self._find_pattern_matches('paragraph_reference', text)),
            len(self._find_pattern_matches('subsection_reference', text)),
        ])
        
        # Complexity indicators
        avg_sentence_length = len(text.split()) / max(1, len(text.split('.')))
        features.append(avg_sentence_length)
        
        # Legal formality indicators
        formal_terms = ['whereas', 'hereby', 'herein', 'thereof', 'pursuant']
        formal_count = sum(1 for term in formal_terms if term.lower() in text.lower())
        features.append(formal_count)
        
        # Cross-reference density
        total_references = sum([
            len(self._find_pattern_matches('section_reference', text)),
            len(self._find_pattern_matches('article_reference', text)),
            text.lower().count('see also'),
            text.lower().count('pursuant to')
        ])
        reference_density = total_references / max(1, len(text.split())) * 1000
        features.append(reference_density)
        
        return np.array(features, dtype=np.float64)
    
    def extract_semantic_features(self, meme_vector: LegalMemeVector) -> np.ndarray:
        """
        Extract semantic features using simple text analysis.
        
        In production, this would use transformer models.
        
        Args:
            meme_vector: Legal meme vector to extract features from
            
        Returns:
            Semantic feature array
        """
        text = meme_vector.text.lower()
        
        # Legal concept categories
        concept_categories = {
            'prohibition': ['shall not', 'prohibited', 'forbidden', 'unlawful', 'illegal'],
            'obligation': ['shall', 'must', 'required', 'obligated', 'duty'],
            'permission': ['may', 'permitted', 'allowed', 'authorized'],
            'penalty': ['fine', 'penalty', 'punishment', 'sanction', 'imprisonment'],
            'procedure': ['procedure', 'process', 'method', 'steps', 'requirements'],
            'enforcement': ['enforce', 'compliance', 'monitoring', 'investigation'],
            'exemption': ['except', 'unless', 'exemption', 'exclusion', 'provided'],
            'definition': ['means', 'defined', 'definition', 'refers to'],
        }
        
        features = []
        
        for category, keywords in concept_categories.items():
            category_score = sum(1 for keyword in keywords if keyword in text)
            # Normalize by text length
            normalized_score = category_score / max(1, len(text.split())) * 1000
            features.append(normalized_score)
        
        # Legal document type indicators
        doc_type_indicators = {
            'statute': ['statute', 'act', 'code', 'law'],
            'regulation': ['regulation', 'rule', 'order', 'directive'],
            'contract': ['agreement', 'contract', 'covenant', 'undertaking'],
            'policy': ['policy', 'guideline', 'principle', 'standard']
        }
        
        for doc_type, keywords in doc_type_indicators.items():
            type_score = sum(1 for keyword in keywords if keyword in text)
            features.append(min(1.0, type_score))  # Binary indicator
        
        return np.array(features, dtype=np.float64)
    
    def _find_pattern_matches(self, pattern_name: str, text: str) -> List[str]:
        """
        Find all matches for a compiled regex pattern.
        
        Args:
            pattern_name: Name of the pattern to search for
            text: Text to search in
            
        Returns:
            List of matches
        """
        if pattern_name not in self._compiled_patterns:
            return []
        
        pattern = self._compiled_patterns[pattern_name]
        return pattern.findall(text)
    
    def _normalize_features(self, features: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Normalize feature arrays to [0, 1] range.
        
        Args:
            features: Dictionary of feature arrays
            
        Returns:
            Dictionary of normalized feature arrays
        """
        normalized = {}
        
        for feature_type, feature_array in features.items():
            if len(feature_array) == 0:
                normalized[feature_type] = feature_array
                continue
            
            # Min-max normalization
            min_val = np.min(feature_array)
            max_val = np.max(feature_array)
            
            if max_val > min_val:
                normalized_array = (feature_array - min_val) / (max_val - min_val)
            else:
                normalized_array = np.zeros_like(feature_array)
            
            normalized[feature_type] = normalized_array
        
        return normalized
    
    def extract_monetary_amounts(self, text: str) -> List[float]:
        """
        Extract monetary amounts from text.
        
        Args:
            text: Text to extract from
            
        Returns:
            List of monetary amounts
        """
        matches = self._find_pattern_matches('monetary_amount', text)
        amounts = []
        
        for match in matches:
            # Clean and convert to float
            clean_match = re.sub(r'[^\d.]', '', match)
            try:
                amount = float(clean_match)
                amounts.append(amount)
            except ValueError:
                continue
        
        return amounts
    
    def extract_time_periods(self, text: str) -> List[Tuple[int, str]]:
        """
        Extract time periods from text.
        
        Args:
            text: Text to extract from
            
        Returns:
            List of (number, unit) tuples
        """
        matches = self._find_pattern_matches('time_period', text)
        periods = []
        
        for match in matches:
            # Extract number and unit
            number_match = re.search(r'\d+', match)
            unit_match = re.search(r'(days?|weeks?|months?|years?)', match, re.IGNORECASE)
            
            if number_match and unit_match:
                number = int(number_match.group())
                unit = unit_match.group().lower()
                periods.append((number, unit))
        
        return periods
    
    def calculate_complexity_score(self, meme_vector: LegalMemeVector) -> float:
        """
        Calculate overall complexity score for the legal text.
        
        Args:
            meme_vector: Legal meme vector to analyze
            
        Returns:
            Complexity score [0, 1]
        """
        text = meme_vector.text
        
        # Various complexity indicators
        word_count = len(text.split())
        sentence_count = len(text.split('.'))
        avg_sentence_length = word_count / max(1, sentence_count)
        
        # Nested structure complexity
        nesting_score = (text.count('(') + text.count('[')) / max(1, word_count) * 100
        
        # Legal jargon density
        jargon_terms = [
            'whereas', 'hereby', 'herein', 'thereof', 'pursuant', 'notwithstanding',
            'aforementioned', 'heretofore', 'hereunder', 'therein', 'thereto'
        ]
        jargon_count = sum(1 for term in jargon_terms if term.lower() in text.lower())
        jargon_density = jargon_count / max(1, word_count) * 100
        
        # Cross-reference complexity
        ref_count = sum([
            len(self._find_pattern_matches('section_reference', text)),
            len(self._find_pattern_matches('article_reference', text)),
            text.lower().count('see also')
        ])
        ref_density = ref_count / max(1, word_count) * 100
        
        # Combine factors
        complexity_factors = [
            min(1.0, avg_sentence_length / 30.0),  # Normalize by reasonable max
            min(1.0, nesting_score / 10.0),
            min(1.0, jargon_density / 5.0),
            min(1.0, ref_density / 5.0)
        ]
        
        complexity_score = np.mean(complexity_factors)
        
        return complexity_score
    
    def validate_extraction(self, features: Dict[str, np.ndarray]) -> bool:
        """
        Validate that the extracted features are reasonable.
        
        Args:
            features: Dictionary of extracted features
            
        Returns:
            True if validation passes
        """
        for feature_type, feature_array in features.items():
            # Check for NaN or infinite values
            if np.any(np.isnan(feature_array)) or np.any(np.isinf(feature_array)):
                logger.warning(f"Invalid values found in {feature_type} features")
                return False
            
            # Check for reasonable ranges
            if np.any(feature_array < 0):
                logger.warning(f"Negative values found in {feature_type} features")
                # This might be acceptable for some features, so just warn
        
        return True
    
    def get_extraction_metadata(self, meme_vector: LegalMemeVector) -> Dict[str, Any]:
        """
        Get metadata about the extraction process.
        
        Args:
            meme_vector: Legal meme vector that was processed
            
        Returns:
            Dictionary with extraction metadata
        """
        return {
            'extractor_class': self.__class__.__name__,
            'extraction_timestamp': datetime.now().isoformat(),
            'text_length': len(meme_vector.text),
            'word_count': len(meme_vector.text.split()),
            'complexity_score': self.calculate_complexity_score(meme_vector),
            'config': {
                'include_structural': self.config.include_structural,
                'include_semantic': self.config.include_semantic,
                'include_domain_specific': self.config.include_domain_specific,
                'normalize_features': self.config.normalize_features
            }
        }