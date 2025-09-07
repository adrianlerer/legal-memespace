"""
Legal Meme Vector Implementation

This module implements the core LegalMemeVector class that represents
legal concepts as mathematical vectors following the Extended Phenotype
Theory applied to jurisprudence.

Based on the theoretical framework developed by Ignacio Adrián Lerer
applying Dawkins' Extended Phenotype Theory to legal evolution.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LegalContext:
    """Represents the legal and cultural context of a legal meme."""
    
    jurisdiction: str
    legal_family: str  # common_law, civil_law, mixed, religious, etc.
    enactment_date: datetime
    amendment_dates: List[datetime] = field(default_factory=list)
    cultural_indices: Dict[str, float] = field(default_factory=dict)  # Hofstede, etc.
    economic_indices: Dict[str, float] = field(default_factory=dict)  # GDP, HDI, etc.
    corruption_indices: Dict[str, float] = field(default_factory=dict)  # CPI, etc.


@dataclass 
class MemeFeatures:
    """Container for different types of legal meme features."""
    
    structural: np.ndarray = field(default_factory=lambda: np.array([]))
    semantic: np.ndarray = field(default_factory=lambda: np.array([]))
    temporal: np.ndarray = field(default_factory=lambda: np.array([]))
    cultural: np.ndarray = field(default_factory=lambda: np.array([]))
    enforcement: np.ndarray = field(default_factory=lambda: np.array([]))


class LegalMemeVector:
    """
    Core class representing a legal concept as a vector in memetic space.
    
    This implementation follows the Extended Phenotype Theory where legal
    norms act as extended phenotypes of cultural and institutional selection
    pressures, creating observable patterns in legal evolution.
    
    Attributes:
        text (str): Original legal text
        context (LegalContext): Contextual information
        features (MemeFeatures): Extracted feature vectors
        vector (np.ndarray): Consolidated meme vector
        metadata (Dict): Additional metadata
    """
    
    def __init__(
        self,
        text: str,
        context: LegalContext,
        text_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a LegalMemeVector.
        
        Args:
            text: The legal text to analyze
            context: Legal and cultural context
            text_id: Unique identifier for this text
            metadata: Additional metadata
        """
        self.text = text
        self.context = context
        self.text_id = text_id or f"legal_text_{id(self)}"
        self.metadata = metadata or {}
        
        self.features = MemeFeatures()
        self.vector: Optional[np.ndarray] = None
        self._normalized_vector: Optional[np.ndarray] = None
        
        logger.info(f"Initialized LegalMemeVector for {self.text_id}")
    
    def extract_features(
        self,
        include_structural: bool = True,
        include_semantic: bool = True,
        include_temporal: bool = True,
        include_cultural: bool = True,
        include_enforcement: bool = True
    ) -> 'LegalMemeVector':
        """
        Extract all feature types from the legal text.
        
        Args:
            include_structural: Extract structural features
            include_semantic: Extract semantic embeddings
            include_temporal: Extract temporal features
            include_cultural: Extract cultural context features
            include_enforcement: Extract enforcement mechanism features
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Extracting features for {self.text_id}")
        
        if include_structural:
            self.features.structural = self._extract_structural_features()
        
        if include_semantic:
            self.features.semantic = self._extract_semantic_features()
            
        if include_temporal:
            self.features.temporal = self._extract_temporal_features()
            
        if include_cultural:
            self.features.cultural = self._extract_cultural_features()
            
        if include_enforcement:
            self.features.enforcement = self._extract_enforcement_features()
        
        # Consolidate into single vector
        self.vector = self._consolidate_features()
        
        return self
    
    def _extract_structural_features(self) -> np.ndarray:
        """
        Extract structural features from legal text.
        
        These capture the formal structure and linguistic patterns
        that reflect legal drafting traditions and institutional
        characteristics.
        
        Returns:
            Array of structural features
        """
        features = []
        
        # Basic text statistics
        text_lower = self.text.lower()
        features.extend([
            len(self.text),  # Text length
            len(self.text.split()),  # Word count
            len(self.text.split('.')),  # Sentence count
            self.text.count('('),  # Parentheses (complexity indicator)
            self.text.count('['),  # Brackets
            self.text.count(';'),  # Semicolons (legal complexity)
        ])
        
        # Legal structure indicators
        legal_keywords = [
            'shall', 'must', 'may', 'should', 'prohibited', 'forbidden',
            'penalty', 'fine', 'imprisonment', 'violation', 'compliance',
            'section', 'article', 'paragraph', 'subsection', 'clause'
        ]
        
        for keyword in legal_keywords:
            features.append(text_lower.count(keyword))
        
        # Conditional structure indicators
        conditional_words = ['if', 'unless', 'provided', 'except', 'where', 'when']
        for word in conditional_words:
            features.append(text_lower.count(word))
        
        # Reference structure (cross-references)
        features.extend([
            self.text.count('§'),  # Section symbols
            text_lower.count('see also'),  # Cross-references
            text_lower.count('pursuant to'),  # Legal citations
            text_lower.count('in accordance with'),  # Compliance references
        ])
        
        return np.array(features, dtype=np.float64)
    
    def _extract_semantic_features(self) -> np.ndarray:
        """
        Extract semantic embeddings using transformer models.
        
        For production use, this would use sentence-transformers
        to create high-dimensional semantic representations.
        
        Returns:
            Semantic feature vector
        """
        # Placeholder implementation
        # In production, would use:
        # from sentence_transformers import SentenceTransformer
        # model = SentenceTransformer('all-MiniLM-L6-v2')
        # embeddings = model.encode(self.text)
        
        # For now, create a simple bag-of-words style feature
        import hashlib
        
        # Create deterministic "embedding" based on text content
        text_hash = int(hashlib.md5(self.text.encode()).hexdigest(), 16)
        np.random.seed(text_hash % (2**32))  # Ensure reproducibility
        
        # Simulate 384-dimensional embedding (typical for sentence transformers)
        semantic_vector = np.random.normal(0, 1, 384)
        
        return semantic_vector.astype(np.float64)
    
    def _extract_temporal_features(self) -> np.ndarray:
        """
        Extract temporal features related to legal evolution.
        
        Returns:
            Temporal feature vector
        """
        features = []
        
        # Years since enactment
        current_year = datetime.now().year
        enactment_year = self.context.enactment_date.year
        features.append(current_year - enactment_year)
        
        # Amendment frequency
        features.append(len(self.context.amendment_dates))
        
        # Years since last amendment
        if self.context.amendment_dates:
            last_amendment = max(self.context.amendment_dates).year
            features.append(current_year - last_amendment)
        else:
            features.append(current_year - enactment_year)  # Same as enactment
        
        # Decade indicators (one-hot encoding for legal eras)
        decades = [1990, 2000, 2010, 2020]
        for decade in decades:
            features.append(1.0 if enactment_year >= decade else 0.0)
        
        return np.array(features, dtype=np.float64)
    
    def _extract_cultural_features(self) -> np.ndarray:
        """
        Extract cultural context features based on Hofstede indices
        and other cultural measurements.
        
        Returns:
            Cultural feature vector
        """
        features = []
        
        # Hofstede dimensions (if available)
        hofstede_dims = [
            'power_distance', 'individualism', 'masculinity',
            'uncertainty_avoidance', 'long_term_orientation', 'indulgence'
        ]
        
        for dim in hofstede_dims:
            features.append(self.context.cultural_indices.get(dim, 0.0))
        
        # Economic indicators
        economic_indicators = ['gdp_per_capita', 'hdi', 'gini_coefficient']
        for indicator in economic_indicators:
            features.append(self.context.economic_indices.get(indicator, 0.0))
        
        # Corruption indices
        corruption_indicators = ['cpi_score', 'wgi_control_corruption', 'transparency_index']
        for indicator in corruption_indicators:
            features.append(self.context.corruption_indices.get(indicator, 0.0))
        
        # Legal family encoding
        legal_families = ['civil_law', 'common_law', 'mixed', 'religious', 'customary']
        for family in legal_families:
            features.append(1.0 if self.context.legal_family == family else 0.0)
        
        return np.array(features, dtype=np.float64)
    
    def _extract_enforcement_features(self) -> np.ndarray:
        """
        Extract enforcement mechanism features.
        
        Returns:
            Enforcement feature vector
        """
        features = []
        text_lower = self.text.lower()
        
        # Penalty types
        penalty_keywords = {
            'fine': ['fine', 'penalty', 'monetary', 'pecuniary'],
            'imprisonment': ['imprisonment', 'jail', 'prison', 'incarceration'],
            'disqualification': ['disqualification', 'suspension', 'prohibition'],
            'restitution': ['restitution', 'damages', 'compensation', 'disgorgement'],
            'administrative': ['license', 'permit', 'registration', 'authorization']
        }
        
        for penalty_type, keywords in penalty_keywords.items():
            count = sum(text_lower.count(keyword) for keyword in keywords)
            features.append(count)
        
        # Enforcement mechanisms
        enforcement_keywords = [
            'investigation', 'audit', 'inspection', 'monitoring',
            'reporting', 'disclosure', 'compliance program',
            'internal controls', 'due diligence', 'whistleblower'
        ]
        
        for keyword in enforcement_keywords:
            features.append(text_lower.count(keyword))
        
        # Severity indicators
        severity_keywords = [
            'criminal', 'civil', 'administrative', 'regulatory',
            'severe', 'substantial', 'significant', 'material'
        ]
        
        for keyword in severity_keywords:
            features.append(text_lower.count(keyword))
        
        return np.array(features, dtype=np.float64)
    
    def _consolidate_features(self) -> np.ndarray:
        """
        Consolidate all feature vectors into a single meme vector.
        
        Returns:
            Consolidated feature vector
        """
        vectors = []
        
        if self.features.structural.size > 0:
            vectors.append(self.features.structural)
        
        if self.features.semantic.size > 0:
            vectors.append(self.features.semantic)
            
        if self.features.temporal.size > 0:
            vectors.append(self.features.temporal)
            
        if self.features.cultural.size > 0:
            vectors.append(self.features.cultural)
            
        if self.features.enforcement.size > 0:
            vectors.append(self.features.enforcement)
        
        if not vectors:
            raise ValueError("No features extracted")
        
        consolidated = np.concatenate(vectors)
        logger.info(f"Consolidated vector shape: {consolidated.shape}")
        
        return consolidated
    
    def normalize_vector(self) -> np.ndarray:
        """
        Normalize the meme vector using L2 normalization.
        
        Returns:
            Normalized vector
        """
        if self.vector is None:
            raise ValueError("Must extract features before normalization")
        
        norm = np.linalg.norm(self.vector)
        if norm == 0:
            self._normalized_vector = self.vector
        else:
            self._normalized_vector = self.vector / norm
        
        return self._normalized_vector
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Calculate feature importance based on vector magnitudes.
        
        Returns:
            Dictionary mapping feature types to importance scores
        """
        if self.vector is None:
            raise ValueError("Must extract features first")
        
        importance = {}
        idx = 0
        
        for feature_type in ['structural', 'semantic', 'temporal', 'cultural', 'enforcement']:
            feature_array = getattr(self.features, feature_type)
            if feature_array.size > 0:
                feature_portion = self.vector[idx:idx + len(feature_array)]
                importance[feature_type] = np.linalg.norm(feature_portion)
                idx += len(feature_array)
        
        # Normalize importance scores
        total_importance = sum(importance.values())
        if total_importance > 0:
            importance = {k: v / total_importance for k, v in importance.items()}
        
        return importance
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the meme vector to a dictionary representation.
        
        Returns:
            Dictionary representation
        """
        return {
            'text_id': self.text_id,
            'text': self.text,
            'context': {
                'jurisdiction': self.context.jurisdiction,
                'legal_family': self.context.legal_family,
                'enactment_date': self.context.enactment_date.isoformat(),
                'amendment_dates': [d.isoformat() for d in self.context.amendment_dates]
            },
            'vector': self.vector.tolist() if self.vector is not None else None,
            'feature_importance': self.get_feature_importance() if self.vector is not None else None,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LegalMemeVector':
        """
        Create a LegalMemeVector from a dictionary representation.
        
        Args:
            data: Dictionary representation
            
        Returns:
            LegalMemeVector instance
        """
        context = LegalContext(
            jurisdiction=data['context']['jurisdiction'],
            legal_family=data['context']['legal_family'],
            enactment_date=datetime.fromisoformat(data['context']['enactment_date']),
            amendment_dates=[datetime.fromisoformat(d) for d in data['context']['amendment_dates']]
        )
        
        meme_vector = cls(
            text=data['text'],
            context=context,
            text_id=data['text_id'],
            metadata=data.get('metadata')
        )
        
        if data.get('vector'):
            meme_vector.vector = np.array(data['vector'])
        
        return meme_vector
    
    def __repr__(self) -> str:
        return f"LegalMemeVector(text_id='{self.text_id}', jurisdiction='{self.context.jurisdiction}', vector_dim={len(self.vector) if self.vector is not None else None})"