"""
Legal Text Processing Utilities

This module provides utilities for processing and cleaning legal texts
before feature extraction in the Legal Memespace framework.

Author: Ignacio Adrián Lerer
"""

import re
import string
from typing import List, Dict, Optional, Tuple, Set
import unicodedata
import logging

logger = logging.getLogger(__name__)


class LegalTextProcessor:
    """
    Utility class for processing legal text documents.
    
    Provides methods for cleaning, normalizing, and preprocessing
    legal texts to improve feature extraction accuracy.
    """
    
    def __init__(self, 
                 preserve_structure: bool = True,
                 normalize_unicode: bool = True,
                 remove_citations: bool = False):
        """
        Initialize the text processor.
        
        Args:
            preserve_structure: Whether to preserve legal document structure
            normalize_unicode: Whether to normalize Unicode characters
            remove_citations: Whether to remove legal citations
        """
        self.preserve_structure = preserve_structure
        self.normalize_unicode = normalize_unicode
        self.remove_citations = remove_citations
        
        # Common legal abbreviations and their expansions
        self.legal_abbreviations = {
            'corp.': 'corporation',
            'inc.': 'incorporated',
            'ltd.': 'limited',
            'llc': 'limited liability company',
            'sec.': 'section',
            'para.': 'paragraph',
            'art.': 'article',
            'ch.': 'chapter',
            'pt.': 'part',
            'subd.': 'subdivision',
            'cl.': 'clause',
            'subcl.': 'subclause',
            'u.s.c.': 'united states code',
            'c.f.r.': 'code of federal regulations',
            'fed. reg.': 'federal register',
            'stat.': 'statutes',
            'pub. l.': 'public law',
            'sess.': 'session',
            'cong.': 'congress',
            'h.r.': 'house resolution',
            's.': 'senate',
            'et seq.': 'and following',
            'et al.': 'and others',
            'ibid.': 'in the same place',
            'id.': 'the same',
            'supra': 'above',
            'infra': 'below',
            'cf.': 'compare',
            'e.g.': 'for example',
            'i.e.': 'that is',
            'viz.': 'namely',
            'n.b.': 'note well',
            'q.v.': 'which see',
            'v.': 'versus',
            'vs.': 'versus'
        }
        
        # Patterns for legal structure elements
        self.structure_patterns = {
            'section_header': re.compile(r'^§\s*\d+(?:\.\d+)*\.?\s*', re.MULTILINE),
            'article_header': re.compile(r'^Article\s+[IVXLCDM]+\.?\s*', re.MULTILINE | re.IGNORECASE),
            'chapter_header': re.compile(r'^Chapter\s+\d+\.?\s*', re.MULTILINE | re.IGNORECASE),
            'part_header': re.compile(r'^Part\s+[IVXLCDM]+\.?\s*', re.MULTILINE | re.IGNORECASE),
            'subsection': re.compile(r'^\([a-z]\)\s*', re.MULTILINE),
            'paragraph': re.compile(r'^\(\d+\)\s*', re.MULTILINE),
            'clause': re.compile(r'^\([ivxlc]+\)\s*', re.MULTILINE),
        }
        
        # Citation patterns
        self.citation_patterns = [
            re.compile(r'\d+\s+U\.S\.C\.?\s*§\s*\d+(?:\([^)]+\))?'),  # USC citations
            re.compile(r'\d+\s+C\.F\.R\.?\s*§\s*\d+(?:\.\d+)*'),       # CFR citations
            re.compile(r'\d+\s+Fed\.?\s+Reg\.?\s+\d+'),                 # Federal Register
            re.compile(r'\d+\s+Stat\.?\s+\d+'),                         # Statutes at Large
            re.compile(r'Pub\.?\s+L\.?\s+No\.?\s+\d+-\d+'),            # Public Law
            re.compile(r'\d+\s+[A-Z][a-z]+\.?\s+\d+(?:\s*\(\d+\))?'),  # Case citations
        ]
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize legal text.
        
        Args:
            text: Raw legal text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        cleaned = text
        
        # Normalize Unicode characters
        if self.normalize_unicode:
            cleaned = unicodedata.normalize('NFKD', cleaned)
        
        # Remove or replace special characters that may interfere with processing
        cleaned = self._fix_encoding_issues(cleaned)
        
        # Expand legal abbreviations
        cleaned = self._expand_abbreviations(cleaned)
        
        # Remove citations if requested
        if self.remove_citations:
            cleaned = self._remove_citations(cleaned)
        
        # Clean up whitespace
        cleaned = self._normalize_whitespace(cleaned)
        
        # Preserve legal structure markers if requested
        if self.preserve_structure:
            cleaned = self._preserve_structure_markers(cleaned)
        
        return cleaned
    
    def _fix_encoding_issues(self, text: str) -> str:
        """Fix common encoding issues in legal texts."""
        # Common encoding fixes
        fixes = {
            '–': '-',      # En dash to hyphen
            '—': '--',     # Em dash to double hyphen
            ''': "'",      # Left single quote
            ''': "'",      # Right single quote
            '"': '"',      # Left double quote
            '"': '"',      # Right double quote
            '…': '...',    # Ellipsis
            '§': 'Section',  # Section symbol (preserve meaning)
            '¶': 'Paragraph',  # Paragraph symbol
        }
        
        for old, new in fixes.items():
            text = text.replace(old, new)
        
        # Remove or replace other problematic Unicode characters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expand legal abbreviations to full forms."""
        expanded = text
        
        for abbrev, expansion in self.legal_abbreviations.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            expanded = re.sub(pattern, expansion, expanded, flags=re.IGNORECASE)
        
        return expanded
    
    def _remove_citations(self, text: str) -> str:
        """Remove legal citations from text."""
        cleaned = text
        
        for pattern in self.citation_patterns:
            cleaned = pattern.sub('', cleaned)
        
        return cleaned
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in text."""
        # Replace multiple whitespace characters with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace from lines
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        
        # Remove empty lines
        lines = [line for line in lines if line]
        
        return '\n'.join(lines)
    
    def _preserve_structure_markers(self, text: str) -> str:
        """Preserve important legal structure markers."""
        # Add special markers for structure elements to preserve them
        # This helps maintain the legal document's hierarchical structure
        
        for element_type, pattern in self.structure_patterns.items():
            # Add markers around structure elements
            def add_marker(match):
                return f"[{element_type.upper()}_START]{match.group()}[{element_type.upper()}_END]"
            
            text = pattern.sub(add_marker, text)
        
        return text
    
    def extract_structure(self, text: str) -> Dict[str, List[str]]:
        """
        Extract structural elements from legal text.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            Dictionary mapping structure types to lists of elements
        """
        structure = {}
        
        for element_type, pattern in self.structure_patterns.items():
            matches = pattern.findall(text)
            structure[element_type] = matches
        
        return structure
    
    def segment_by_structure(self, text: str) -> List[Dict[str, str]]:
        """
        Segment text by legal document structure.
        
        Args:
            text: Legal text to segment
            
        Returns:
            List of text segments with structure information
        """
        segments = []
        
        # Split by major structural elements
        section_pattern = re.compile(r'(§\s*\d+(?:\.\d+)*\.?\s*[^\n]*)', re.MULTILINE)
        
        # Find all sections
        section_matches = list(section_pattern.finditer(text))
        
        if not section_matches:
            # No sections found, return entire text as one segment
            return [{'type': 'full_text', 'content': text, 'identifier': 'full'}]
        
        # Extract content between sections
        for i, match in enumerate(section_matches):
            section_header = match.group(1)
            start_pos = match.end()
            
            # Find end position (start of next section or end of text)
            if i + 1 < len(section_matches):
                end_pos = section_matches[i + 1].start()
            else:
                end_pos = len(text)
            
            section_content = text[start_pos:end_pos].strip()
            
            segments.append({
                'type': 'section',
                'identifier': section_header.strip(),
                'content': section_content,
                'full_text': section_header + ' ' + section_content
            })
        
        return segments
    
    def extract_definitions(self, text: str) -> Dict[str, str]:
        """
        Extract term definitions from legal text.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            Dictionary mapping terms to their definitions
        """
        definitions = {}
        
        # Common definition patterns in legal texts
        definition_patterns = [
            re.compile(r'"([^"]+)"\s+means\s+([^.]+\.)', re.IGNORECASE),
            re.compile(r'the\s+term\s+"([^"]+)"\s+(?:means|includes)\s+([^.]+\.)', re.IGNORECASE),
            re.compile(r'"([^"]+)"\s+(?:shall\s+)?(?:mean|include)\s+([^.]+\.)', re.IGNORECASE),
            re.compile(r'([A-Z][a-zA-Z\s]+)\s+means\s+([^.]+\.)', re.IGNORECASE),
        ]
        
        for pattern in definition_patterns:
            matches = pattern.findall(text)
            for term, definition in matches:
                term = term.strip().lower()
                definition = definition.strip()
                definitions[term] = definition
        
        return definitions
    
    def extract_cross_references(self, text: str) -> List[str]:
        """
        Extract cross-references within the legal document.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            List of cross-references found
        """
        cross_references = []
        
        # Patterns for internal cross-references
        reference_patterns = [
            re.compile(r'see\s+§\s*\d+(?:\.\d+)*', re.IGNORECASE),
            re.compile(r'pursuant\s+to\s+§\s*\d+(?:\.\d+)*', re.IGNORECASE),
            re.compile(r'under\s+§\s*\d+(?:\.\d+)*', re.IGNORECASE),
            re.compile(r'in\s+accordance\s+with\s+§\s*\d+(?:\.\d+)*', re.IGNORECASE),
            re.compile(r'as\s+provided\s+in\s+§\s*\d+(?:\.\d+)*', re.IGNORECASE),
            re.compile(r'see\s+also\s+§\s*\d+(?:\.\d+)*', re.IGNORECASE),
        ]
        
        for pattern in reference_patterns:
            matches = pattern.findall(text)
            cross_references.extend(matches)
        
        return cross_references
    
    def calculate_readability_metrics(self, text: str) -> Dict[str, float]:
        """
        Calculate readability metrics for legal text.
        
        Args:
            text: Legal text to analyze
            
        Returns:
            Dictionary with readability metrics
        """
        # Basic text statistics
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        word_count = len(words)
        sentence_count = len(sentences)
        
        if sentence_count == 0:
            return {'error': 'No sentences found'}
        
        # Average words per sentence
        avg_words_per_sentence = word_count / sentence_count
        
        # Average syllables per word (approximation)
        syllable_count = 0
        for word in words:
            word = word.lower().strip(string.punctuation)
            syllable_count += max(1, len(re.findall(r'[aeiouy]+', word)))
        
        avg_syllables_per_word = syllable_count / max(1, word_count)
        
        # Flesch Reading Ease Score (adapted for legal text)
        flesch_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        
        # Flesch-Kincaid Grade Level
        fk_grade = (0.39 * avg_words_per_sentence) + (11.8 * avg_syllables_per_word) - 15.59
        
        # Legal complexity indicators
        complex_words = [word for word in words if len(word) > 6]
        complex_word_ratio = len(complex_words) / max(1, word_count)
        
        # Legal jargon density
        legal_jargon = [
            'whereas', 'hereby', 'herein', 'thereof', 'pursuant', 'notwithstanding',
            'aforementioned', 'heretofore', 'hereunder', 'therein', 'thereto'
        ]
        
        jargon_count = sum(1 for word in words if word.lower() in legal_jargon)
        jargon_density = jargon_count / max(1, word_count) * 100
        
        return {
            'flesch_reading_ease': max(0, min(100, flesch_score)),
            'flesch_kincaid_grade': max(0, fk_grade),
            'avg_words_per_sentence': avg_words_per_sentence,
            'avg_syllables_per_word': avg_syllables_per_word,
            'complex_word_ratio': complex_word_ratio,
            'jargon_density': jargon_density,
            'word_count': word_count,
            'sentence_count': sentence_count
        }
    
    def extract_key_phrases(self, text: str, max_phrases: int = 20) -> List[Tuple[str, int]]:
        """
        Extract key phrases from legal text.
        
        Args:
            text: Legal text to analyze
            max_phrases: Maximum number of phrases to return
            
        Returns:
            List of (phrase, frequency) tuples
        """
        # Clean text
        cleaned = self.clean_text(text)
        
        # Extract n-grams (2-5 words)
        phrase_counts = {}
        
        words = cleaned.lower().split()
        
        # Generate n-grams
        for n in range(2, 6):  # 2 to 5 word phrases
            for i in range(len(words) - n + 1):
                phrase = ' '.join(words[i:i+n])
                
                # Filter out common phrases and very short phrases
                if (len(phrase) > 10 and 
                    not re.match(r'^(the|and|or|of|in|to|for|with|by|from|as|at|on)\s', phrase) and
                    not re.match(r'\s(the|and|or|of|in|to|for|with|by|from|as|at|on)$', phrase)):
                    
                    phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
        
        # Sort by frequency and return top phrases
        sorted_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_phrases[:max_phrases]
    
    def preprocess_for_similarity(self, text: str) -> str:
        """
        Preprocess text specifically for similarity analysis.
        
        Args:
            text: Raw legal text
            
        Returns:
            Preprocessed text optimized for similarity comparison
        """
        # Apply all cleaning steps
        processed = self.clean_text(text)
        
        # Additional preprocessing for similarity
        processed = processed.lower()
        
        # Remove structure markers that might interfere with similarity
        structure_markers = ['[SECTION_HEADER_START]', '[SECTION_HEADER_END]', 
                           '[ARTICLE_HEADER_START]', '[ARTICLE_HEADER_END]']
        
        for marker in structure_markers:
            processed = processed.replace(marker.lower(), '')
        
        # Standardize legal terminology
        legal_synonyms = {
            'shall not': 'prohibited',
            'is prohibited': 'prohibited', 
            'is forbidden': 'prohibited',
            'must not': 'prohibited',
            'shall': 'must',
            'may not': 'prohibited',
        }
        
        for synonym, standard in legal_synonyms.items():
            processed = processed.replace(synonym, standard)
        
        # Remove excessive punctuation
        processed = re.sub(r'[^\w\s]', ' ', processed)
        
        # Normalize whitespace again
        processed = re.sub(r'\s+', ' ', processed).strip()
        
        return processed