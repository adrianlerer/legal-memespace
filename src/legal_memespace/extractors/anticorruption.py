"""
Anti-Corruption Legal Extractor

This module implements specialized feature extraction for anti-corruption
legislation, following the Extended Phenotype Theory applied to legal evolution.
It focuses on key elements that define anti-corruption legal memes.

Author: Ignacio Adrián Lerer
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Set, Any
import re
import logging
from dataclasses import dataclass

from .base_extractor import BaseLegalExtractor, ExtractionConfig
from ..core.meme_vector import LegalMemeVector

logger = logging.getLogger(__name__)


@dataclass
class AntiCorruptionConfig(ExtractionConfig):
    """Configuration specific to anti-corruption feature extraction."""
    
    include_fcpa_features: bool = True
    include_uk_bribery_features: bool = True
    include_sapin_features: bool = True
    include_corporate_liability: bool = True
    include_whistleblower_protection: bool = True
    penalty_weight: float = 1.0
    enforcement_weight: float = 1.0


class AntiCorruptionExtractor(BaseLegalExtractor):
    """
    Specialized extractor for anti-corruption legislation features.
    
    This extractor identifies and quantifies key elements of anti-corruption
    laws that serve as legal memes in the evolutionary framework:
    - Prohibition scope and definitions
    - Corporate liability mechanisms
    - Penalty structures and severity
    - Compliance requirements
    - Enforcement mechanisms
    - Whistleblower protections
    """
    
    def __init__(self, config: Optional[AntiCorruptionConfig] = None):
        """
        Initialize the anti-corruption extractor.
        
        Args:
            config: Anti-corruption specific configuration
        """
        self.ac_config = config or AntiCorruptionConfig()
        
        # Custom patterns for anti-corruption laws
        anticorruption_patterns = {
            # Bribery and corruption terms
            'bribery': r'\bbriber?y\b|\bbribe[sd]?\b|\bkickbacks?\b',
            'corruption': r'\bcorruption\b|\bcorrupt\b|\bcorrupting\b',
            'foreign_official': r'\bforeign\s+(?:public\s+)?officials?\b|\bpublic\s+officials?\b',
            'facilitation_payment': r'\bfacilitation\s+payments?\b|\bgrease\s+payments?\b',
            
            # Corporate liability
            'corporate_entity': r'\bcorporations?\b|\bentit(?:y|ies)\b|\bcompan(?:y|ies)\b|\borganizations?\b',
            'successor_liability': r'\bsuccessor\s+liabilit\b|\bmerger\b|\bacquisition\b',
            'parent_subsidiary': r'\bparent\s+(?:company|corporation)\b|\bsubsidiar(?:y|ies)\b',
            
            # Compliance and due diligence
            'compliance_program': r'\bcompliance\s+(?:program|system|procedures?)\b',
            'due_diligence': r'\bdue\s+diligence\b|\brisk\s+assessment\b',
            'internal_controls': r'\binternal\s+controls?\b|\baccounting\s+controls?\b',
            'training': r'\btraining\b|\beducation\b|\baware?ness\b',
            'monitoring': r'\bmonitoring\b|\bsupervision\b|\boversight\b',
            'auditing': r'\baud(?:it|iting)\b|\breview\b|\binspection\b',
            
            # Penalties and sanctions
            'criminal_penalty': r'\bcriminal\s+(?:penalty|sanction|fine)\b|\bimprisonment\b',
            'civil_penalty': r'\bcivil\s+(?:penalty|sanction|fine)\b|\badministrative\s+fine\b',
            'disgorgement': r'\bdisgorgement\b|\brestitution\b|\bforfeiture\b',
            'debarment': r'\bdebarment\b|\bsuspension\b|\bdisqualification\b',
            
            # Enforcement mechanisms
            'investigation': r'\binvestigat(?:e|ion|ing)\b|\benquir(?:y|ies)\b',
            'prosecution': r'\bprosecute\b|\bprosecution\b|\bcharges?\b',
            'cooperation': r'\bcooperat(?:e|ion|ing)\b|\bassist(?:ance)?\b',
            'disclosure': r'\bdisclos(?:e|ure|ing)\b|\breport(?:ing)?\b',
            
            # Whistleblower protection
            'whistleblower': r'\bwhistle-?blower\b|\binformant\b|\breporter\b',
            'protection': r'\bprotection\b|\bprotect(?:ed|ing)?\b',
            'retaliation': r'\bretaliation\b|\breprisal\b|\bretribution\b',
            'anonymity': r'\banonymit[y]\b|\banonymous\b|\bconfidential\b',
            
            # Jurisdictional scope
            'extraterritorial': r'\bextraterritorial\b|\boutside\s+(?:the\s+)?(?:united\s+states|jurisdiction)\b',
            'foreign_commerce': r'\bforeign\s+commerce\b|\binternational\s+trade\b',
            'interstate_commerce': r'\binterstate\s+commerce\b|\bcommerce\s+clause\b',
        }
        
        super().__init__(self.ac_config, anticorruption_patterns)
        
        # Feature categories for anti-corruption laws
        self.feature_categories = [
            'prohibition_scope',
            'corporate_liability', 
            'penalties',
            'compliance_requirements',
            'enforcement_mechanisms',
            'whistleblower_protection',
            'jurisdictional_scope'
        ]
        
        logger.info("Initialized AntiCorruptionExtractor")
    
    def extract_domain_features(self, meme_vector: LegalMemeVector) -> np.ndarray:
        """
        Extract anti-corruption specific features from legal text.
        
        Args:
            meme_vector: Legal meme vector to extract features from
            
        Returns:
            Anti-corruption feature array
        """
        text = meme_vector.text
        features = []
        
        # Extract features for each category
        features.extend(self.extract_prohibition_scope(text))
        features.extend(self.extract_corporate_liability(text))
        features.extend(self.extract_penalties(text))
        features.extend(self.extract_compliance_requirements(text))
        features.extend(self.extract_enforcement_mechanisms(text))
        features.extend(self.extract_whistleblower_protection(text))
        features.extend(self.extract_jurisdictional_scope(text))
        
        return np.array(features, dtype=np.float64)
    
    def extract_prohibition_scope(self, text: str) -> List[float]:
        """
        Extract features related to the scope of prohibited activities.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            List of prohibition scope features
        """
        features = []
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Core prohibition terms
        bribery_count = len(self._find_pattern_matches('bribery', text))
        corruption_count = len(self._find_pattern_matches('corruption', text))
        
        # Normalize by text length
        features.extend([
            bribery_count / max(1, word_count) * 1000,
            corruption_count / max(1, word_count) * 1000
        ])
        
        # Specific prohibited activities
        prohibited_activities = {
            'giving_bribes': ['give', 'offer', 'pay', 'provide', 'transfer'],
            'receiving_bribes': ['receive', 'accept', 'solicit', 'demand'],
            'promising_bribes': ['promise', 'agree', 'commit', 'undertake'],
            'facilitating_corruption': ['facilitate', 'enable', 'assist', 'help']
        }
        
        for activity_type, keywords in prohibited_activities.items():
            # Count co-occurrence with bribery/corruption terms
            activity_score = 0
            for keyword in keywords:
                # Look for keyword near bribery/corruption terms (within 50 words)
                pattern = rf'\b{keyword}\b.{{0,300}}\b(?:brib|corrupt)\b|\b(?:brib|corrupt)\b.{{0,300}}\b{keyword}\b'
                matches = re.findall(pattern, text_lower, re.DOTALL)
                activity_score += len(matches)
            
            features.append(activity_score / max(1, word_count) * 1000)
        
        # Target scope
        target_categories = {
            'foreign_officials': len(self._find_pattern_matches('foreign_official', text)),
            'private_parties': text_lower.count('private') + text_lower.count('commercial'),
            'political_parties': text_lower.count('political party') + text_lower.count('candidate'),
            'facilitation_payments': len(self._find_pattern_matches('facilitation_payment', text))
        }
        
        for category, count in target_categories.items():
            features.append(count / max(1, word_count) * 1000)
        
        # Monetary thresholds (indicates scope precision)
        monetary_amounts = self.extract_monetary_amounts(text)
        features.extend([
            len(monetary_amounts),  # Number of monetary thresholds
            max(monetary_amounts) if monetary_amounts else 0,  # Highest threshold
            min(monetary_amounts) if monetary_amounts else 0   # Lowest threshold
        ])
        
        return features
    
    def extract_corporate_liability(self, text: str) -> List[float]:
        """
        Extract features related to corporate liability mechanisms.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            List of corporate liability features
        """
        features = []
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Corporate entity recognition
        corporate_mentions = len(self._find_pattern_matches('corporate_entity', text))
        features.append(corporate_mentions / max(1, word_count) * 1000)
        
        # Liability standards
        liability_standards = {
            'strict_liability': ['strict liability', 'absolute liability'],
            'vicarious_liability': ['vicarious liability', 'respondeat superior'],
            'negligence_standard': ['negligence', 'reasonable care', 'due care'],
            'knowledge_standard': ['knowledge', 'knew', 'should have known', 'willful blindness']
        }
        
        for standard, keywords in liability_standards.items():
            standard_score = sum(1 for keyword in keywords if keyword in text_lower)
            features.append(standard_score)
        
        # Corporate structure considerations
        structure_elements = {
            'parent_subsidiary': len(self._find_pattern_matches('parent_subsidiary', text)),
            'successor_liability': len(self._find_pattern_matches('successor_liability', text)),
            'joint_ventures': text_lower.count('joint venture') + text_lower.count('partnership'),
            'agents_representatives': text_lower.count('agent') + text_lower.count('representative')
        }
        
        for element, count in structure_elements.items():
            features.append(count / max(1, word_count) * 1000)
        
        # Affirmative defenses
        defense_types = {
            'compliance_defense': 'compliance program',
            'due_diligence_defense': 'due diligence', 
            'good_faith_defense': 'good faith',
            'cooperation_defense': 'cooperation'
        }
        
        for defense_type, keyword in defense_types.items():
            defense_score = 1 if keyword in text_lower else 0
            features.append(defense_score)
        
        return features
    
    def extract_penalties(self, text: str) -> List[float]:
        """
        Extract features related to penalty structures and severity.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            List of penalty features
        """
        features = []
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Penalty types
        penalty_types = {
            'criminal_penalties': len(self._find_pattern_matches('criminal_penalty', text)),
            'civil_penalties': len(self._find_pattern_matches('civil_penalty', text)),
            'disgorgement': len(self._find_pattern_matches('disgorgement', text)),
            'debarment': len(self._find_pattern_matches('debarment', text))
        }
        
        for penalty_type, count in penalty_types.items():
            features.append(count / max(1, word_count) * 1000)
        
        # Penalty severity indicators
        severity_terms = [
            'fine', 'imprisonment', 'prison', 'jail', 'incarceration',
            'felony', 'misdemeanor', 'violation', 'offense'
        ]
        
        total_severity = sum(1 for term in severity_terms if term in text_lower)
        features.append(total_severity / max(1, word_count) * 1000)
        
        # Monetary penalty amounts
        monetary_penalties = []
        
        # Look for specific penalty amounts
        fine_patterns = [
            r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
            r'\b\d{1,3}(?:,\d{3})*\s*dollars?',
            r'\bmillion\s+dollars?\b',
            r'\bbillion\s+dollars?\b'
        ]
        
        for pattern in fine_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            monetary_penalties.extend(matches)
        
        features.extend([
            len(monetary_penalties),  # Number of monetary penalties
            1 if 'million' in text_lower else 0,  # Million-dollar penalties
            1 if 'billion' in text_lower else 0   # Billion-dollar penalties
        ])
        
        # Prison terms
        time_periods = self.extract_time_periods(text)
        prison_years = []
        
        for number, unit in time_periods:
            if 'year' in unit:
                prison_years.append(number)
            elif 'month' in unit:
                prison_years.append(number / 12.0)
        
        features.extend([
            len(prison_years),  # Number of prison terms mentioned
            max(prison_years) if prison_years else 0,  # Maximum prison term
            np.mean(prison_years) if prison_years else 0  # Average prison term
        ])
        
        # Penalty multipliers and enhancements
        multiplier_terms = ['double', 'triple', 'multiple', 'enhanced', 'aggravated']
        multiplier_score = sum(1 for term in multiplier_terms if term in text_lower)
        features.append(multiplier_score)
        
        return features
    
    def extract_compliance_requirements(self, text: str) -> List[float]:
        """
        Extract features related to compliance program requirements.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            List of compliance requirement features
        """
        features = []
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Core compliance elements
        compliance_elements = {
            'compliance_program': len(self._find_pattern_matches('compliance_program', text)),
            'due_diligence': len(self._find_pattern_matches('due_diligence', text)),
            'internal_controls': len(self._find_pattern_matches('internal_controls', text)),
            'training': len(self._find_pattern_matches('training', text)),
            'monitoring': len(self._find_pattern_matches('monitoring', text)),
            'auditing': len(self._find_pattern_matches('auditing', text))
        }
        
        for element, count in compliance_elements.items():
            features.append(count / max(1, word_count) * 1000)
        
        # Compliance program components
        program_components = [
            'risk assessment', 'policies and procedures', 'training and communication',
            'monitoring and auditing', 'reporting system', 'disciplinary measures',
            'periodic review', 'senior management oversight', 'board oversight'
        ]
        
        component_score = sum(1 for component in program_components if component in text_lower)
        features.append(component_score / len(program_components))  # Normalized completeness
        
        # Specific compliance standards
        standards = {
            'iso_37001': 'iso 37001' in text_lower,
            'fcpa_guidance': 'fcpa' in text_lower and 'guidance' in text_lower,
            'uk_guidance': 'bribery act' in text_lower and 'guidance' in text_lower,
            'oecd_standards': 'oecd' in text_lower
        }
        
        for standard, present in standards.items():
            features.append(1.0 if present else 0.0)
        
        # Third party management
        third_party_terms = [
            'third party', 'vendor', 'supplier', 'contractor', 'intermediary',
            'consultant', 'agent', 'distributor', 'business partner'
        ]
        
        third_party_score = sum(1 for term in third_party_terms if term in text_lower)
        features.append(third_party_score / max(1, word_count) * 1000)
        
        return features
    
    def extract_enforcement_mechanisms(self, text: str) -> List[float]:
        """
        Extract features related to enforcement mechanisms and authorities.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            List of enforcement mechanism features
        """
        features = []
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Enforcement authorities
        authorities = [
            'department of justice', 'doj', 'securities and exchange commission', 'sec',
            'serious fraud office', 'sfo', 'financial conduct authority', 'fca',
            'attorney general', 'prosecutor', 'district attorney'
        ]
        
        authority_mentions = sum(1 for authority in authorities if authority in text_lower)
        features.append(authority_mentions)
        
        # Enforcement mechanisms
        mechanisms = {
            'investigation': len(self._find_pattern_matches('investigation', text)),
            'prosecution': len(self._find_pattern_matches('prosecution', text)),
            'cooperation': len(self._find_pattern_matches('cooperation', text)),
            'disclosure': len(self._find_pattern_matches('disclosure', text))
        }
        
        for mechanism, count in mechanisms.items():
            features.append(count / max(1, word_count) * 1000)
        
        # Cooperation incentives
        cooperation_terms = [
            'cooperation agreement', 'deferred prosecution', 'non-prosecution agreement',
            'leniency', 'mitigation', 'reduction', 'credit for cooperation'
        ]
        
        cooperation_score = sum(1 for term in cooperation_terms if term in text_lower)
        features.append(cooperation_score)
        
        # Statute of limitations
        limitations_present = 1 if 'statute of limitations' in text_lower or 'limitation period' in text_lower else 0
        features.append(limitations_present)
        
        # International cooperation
        international_terms = [
            'mutual legal assistance', 'extradition', 'international cooperation',
            'treaty', 'convention', 'multilateral'
        ]
        
        international_score = sum(1 for term in international_terms if term in text_lower)
        features.append(international_score)
        
        return features
    
    def extract_whistleblower_protection(self, text: str) -> List[float]:
        """
        Extract features related to whistleblower protection provisions.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            List of whistleblower protection features
        """
        features = []
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Whistleblower terminology
        whistleblower_terms = len(self._find_pattern_matches('whistleblower', text))
        features.append(whistleblower_terms / max(1, word_count) * 1000)
        
        # Protection mechanisms
        protection_mechanisms = {
            'protection': len(self._find_pattern_matches('protection', text)),
            'anonymity': len(self._find_pattern_matches('anonymity', text)),
            'confidentiality': text_lower.count('confidential'),
            'non_retaliation': text_lower.count('retaliation') + text_lower.count('reprisal')
        }
        
        for mechanism, count in protection_mechanisms.items():
            features.append(count / max(1, word_count) * 1000)
        
        # Reporting channels
        reporting_channels = [
            'hotline', 'helpline', 'reporting system', 'ombudsman',
            'ethics line', 'compliance officer', 'internal reporting'
        ]
        
        channels_score = sum(1 for channel in reporting_channels if channel in text_lower)
        features.append(channels_score)
        
        # Incentives for reporting
        incentive_terms = [
            'reward', 'compensation', 'bounty', 'incentive', 'award'
        ]
        
        incentives_score = sum(1 for term in incentive_terms if term in text_lower)
        features.append(incentives_score)
        
        # Legal remedies for retaliation
        remedy_terms = [
            'reinstatement', 'back pay', 'damages', 'attorney fees', 'injunctive relief'
        ]
        
        remedies_score = sum(1 for term in remedy_terms if term in text_lower)
        features.append(remedies_score)
        
        return features
    
    def extract_jurisdictional_scope(self, text: str) -> List[float]:
        """
        Extract features related to jurisdictional scope and extraterritorial reach.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            List of jurisdictional scope features
        """
        features = []
        text_lower = text.lower()
        word_count = len(text.split())
        
        # Territorial scope
        territorial_indicators = {
            'extraterritorial': len(self._find_pattern_matches('extraterritorial', text)),
            'foreign_commerce': len(self._find_pattern_matches('foreign_commerce', text)),
            'interstate_commerce': len(self._find_pattern_matches('interstate_commerce', text))
        }
        
        for indicator, count in territorial_indicators.items():
            features.append(count / max(1, word_count) * 1000)
        
        # Nexus requirements
        nexus_terms = [
            'nexus', 'connection', 'substantial connection', 'minimum contacts',
            'effects test', 'conduct test', 'territorial nexus'
        ]
        
        nexus_score = sum(1 for term in nexus_terms if term in text_lower)
        features.append(nexus_score)
        
        # International elements
        international_elements = [
            'foreign national', 'foreign entity', 'foreign government',
            'international transaction', 'cross-border', 'transnational'
        ]
        
        international_score = sum(1 for element in international_elements if element in text_lower)
        features.append(international_score)
        
        # Specific geographic references
        geographic_regions = [
            'united states', 'european union', 'asia pacific', 'latin america',
            'africa', 'middle east', 'worldwide', 'global'
        ]
        
        geographic_score = sum(1 for region in geographic_regions if region in text_lower)
        features.append(geographic_score)
        
        return features
    
    def get_feature_names(self) -> List[str]:
        """
        Get comprehensive list of all feature names extracted by this extractor.
        
        Returns:
            List of feature names
        """
        feature_names = []
        
        # Prohibition scope features
        prohibition_features = [
            'bribery_density', 'corruption_density',
            'giving_bribes_score', 'receiving_bribes_score', 
            'promising_bribes_score', 'facilitating_corruption_score',
            'foreign_officials_mentions', 'private_parties_mentions',
            'political_parties_mentions', 'facilitation_payments_mentions',
            'monetary_thresholds_count', 'max_threshold', 'min_threshold'
        ]
        feature_names.extend(prohibition_features)
        
        # Corporate liability features
        liability_features = [
            'corporate_mentions',
            'strict_liability', 'vicarious_liability', 'negligence_standard', 'knowledge_standard',
            'parent_subsidiary_mentions', 'successor_liability_mentions',
            'joint_ventures_mentions', 'agents_representatives_mentions',
            'compliance_defense', 'due_diligence_defense', 'good_faith_defense', 'cooperation_defense'
        ]
        feature_names.extend(liability_features)
        
        # Penalty features
        penalty_features = [
            'criminal_penalties', 'civil_penalties', 'disgorgement_mentions', 'debarment_mentions',
            'severity_score', 'monetary_penalties_count', 'million_dollar_penalties', 'billion_dollar_penalties',
            'prison_terms_count', 'max_prison_term', 'avg_prison_term', 'penalty_multipliers'
        ]
        feature_names.extend(penalty_features)
        
        # Compliance features
        compliance_features = [
            'compliance_program_mentions', 'due_diligence_mentions', 'internal_controls_mentions',
            'training_mentions', 'monitoring_mentions', 'auditing_mentions',
            'program_completeness', 'iso_37001', 'fcpa_guidance', 'uk_guidance', 'oecd_standards',
            'third_party_management'
        ]
        feature_names.extend(compliance_features)
        
        # Enforcement features
        enforcement_features = [
            'authority_mentions', 'investigation_mentions', 'prosecution_mentions',
            'cooperation_mentions', 'disclosure_mentions', 'cooperation_incentives',
            'statute_limitations', 'international_cooperation'
        ]
        feature_names.extend(enforcement_features)
        
        # Whistleblower features
        whistleblower_features = [
            'whistleblower_mentions', 'protection_mentions', 'anonymity_mentions',
            'confidentiality_mentions', 'non_retaliation_mentions', 'reporting_channels',
            'reporting_incentives', 'legal_remedies'
        ]
        feature_names.extend(whistleblower_features)
        
        # Jurisdictional features
        jurisdictional_features = [
            'extraterritorial_mentions', 'foreign_commerce_mentions', 'interstate_commerce_mentions',
            'nexus_requirements', 'international_elements', 'geographic_scope'
        ]
        feature_names.extend(jurisdictional_features)
        
        return feature_names
    
    def analyze_legal_evolution(self, meme_vectors: List[LegalMemeVector]) -> Dict[str, Any]:
        """
        Analyze evolutionary patterns in anti-corruption legislation.
        
        Args:
            meme_vectors: List of anti-corruption legal meme vectors
            
        Returns:
            Dictionary with evolution analysis results
        """
        if not meme_vectors:
            return {}
        
        # Extract features for all memes
        all_features = []
        all_dates = []
        
        for meme in meme_vectors:
            if meme.vector is None:
                meme.extract_features()
            
            # Extract domain-specific features
            ac_features = self.extract_domain_features(meme)
            all_features.append(ac_features)
            all_dates.append(meme.context.enactment_date)
        
        features_array = np.array(all_features)
        
        # Temporal analysis
        sorted_indices = np.argsort(all_dates)
        sorted_features = features_array[sorted_indices]
        sorted_dates = [all_dates[i] for i in sorted_indices]
        
        # Calculate feature evolution trends
        feature_trends = {}
        feature_names = self.get_feature_names()
        
        for i, feature_name in enumerate(feature_names):
            if i < sorted_features.shape[1]:
                feature_values = sorted_features[:, i]
                # Simple linear trend (correlation with time)
                time_indices = np.arange(len(feature_values))
                if len(time_indices) > 1 and np.std(feature_values) > 0:
                    correlation = np.corrcoef(time_indices, feature_values)[0, 1]
                    feature_trends[feature_name] = correlation
        
        # Identify dominant memes (most common features)
        mean_features = np.mean(features_array, axis=0)
        std_features = np.std(features_array, axis=0)
        
        dominant_features = {}
        for i, feature_name in enumerate(feature_names):
            if i < len(mean_features):
                # Features with high mean and low variance are dominant
                if std_features[i] > 0:
                    dominance_score = mean_features[i] / (1 + std_features[i])
                else:
                    dominance_score = mean_features[i]
                dominant_features[feature_name] = dominance_score
        
        # Sort by dominance
        sorted_dominant = sorted(dominant_features.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'feature_trends': feature_trends,
            'dominant_features': dict(sorted_dominant[:10]),  # Top 10
            'evolution_summary': {
                'total_laws_analyzed': len(meme_vectors),
                'date_range': f"{min(all_dates).year} - {max(all_dates).year}",
                'most_evolving_features': sorted(
                    feature_trends.items(), 
                    key=lambda x: abs(x[1]), 
                    reverse=True
                )[:5],
                'average_feature_vector': mean_features.tolist()
            }
        }