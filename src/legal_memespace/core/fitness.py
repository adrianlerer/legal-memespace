"""
Legal Fitness Analysis Module

This module implements fitness functions for legal memes based on
the Extended Phenotype Theory. Legal fitness is measured by the
survival and replication success of legal norms across jurisdictions
and time periods.

Author: Ignacio Adrián Lerer
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union, Any, Callable
from datetime import datetime, timedelta
import logging
import math
from dataclasses import dataclass
from enum import Enum

from .meme_vector import LegalMemeVector, LegalContext

logger = logging.getLogger(__name__)


class SelectionPressure(Enum):
    """Types of evolutionary selection pressures on legal memes."""
    
    CULTURAL_CONVERGENCE = "cultural_convergence"
    ECONOMIC_EFFICIENCY = "economic_efficiency"
    INSTITUTIONAL_COMPATIBILITY = "institutional_compatibility"
    ENFORCEMENT_EFFECTIVENESS = "enforcement_effectiveness"
    INTERNATIONAL_HARMONIZATION = "international_harmonization"
    DEMOCRATIC_LEGITIMACY = "democratic_legitimacy"


@dataclass
class FitnessMetrics:
    """Container for different fitness measurements."""
    
    survival_fitness: float = 0.0  # How long the meme survives
    replication_fitness: float = 0.0  # How widely the meme spreads
    adaptation_fitness: float = 0.0  # How well meme adapts to new contexts
    enforcement_fitness: float = 0.0  # How effectively enforced
    cultural_fitness: float = 0.0  # How well it fits cultural context
    temporal_fitness: float = 0.0  # How well it maintains relevance over time
    
    overall_fitness: float = 0.0  # Combined fitness score


def calculate_legal_fitness(
    meme: LegalMemeVector,
    reference_population: List[LegalMemeVector],
    fitness_components: Optional[List[str]] = None,
    weights: Optional[Dict[str, float]] = None,
    temporal_window: Optional[timedelta] = None
) -> FitnessMetrics:
    """
    Calculate comprehensive legal fitness for a legal meme.
    
    This implements the core fitness calculation based on Extended
    Phenotype Theory where legal norms compete for survival and
    replication in the legal ecosystem.
    
    Args:
        meme: Target legal meme to evaluate
        reference_population: Population of related legal memes for comparison
        fitness_components: List of fitness components to calculate
        weights: Custom weights for different fitness components
        temporal_window: Time window for fitness calculation
        
    Returns:
        FitnessMetrics object with detailed fitness measurements
    """
    if fitness_components is None:
        fitness_components = [
            'survival', 'replication', 'adaptation', 
            'enforcement', 'cultural', 'temporal'
        ]
    
    if weights is None:
        weights = {
            'survival': 0.2,
            'replication': 0.25,
            'adaptation': 0.15,
            'enforcement': 0.15,
            'cultural': 0.15,
            'temporal': 0.1
        }
    
    metrics = FitnessMetrics()
    
    # Calculate individual fitness components
    if 'survival' in fitness_components:
        metrics.survival_fitness = _calculate_survival_fitness(
            meme, reference_population, temporal_window
        )
    
    if 'replication' in fitness_components:
        metrics.replication_fitness = _calculate_replication_fitness(
            meme, reference_population
        )
    
    if 'adaptation' in fitness_components:
        metrics.adaptation_fitness = _calculate_adaptation_fitness(
            meme, reference_population
        )
    
    if 'enforcement' in fitness_components:
        metrics.enforcement_fitness = _calculate_enforcement_fitness(meme)
    
    if 'cultural' in fitness_components:
        metrics.cultural_fitness = _calculate_cultural_fitness(
            meme, reference_population
        )
    
    if 'temporal' in fitness_components:
        metrics.temporal_fitness = _calculate_temporal_fitness(meme)
    
    # Calculate overall fitness as weighted average
    overall_fitness = 0.0
    total_weight = 0.0
    
    fitness_values = {
        'survival': metrics.survival_fitness,
        'replication': metrics.replication_fitness,
        'adaptation': metrics.adaptation_fitness,
        'enforcement': metrics.enforcement_fitness,
        'cultural': metrics.cultural_fitness,
        'temporal': metrics.temporal_fitness
    }
    
    for component, fitness_value in fitness_values.items():
        if component in weights and component in fitness_components:
            weight = weights[component]
            overall_fitness += weight * fitness_value
            total_weight += weight
    
    if total_weight > 0:
        metrics.overall_fitness = overall_fitness / total_weight
    
    logger.info(f"Calculated fitness for {meme.text_id}: {metrics.overall_fitness:.3f}")
    
    return metrics


def _calculate_survival_fitness(
    meme: LegalMemeVector,
    reference_population: List[LegalMemeVector],
    temporal_window: Optional[timedelta] = None
) -> float:
    """
    Calculate survival fitness based on how long legal memes persist
    without being repealed or significantly amended.
    
    Args:
        meme: Target meme
        reference_population: Population for comparison
        temporal_window: Time window for analysis
        
    Returns:
        Survival fitness score [0, 1]
    """
    current_date = datetime.now()
    enactment_date = meme.context.enactment_date
    
    # Time since enactment
    age_years = (current_date - enactment_date).days / 365.25
    
    # Check for recent amendments (indicates instability)
    amendment_penalty = 0.0
    if meme.context.amendment_dates:
        recent_amendments = [
            d for d in meme.context.amendment_dates
            if (current_date - d).days <= 365  # Within last year
        ]
        amendment_penalty = min(0.5, len(recent_amendments) * 0.1)
    
    # Compare with reference population
    if reference_population:
        ages = []
        for ref_meme in reference_population:
            ref_age = (current_date - ref_meme.context.enactment_date).days / 365.25
            ages.append(ref_age)
        
        if ages:
            # Percentile rank in population
            ages_sorted = sorted(ages + [age_years])
            percentile_rank = ages_sorted.index(age_years) / len(ages_sorted)
        else:
            percentile_rank = 0.5
    else:
        # Use absolute age assessment
        percentile_rank = min(1.0, age_years / 20.0)  # 20 years = mature law
    
    survival_fitness = max(0.0, percentile_rank - amendment_penalty)
    
    return survival_fitness


def _calculate_replication_fitness(
    meme: LegalMemeVector,
    reference_population: List[LegalMemeVector]
) -> float:
    """
    Calculate replication fitness based on how widely a legal meme
    has spread to other jurisdictions.
    
    Args:
        meme: Target meme
        reference_population: Population for comparison
        
    Returns:
        Replication fitness score [0, 1]
    """
    from .similarity import cosine_similarity
    
    # Count similar memes in different jurisdictions
    similar_count = 0
    total_jurisdictions = set()
    
    similarity_threshold = 0.7  # High similarity threshold
    
    for ref_meme in reference_population:
        total_jurisdictions.add(ref_meme.context.jurisdiction)
        
        # Skip same jurisdiction
        if ref_meme.context.jurisdiction == meme.context.jurisdiction:
            continue
        
        # Check similarity
        if (ref_meme.vector is not None and meme.vector is not None):
            similarity = cosine_similarity(meme, ref_meme)
            if similarity >= similarity_threshold:
                similar_count += 1
    
    # Calculate replication rate
    if len(total_jurisdictions) > 1:
        max_possible_replications = len(total_jurisdictions) - 1
        replication_rate = similar_count / max_possible_replications
    else:
        replication_rate = 0.0
    
    return min(1.0, replication_rate)


def _calculate_adaptation_fitness(
    meme: LegalMemeVector,
    reference_population: List[LegalMemeVector]
) -> float:
    """
    Calculate adaptation fitness based on how well a legal meme
    adapts to different cultural and institutional contexts.
    
    Args:
        meme: Target meme
        reference_population: Population for comparison
        
    Returns:
        Adaptation fitness score [0, 1]
    """
    from .similarity import cultural_distance_weighting
    
    adaptations = []
    
    for ref_meme in reference_population:
        # Skip same jurisdiction
        if ref_meme.context.jurisdiction == meme.context.jurisdiction:
            continue
        
        # Calculate cultural distance
        cultural_distance = cultural_distance_weighting(
            meme.context, ref_meme.context
        )
        
        # If similar meme exists in culturally distant context,
        # indicates good adaptation capability
        if (ref_meme.vector is not None and meme.vector is not None):
            from .similarity import cosine_similarity
            similarity = cosine_similarity(meme, ref_meme)
            
            if similarity >= 0.6:  # Moderate similarity threshold
                # Higher cultural distance with maintained similarity = better adaptation
                adaptation_score = cultural_distance * similarity
                adaptations.append(adaptation_score)
    
    if adaptations:
        return min(1.0, np.mean(adaptations))
    else:
        return 0.0


def _calculate_enforcement_fitness(meme: LegalMemeVector) -> float:
    """
    Calculate enforcement fitness based on the strength and
    comprehensiveness of enforcement mechanisms in the legal text.
    
    Args:
        meme: Target meme
        
    Returns:
        Enforcement fitness score [0, 1]
    """
    text_lower = meme.text.lower()
    
    # Enforcement mechanism indicators
    enforcement_indicators = {
        'penalties': ['fine', 'penalty', 'imprisonment', 'sanctions'],
        'investigations': ['investigation', 'audit', 'inspection', 'examination'],
        'monitoring': ['monitoring', 'supervision', 'oversight', 'compliance'],
        'reporting': ['report', 'disclosure', 'notification', 'declaration'],
        'institutions': ['authority', 'agency', 'commission', 'regulator'],
        'procedures': ['procedure', 'process', 'mechanism', 'system']
    }
    
    enforcement_score = 0.0
    max_score = len(enforcement_indicators)
    
    for category, keywords in enforcement_indicators.items():
        category_score = 0.0
        for keyword in keywords:
            if keyword in text_lower:
                category_score = 1.0
                break
        enforcement_score += category_score
    
    # Normalize to [0, 1]
    normalized_score = enforcement_score / max_score if max_score > 0 else 0.0
    
    # Bonus for specific enforcement features
    bonus = 0.0
    
    # Whistleblower protection
    if any(term in text_lower for term in ['whistleblower', 'whistle-blower', 'protection']):
        bonus += 0.1
    
    # Corporate liability
    if any(term in text_lower for term in ['corporate', 'entity', 'organization']):
        bonus += 0.1
    
    # Due diligence requirements
    if any(term in text_lower for term in ['due diligence', 'compliance program', 'internal controls']):
        bonus += 0.1
    
    final_score = min(1.0, normalized_score + bonus)
    
    return final_score


def _calculate_cultural_fitness(
    meme: LegalMemeVector,
    reference_population: List[LegalMemeVector]
) -> float:
    """
    Calculate cultural fitness based on how well a legal meme
    fits within its cultural context.
    
    Args:
        meme: Target meme
        reference_population: Population for comparison
        
    Returns:
        Cultural fitness score [0, 1]
    """
    # Cultural fit indicators from context
    cultural_score = 0.0
    
    # Check if cultural indices are available
    cultural_indices = meme.context.cultural_indices
    if not cultural_indices:
        return 0.5  # Neutral score if no cultural data
    
    # Hofstede dimension analysis
    hofstede_scores = []
    
    # Power distance analysis
    if 'power_distance' in cultural_indices:
        pd_score = cultural_indices['power_distance']
        # High power distance cultures may prefer hierarchical legal structures
        if 'authority' in meme.text.lower() or 'hierarchy' in meme.text.lower():
            hofstede_scores.append(pd_score / 100.0)
        else:
            hofstede_scores.append((100 - pd_score) / 100.0)
    
    # Uncertainty avoidance analysis
    if 'uncertainty_avoidance' in cultural_indices:
        ua_score = cultural_indices['uncertainty_avoidance']
        # High UA cultures prefer detailed, prescriptive laws
        text_complexity = len(meme.text.split()) / 1000.0  # Rough complexity measure
        if ua_score > 70:  # High UA
            hofstede_scores.append(min(1.0, text_complexity))
        else:  # Low UA
            hofstede_scores.append(max(0.0, 1.0 - text_complexity))
    
    if hofstede_scores:
        cultural_score = np.mean(hofstede_scores)
    else:
        cultural_score = 0.5
    
    # Economic context fit
    economic_fit = 0.5
    if meme.context.economic_indices:
        # Higher GDP per capita may correlate with more sophisticated legal frameworks
        gdp_per_capita = meme.context.economic_indices.get('gdp_per_capita', 0)
        if gdp_per_capita > 0:
            # Sophisticated law indicators
            sophisticated_terms = [
                'compliance', 'due diligence', 'risk management',
                'governance', 'transparency', 'accountability'
            ]
            sophistication_count = sum(
                1 for term in sophisticated_terms
                if term in meme.text.lower()
            )
            
            if gdp_per_capita > 30000:  # High-income country
                economic_fit = min(1.0, sophistication_count / len(sophisticated_terms))
            else:  # Lower-income country
                economic_fit = max(0.0, 1.0 - sophistication_count / len(sophisticated_terms))
    
    # Combine cultural and economic fitness
    final_fitness = (cultural_score + economic_fit) / 2.0
    
    return final_fitness


def _calculate_temporal_fitness(meme: LegalMemeVector) -> float:
    """
    Calculate temporal fitness based on how well a legal meme
    maintains relevance over time.
    
    Args:
        meme: Target meme
        
    Returns:
        Temporal fitness score [0, 1]
    """
    current_date = datetime.now()
    enactment_date = meme.context.enactment_date
    
    # Age of the law
    age_years = (current_date - enactment_date).days / 365.25
    
    # Modern legal concepts (indicates forward-looking design)
    modern_concepts = [
        'digital', 'electronic', 'cyber', 'online', 'internet',
        'data protection', 'privacy', 'artificial intelligence',
        'blockchain', 'cryptocurrency', 'cloud computing',
        'sustainable', 'environmental', 'climate', 'green'
    ]
    
    modernity_score = 0.0
    text_lower = meme.text.lower()
    
    for concept in modern_concepts:
        if concept in text_lower:
            modernity_score += 1.0
    
    # Normalize modernity score
    normalized_modernity = min(1.0, modernity_score / 5.0)  # Max 5 modern concepts
    
    # Temporal decay function
    # Laws enacted more recently have higher baseline temporal fitness
    recency_score = math.exp(-age_years / 10.0)  # 10-year half-life
    
    # Amendment frequency (recent amendments suggest ongoing relevance)
    amendment_boost = 0.0
    if meme.context.amendment_dates:
        recent_amendments = [
            d for d in meme.context.amendment_dates
            if (current_date - d).days <= 1095  # Within last 3 years
        ]
        amendment_boost = min(0.3, len(recent_amendments) * 0.1)
    
    # Combine factors
    temporal_fitness = (0.4 * recency_score + 
                       0.4 * normalized_modernity + 
                       0.2 * amendment_boost)
    
    return min(1.0, temporal_fitness)


def evolutionary_pressure(
    population: List[LegalMemeVector],
    pressure_type: SelectionPressure,
    intensity: float = 1.0
) -> List[Tuple[LegalMemeVector, float]]:
    """
    Apply evolutionary pressure to a population of legal memes.
    
    Args:
        population: Population of legal meme vectors
        pressure_type: Type of selection pressure to apply
        intensity: Intensity of selection pressure [0, 1]
        
    Returns:
        List of (meme, fitness_under_pressure) tuples
    """
    results = []
    
    for meme in population:
        if pressure_type == SelectionPressure.CULTURAL_CONVERGENCE:
            # Fitness based on cultural adaptability
            fitness = _calculate_cultural_fitness(meme, population)
        
        elif pressure_type == SelectionPressure.ECONOMIC_EFFICIENCY:
            # Fitness based on economic indicators and enforcement costs
            fitness = _calculate_enforcement_fitness(meme) * 0.6 + \
                     _calculate_cultural_fitness(meme, population) * 0.4
        
        elif pressure_type == SelectionPressure.INSTITUTIONAL_COMPATIBILITY:
            # Fitness based on legal family and institutional alignment
            fitness = _calculate_adaptation_fitness(meme, population)
        
        elif pressure_type == SelectionPressure.ENFORCEMENT_EFFECTIVENESS:
            # Fitness based purely on enforcement mechanisms
            fitness = _calculate_enforcement_fitness(meme)
        
        elif pressure_type == SelectionPressure.INTERNATIONAL_HARMONIZATION:
            # Fitness based on replication success
            fitness = _calculate_replication_fitness(meme, population)
        
        elif pressure_type == SelectionPressure.DEMOCRATIC_LEGITIMACY:
            # Fitness based on temporal relevance and cultural fit
            fitness = (_calculate_temporal_fitness(meme) + 
                      _calculate_cultural_fitness(meme, population)) / 2.0
        
        else:
            raise ValueError(f"Unknown selection pressure: {pressure_type}")
        
        # Apply intensity scaling
        adjusted_fitness = fitness ** intensity
        
        results.append((meme, adjusted_fitness))
    
    # Sort by fitness (descending)
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results


def predict_evolutionary_trajectory(
    meme: LegalMemeVector,
    reference_population: List[LegalMemeVector],
    time_horizon_years: float = 10.0,
    selection_pressures: Optional[List[SelectionPressure]] = None
) -> Dict[str, float]:
    """
    Predict evolutionary trajectory of a legal meme.
    
    Args:
        meme: Target legal meme
        reference_population: Reference population for comparison
        time_horizon_years: Time horizon for prediction
        selection_pressures: List of expected selection pressures
        
    Returns:
        Dictionary with trajectory predictions
    """
    if selection_pressures is None:
        selection_pressures = [
            SelectionPressure.CULTURAL_CONVERGENCE,
            SelectionPressure.INTERNATIONAL_HARMONIZATION
        ]
    
    # Current fitness
    current_fitness = calculate_legal_fitness(meme, reference_population)
    
    # Predicted fitness under various pressures
    pressure_predictions = {}
    
    for pressure in selection_pressures:
        pressure_results = evolutionary_pressure([meme], pressure)
        pressure_fitness = pressure_results[0][1] if pressure_results else 0.0
        pressure_predictions[pressure.value] = pressure_fitness
    
    # Temporal decay prediction
    temporal_decay = math.exp(-time_horizon_years / 15.0)  # 15-year half-life
    
    # Overall trajectory prediction
    avg_pressure_fitness = np.mean(list(pressure_predictions.values()))
    predicted_fitness = (current_fitness.overall_fitness * 0.4 + 
                        avg_pressure_fitness * 0.4 + 
                        temporal_decay * 0.2)
    
    return {
        'current_fitness': current_fitness.overall_fitness,
        'predicted_fitness': predicted_fitness,
        'temporal_decay_factor': temporal_decay,
        'pressure_predictions': pressure_predictions,
        'survival_probability': min(1.0, predicted_fitness)
    }