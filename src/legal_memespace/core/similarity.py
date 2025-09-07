"""
Legal Memetic Similarity Analysis

This module implements similarity measures for legal meme vectors,
incorporating cultural distance weighting and temporal decay functions
based on the Extended Phenotype Theory applied to legal evolution.

Author: Ignacio Adrián Lerer
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Any
from datetime import datetime, timedelta
import logging
from scipy.spatial.distance import cosine as scipy_cosine
from scipy.stats import pearsonr
import math

from .meme_vector import LegalMemeVector, LegalContext

logger = logging.getLogger(__name__)


def cosine_similarity(
    vector_a: Union[np.ndarray, LegalMemeVector],
    vector_b: Union[np.ndarray, LegalMemeVector],
    normalized: bool = True
) -> float:
    """
    Calculate cosine similarity between two legal meme vectors.
    
    Args:
        vector_a: First vector or LegalMemeVector
        vector_b: Second vector or LegalMemeVector
        normalized: Whether to normalize vectors before calculation
        
    Returns:
        Cosine similarity score [0, 1]
    """
    # Extract vectors if LegalMemeVector objects passed
    if isinstance(vector_a, LegalMemeVector):
        if vector_a.vector is None:
            raise ValueError("vector_a must have extracted features")
        vec_a = vector_a.vector
    else:
        vec_a = vector_a
    
    if isinstance(vector_b, LegalMemeVector):
        if vector_b.vector is None:
            raise ValueError("vector_b must have extracted features")
        vec_b = vector_b.vector
    else:
        vec_b = vector_b
    
    # Ensure vectors are numpy arrays
    vec_a = np.asarray(vec_a, dtype=np.float64)
    vec_b = np.asarray(vec_b, dtype=np.float64)
    
    # Check dimension compatibility
    if vec_a.shape != vec_b.shape:
        raise ValueError(f"Vector dimensions don't match: {vec_a.shape} vs {vec_b.shape}")
    
    # Normalize if requested
    if normalized:
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        vec_a = vec_a / norm_a
        vec_b = vec_b / norm_b
    
    # Calculate cosine similarity
    dot_product = np.dot(vec_a, vec_b)
    
    # Clamp to [0, 1] to handle floating point errors
    similarity = max(0.0, min(1.0, dot_product))
    
    return similarity


def euclidean_distance(
    vector_a: Union[np.ndarray, LegalMemeVector],
    vector_b: Union[np.ndarray, LegalMemeVector],
    normalized: bool = True
) -> float:
    """
    Calculate Euclidean distance between two legal meme vectors.
    
    Args:
        vector_a: First vector or LegalMemeVector
        vector_b: Second vector or LegalMemeVector
        normalized: Whether to normalize vectors before calculation
        
    Returns:
        Euclidean distance
    """
    # Extract vectors
    if isinstance(vector_a, LegalMemeVector):
        vec_a = vector_a.vector
    else:
        vec_a = vector_a
    
    if isinstance(vector_b, LegalMemeVector):
        vec_b = vector_b.vector
    else:
        vec_b = vector_b
    
    vec_a = np.asarray(vec_a, dtype=np.float64)
    vec_b = np.asarray(vec_b, dtype=np.float64)
    
    if normalized:
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        
        if norm_a > 0:
            vec_a = vec_a / norm_a
        if norm_b > 0:
            vec_b = vec_b / norm_b
    
    return np.linalg.norm(vec_a - vec_b)


def legal_memetic_distance(
    meme_a: LegalMemeVector,
    meme_b: LegalMemeVector,
    weights: Optional[Dict[str, float]] = None,
    include_cultural: bool = True,
    include_temporal: bool = True
) -> float:
    """
    Calculate comprehensive legal memetic distance incorporating
    cultural and temporal factors.
    
    This implements the core distance measure for the Extended
    Phenotype Theory applied to legal evolution.
    
    Args:
        meme_a: First legal meme vector
        meme_b: Second legal meme vector
        weights: Custom weights for different distance components
        include_cultural: Include cultural distance weighting
        include_temporal: Include temporal decay function
        
    Returns:
        Comprehensive memetic distance [0, ∞)
    """
    if weights is None:
        weights = {
            'cosine': 0.4,
            'cultural': 0.3,
            'temporal': 0.2,
            'structural': 0.1
        }
    
    distances = {}
    
    # Base cosine distance
    cosine_sim = cosine_similarity(meme_a, meme_b)
    distances['cosine'] = 1.0 - cosine_sim  # Convert similarity to distance
    
    # Cultural distance
    if include_cultural:
        distances['cultural'] = cultural_distance_weighting(
            meme_a.context, meme_b.context
        )
    
    # Temporal distance
    if include_temporal:
        distances['temporal'] = temporal_decay_function(
            meme_a.context.enactment_date,
            meme_b.context.enactment_date
        )
    
    # Structural distance (legal family compatibility)
    distances['structural'] = legal_family_distance(
        meme_a.context.legal_family,
        meme_b.context.legal_family
    )
    
    # Weighted combination
    total_distance = 0.0
    total_weight = 0.0
    
    for component, distance in distances.items():
        if component in weights:
            weight = weights[component]
            total_distance += weight * distance
            total_weight += weight
    
    # Normalize by total weight
    if total_weight > 0:
        total_distance /= total_weight
    
    logger.debug(f"Memetic distance components: {distances}")
    
    return total_distance


def cultural_distance_weighting(
    context_a: LegalContext,
    context_b: LegalContext,
    dimensions: Optional[List[str]] = None
) -> float:
    """
    Calculate cultural distance weighting based on Hofstede dimensions
    and other cultural indicators.
    
    Args:
        context_a: First legal context
        context_b: Second legal context
        dimensions: Specific cultural dimensions to consider
        
    Returns:
        Cultural distance [0, 1]
    """
    if dimensions is None:
        dimensions = [
            'power_distance', 'individualism', 'masculinity',
            'uncertainty_avoidance', 'long_term_orientation', 'indulgence'
        ]
    
    distances = []
    
    # Hofstede cultural dimensions
    for dim in dimensions:
        val_a = context_a.cultural_indices.get(dim)
        val_b = context_b.cultural_indices.get(dim)
        
        if val_a is not None and val_b is not None:
            # Normalize to [0, 1] assuming Hofstede scale [0, 100]
            normalized_distance = abs(val_a - val_b) / 100.0
            distances.append(normalized_distance)
    
    # Economic indicators
    economic_dims = ['gdp_per_capita', 'hdi', 'gini_coefficient']
    for dim in economic_dims:
        val_a = context_a.economic_indices.get(dim)
        val_b = context_b.economic_indices.get(dim)
        
        if val_a is not None and val_b is not None:
            # Normalize based on typical ranges
            if dim == 'gdp_per_capita':
                # Log scale for GDP per capita
                if val_a > 0 and val_b > 0:
                    log_diff = abs(math.log10(val_a) - math.log10(val_b))
                    normalized_distance = min(1.0, log_diff / 2.0)  # Max ~2 orders of magnitude
                    distances.append(normalized_distance)
            elif dim == 'hdi':
                # HDI is already [0, 1]
                normalized_distance = abs(val_a - val_b)
                distances.append(normalized_distance)
            elif dim == 'gini_coefficient':
                # Gini is [0, 1]
                normalized_distance = abs(val_a - val_b)
                distances.append(normalized_distance)
    
    # Corruption indices
    corruption_dims = ['cpi_score', 'wgi_control_corruption']
    for dim in corruption_dims:
        val_a = context_a.corruption_indices.get(dim)
        val_b = context_b.corruption_indices.get(dim)
        
        if val_a is not None and val_b is not None:
            if dim == 'cpi_score':
                # CPI is [0, 100]
                normalized_distance = abs(val_a - val_b) / 100.0
                distances.append(normalized_distance)
            elif dim == 'wgi_control_corruption':
                # WGI is approximately [-2.5, 2.5]
                normalized_distance = abs(val_a - val_b) / 5.0
                distances.append(normalized_distance)
    
    # Return average distance if any dimensions available
    if distances:
        return np.mean(distances)
    else:
        # Default moderate distance if no cultural data available
        return 0.5


def temporal_decay_function(
    date_a: datetime,
    date_b: datetime,
    half_life_years: float = 10.0,
    max_distance: float = 1.0
) -> float:
    """
    Calculate temporal decay function for legal evolution.
    
    Based on the assumption that legal memes decay in influence
    over time, with more recent laws having higher similarity
    potential due to shared contemporary influences.
    
    Args:
        date_a: First enactment date
        date_b: Second enactment date
        half_life_years: Half-life for temporal decay in years
        max_distance: Maximum temporal distance
        
    Returns:
        Temporal distance [0, max_distance]
    """
    time_diff = abs((date_a - date_b).days) / 365.25  # Years
    
    # Exponential decay function
    # distance = max_distance * (1 - exp(-λt)) where λ = ln(2)/half_life
    lambda_param = math.log(2) / half_life_years
    distance = max_distance * (1 - math.exp(-lambda_param * time_diff))
    
    return min(distance, max_distance)


def legal_family_distance(
    family_a: str,
    family_b: str,
    distance_matrix: Optional[Dict[Tuple[str, str], float]] = None
) -> float:
    """
    Calculate distance between legal families.
    
    Args:
        family_a: First legal family
        family_b: Second legal family
        distance_matrix: Custom distance matrix between legal families
        
    Returns:
        Legal family distance [0, 1]
    """
    if distance_matrix is None:
        # Default distance matrix based on legal theory
        distance_matrix = {
            ('civil_law', 'civil_law'): 0.0,
            ('common_law', 'common_law'): 0.0,
            ('mixed', 'mixed'): 0.0,
            ('religious', 'religious'): 0.0,
            ('customary', 'customary'): 0.0,
            
            ('civil_law', 'common_law'): 0.6,
            ('common_law', 'civil_law'): 0.6,
            
            ('civil_law', 'mixed'): 0.3,
            ('mixed', 'civil_law'): 0.3,
            ('common_law', 'mixed'): 0.3,
            ('mixed', 'common_law'): 0.3,
            
            ('civil_law', 'religious'): 0.8,
            ('religious', 'civil_law'): 0.8,
            ('common_law', 'religious'): 0.8,
            ('religious', 'common_law'): 0.8,
            
            ('civil_law', 'customary'): 0.9,
            ('customary', 'civil_law'): 0.9,
            ('common_law', 'customary'): 0.9,
            ('customary', 'common_law'): 0.9,
            
            ('mixed', 'religious'): 0.5,
            ('religious', 'mixed'): 0.5,
            ('mixed', 'customary'): 0.7,
            ('customary', 'mixed'): 0.7,
            
            ('religious', 'customary'): 0.4,
            ('customary', 'religious'): 0.4,
        }
    
    key = (family_a, family_b)
    if key in distance_matrix:
        return distance_matrix[key]
    
    # If not in matrix, assume maximum distance
    return 1.0


def calculate_similarity_matrix(
    meme_vectors: List[LegalMemeVector],
    similarity_function: str = 'cosine',
    **kwargs
) -> np.ndarray:
    """
    Calculate pairwise similarity matrix for a list of legal meme vectors.
    
    Args:
        meme_vectors: List of LegalMemeVector objects
        similarity_function: Type of similarity to calculate
        **kwargs: Additional arguments for similarity function
        
    Returns:
        Symmetric similarity matrix
    """
    n = len(meme_vectors)
    similarity_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i, n):
            if i == j:
                similarity_matrix[i, j] = 1.0
            else:
                if similarity_function == 'cosine':
                    sim = cosine_similarity(meme_vectors[i], meme_vectors[j], **kwargs)
                elif similarity_function == 'memetic':
                    # Convert distance to similarity
                    dist = legal_memetic_distance(meme_vectors[i], meme_vectors[j], **kwargs)
                    sim = 1.0 / (1.0 + dist)  # Convert distance to similarity
                else:
                    raise ValueError(f"Unknown similarity function: {similarity_function}")
                
                similarity_matrix[i, j] = sim
                similarity_matrix[j, i] = sim  # Symmetric
    
    return similarity_matrix


def find_most_similar(
    target_meme: LegalMemeVector,
    candidate_memes: List[LegalMemeVector],
    similarity_function: str = 'cosine',
    top_k: int = 5,
    **kwargs
) -> List[Tuple[LegalMemeVector, float]]:
    """
    Find the most similar legal memes to a target meme.
    
    Args:
        target_meme: Target legal meme vector
        candidate_memes: List of candidate meme vectors
        similarity_function: Type of similarity to calculate
        top_k: Number of top similar memes to return
        **kwargs: Additional arguments for similarity function
        
    Returns:
        List of (meme, similarity_score) tuples, sorted by similarity (descending)
    """
    similarities = []
    
    for candidate in candidate_memes:
        if similarity_function == 'cosine':
            sim = cosine_similarity(target_meme, candidate, **kwargs)
        elif similarity_function == 'memetic':
            dist = legal_memetic_distance(target_meme, candidate, **kwargs)
            sim = 1.0 / (1.0 + dist)
        else:
            raise ValueError(f"Unknown similarity function: {similarity_function}")
        
        similarities.append((candidate, sim))
    
    # Sort by similarity (descending) and return top_k
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities[:top_k]


def cluster_memes(
    meme_vectors: List[LegalMemeVector],
    n_clusters: int = 5,
    similarity_function: str = 'cosine',
    clustering_method: str = 'kmeans',
    **kwargs
) -> Dict[int, List[LegalMemeVector]]:
    """
    Cluster legal meme vectors based on similarity.
    
    Args:
        meme_vectors: List of LegalMemeVector objects
        n_clusters: Number of clusters
        similarity_function: Similarity function to use
        clustering_method: Clustering algorithm
        **kwargs: Additional arguments
        
    Returns:
        Dictionary mapping cluster IDs to lists of meme vectors
    """
    # Extract vectors for clustering
    vectors = []
    for meme in meme_vectors:
        if meme.vector is None:
            raise ValueError(f"Meme {meme.text_id} must have extracted features")
        vectors.append(meme.vector)
    
    vectors = np.array(vectors)
    
    if clustering_method == 'kmeans':
        from sklearn.cluster import KMeans
        
        clusterer = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = clusterer.fit_predict(vectors)
    else:
        raise ValueError(f"Unknown clustering method: {clustering_method}")
    
    # Group memes by cluster
    clusters = {}
    for i, label in enumerate(cluster_labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(meme_vectors[i])
    
    return clusters