"""
Tests for legal text extractors.

Author: Ignacio Adrián Lerer
"""

import pytest
import numpy as np
from datetime import datetime

from legal_memespace.core.meme_vector import LegalMemeVector, LegalContext
from legal_memespace.extractors.anticorruption import AntiCorruptionExtractor, AntiCorruptionConfig
from legal_memespace.extractors.base_extractor import BaseLegalExtractor, ExtractionConfig
from legal_memespace.extractors.text_processing import LegalTextProcessor


class TestLegalTextProcessor:
    """Test suite for LegalTextProcessor."""
    
    def test_clean_text_basic(self):
        """Test basic text cleaning functionality."""
        processor = LegalTextProcessor()
        
        # Test Unicode normalization
        text = "§ 123. This is a test – with various characters"
        cleaned = processor.clean_text(text)
        
        assert "Section" in cleaned  # § should be converted
        assert "–" not in cleaned or "-" in cleaned  # En dash handling
        assert len(cleaned) > 0
    
    def test_expand_abbreviations(self):
        """Test legal abbreviation expansion."""
        processor = LegalTextProcessor()
        
        text = "See sec. 123 and art. 456 of the corp. bylaws."
        expanded = processor._expand_abbreviations(text)
        
        assert "section" in expanded.lower()
        assert "article" in expanded.lower() 
        assert "corporation" in expanded.lower()
    
    def test_extract_definitions(self):
        """Test definition extraction."""
        processor = LegalTextProcessor()
        
        text = '"Bribery" means the giving of money to influence an official. The term "corruption" includes bribery and fraud.'
        definitions = processor.extract_definitions(text)
        
        assert "bribery" in definitions
        assert "corruption" in definitions
        assert "giving of money" in definitions["bribery"]
    
    def test_calculate_readability_metrics(self):
        """Test readability calculation."""
        processor = LegalTextProcessor()
        
        text = "This is a simple sentence. This is another sentence with more complex words."
        metrics = processor.calculate_readability_metrics(text)
        
        assert "flesch_reading_ease" in metrics
        assert "flesch_kincaid_grade" in metrics
        assert metrics["word_count"] > 0
        assert metrics["sentence_count"] > 0


class TestAntiCorruptionExtractor:
    """Test suite for AntiCorruptionExtractor."""
    
    @pytest.fixture
    def sample_meme(self):
        """Create a sample legal meme for testing."""
        context = LegalContext(
            jurisdiction="United States",
            legal_family="common_law",
            enactment_date=datetime(1977, 12, 19),
            cultural_indices={
                'power_distance': 40,
                'individualism': 91,
                'uncertainty_avoidance': 46
            }
        )
        
        text = """
        It shall be unlawful for any issuer to make use of interstate commerce 
        corruptly in furtherance of an offer, payment, promise to pay, or 
        authorization of the payment of any money, or offer, gift, promise to 
        give, or authorization of the giving of anything of value to any foreign 
        official for purposes of influencing any act or decision of such foreign 
        official in his official capacity, or inducing such foreign official to 
        do or omit to do any act in violation of the lawful duty of such official, 
        or securing any improper advantage. The penalty for violation shall be 
        imprisonment for not more than five years and a fine of not more than 
        $2,000,000 for corporations. Companies must implement compliance programs 
        and due diligence procedures.
        """
        
        return LegalMemeVector(
            text=text,
            context=context,
            text_id="test_fcpa"
        )
    
    def test_extractor_initialization(self):
        """Test extractor initialization."""
        config = AntiCorruptionConfig(
            include_fcpa_features=True,
            include_uk_bribery_features=True
        )
        
        extractor = AntiCorruptionExtractor(config)
        
        assert extractor.ac_config.include_fcpa_features
        assert extractor.ac_config.include_uk_bribery_features
        assert len(extractor.feature_categories) > 0
    
    def test_extract_prohibition_scope(self, sample_meme):
        """Test prohibition scope feature extraction."""
        extractor = AntiCorruptionExtractor()
        
        features = extractor.extract_prohibition_scope(sample_meme.text)
        
        assert isinstance(features, list)
        assert len(features) > 0
        assert all(isinstance(f, (int, float)) for f in features)
        
        # Should detect bribery/corruption terms
        assert features[0] > 0 or features[1] > 0  # Bribery or corruption density
    
    def test_extract_penalties(self, sample_meme):
        """Test penalty extraction."""
        extractor = AntiCorruptionExtractor()
        
        features = extractor.extract_penalties(sample_meme.text)
        
        assert isinstance(features, list)
        assert len(features) > 0
        
        # Should detect imprisonment and monetary penalties
        prison_terms_count = features[-3]  # Based on feature order
        assert prison_terms_count >= 0
    
    def test_extract_compliance_requirements(self, sample_meme):
        """Test compliance requirements extraction.""" 
        extractor = AntiCorruptionExtractor()
        
        features = extractor.extract_compliance_requirements(sample_meme.text)
        
        assert isinstance(features, list)
        assert len(features) > 0
        
        # Should detect compliance program mentions
        compliance_mentions = features[0]  # First feature is compliance program mentions
        assert compliance_mentions > 0
    
    def test_extract_domain_features(self, sample_meme):
        """Test complete domain feature extraction."""
        extractor = AntiCorruptionExtractor()
        
        features = extractor.extract_domain_features(sample_meme)
        
        assert isinstance(features, np.ndarray)
        assert features.dtype == np.float64
        assert len(features) > 50  # Should have many features
        assert not np.any(np.isnan(features))  # No NaN values
    
    def test_get_feature_names(self):
        """Test feature name retrieval."""
        extractor = AntiCorruptionExtractor()
        
        feature_names = extractor.get_feature_names()
        
        assert isinstance(feature_names, list)
        assert len(feature_names) > 50
        assert "bribery_density" in feature_names
        assert "compliance_program_mentions" in feature_names
        assert "criminal_penalties" in feature_names
    
    def test_analyze_legal_evolution(self, sample_meme):
        """Test legal evolution analysis."""
        extractor = AntiCorruptionExtractor()
        
        # Create a small population
        memes = [sample_meme]
        
        # Extract features first
        for meme in memes:
            meme.extract_features()
        
        analysis = extractor.analyze_legal_evolution(memes)
        
        assert isinstance(analysis, dict)
        assert "evolution_summary" in analysis
        assert analysis["evolution_summary"]["total_laws_analyzed"] == 1
    
    def test_feature_validation(self, sample_meme):
        """Test feature extraction validation."""
        extractor = AntiCorruptionExtractor()
        
        # Extract all features
        all_features = extractor.extract_all_features(sample_meme)
        
        # Validate features
        is_valid = extractor.validate_extraction(all_features)
        
        assert is_valid
        assert "domain" in all_features
        assert isinstance(all_features["domain"], np.ndarray)


class TestBaseExtractor:
    """Test suite for BaseLegalExtractor."""
    
    @pytest.fixture
    def sample_meme(self):
        """Create a sample legal meme for testing."""
        context = LegalContext(
            jurisdiction="Test Jurisdiction",
            legal_family="test_family",
            enactment_date=datetime(2000, 1, 1)
        )
        
        text = "This is a test legal document with § 123 and various legal terms."
        
        return LegalMemeVector(
            text=text,
            context=context,
            text_id="test_meme"
        )
    
    def test_pattern_compilation(self):
        """Test regex pattern compilation."""
        # Create a simple extractor subclass for testing
        class TestExtractor(BaseLegalExtractor):
            def extract_domain_features(self, meme_vector):
                return np.array([1, 2, 3])
            
            def get_feature_names(self):
                return ["test1", "test2", "test3"]
        
        extractor = TestExtractor()
        
        assert len(extractor._compiled_patterns) > 0
        assert "section_reference" in extractor._compiled_patterns
    
    def test_extract_structural_features(self, sample_meme):
        """Test structural feature extraction."""
        class TestExtractor(BaseLegalExtractor):
            def extract_domain_features(self, meme_vector):
                return np.array([])
            
            def get_feature_names(self):
                return []
        
        extractor = TestExtractor()
        features = extractor.extract_structural_features(sample_meme)
        
        assert isinstance(features, np.ndarray)
        assert len(features) > 0
        assert features.dtype == np.float64
    
    def test_complexity_score_calculation(self, sample_meme):
        """Test complexity score calculation.""" 
        class TestExtractor(BaseLegalExtractor):
            def extract_domain_features(self, meme_vector):
                return np.array([])
            
            def get_feature_names(self):
                return []
        
        extractor = TestExtractor()
        complexity = extractor.calculate_complexity_score(sample_meme)
        
        assert isinstance(complexity, float)
        assert 0 <= complexity <= 1
    
    def test_monetary_amount_extraction(self):
        """Test monetary amount extraction."""
        class TestExtractor(BaseLegalExtractor):
            def extract_domain_features(self, meme_vector):
                return np.array([])
            
            def get_feature_names(self):
                return []
        
        extractor = TestExtractor()
        
        text = "The fine shall not exceed $1,000,000 or 2.5 million dollars."
        amounts = extractor.extract_monetary_amounts(text)
        
        assert len(amounts) >= 1
        assert any(amount >= 1000000 for amount in amounts)


if __name__ == "__main__":
    pytest.main([__file__])