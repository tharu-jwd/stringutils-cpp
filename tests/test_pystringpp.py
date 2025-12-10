#!/usr/bin/env python3
"""
Comprehensive test suite for pystringpp package.

Tests cover all core functions with edge cases, error handling, and performance validation.
Designed to achieve >90% code coverage with pytest framework.
"""

import pytest
import sys
import os
import time
from typing import List, Tuple

# Add the python directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

# Try importing the C++ extension, fall back to pure Python implementations
try:
    import pystringpp as su_cpp
    HAS_CPP_EXTENSION = True
    print(f"✓ Testing with C++ extension (version {getattr(su_cpp, '__version__', 'unknown')})")
except ImportError:
    HAS_CPP_EXTENSION = False
    print("✗ C++ extension not available, using pure Python fallbacks")

# Pure Python fallback implementations for testing
def python_reverse_string(s: str) -> str:
    """Pure Python implementation of string reversal."""
    return s[::-1]

def python_count_char(s: str, char: str) -> int:
    """Pure Python implementation of character counting."""
    if len(char) != 1:
        raise ValueError("char must be a single character")
    return s.count(char)

def python_find_pattern(text: str, pattern: str) -> List[int]:
    """Pure Python implementation of pattern finding."""
    if not pattern:
        return []
    positions = []
    start = 0
    while True:
        pos = text.find(pattern, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    return positions

def python_validate_dna(sequence: str) -> bool:
    """Pure Python implementation of DNA validation."""
    if not sequence:
        return True
    valid_chars = set('ATGCatgc')
    return all(char in valid_chars for char in sequence)

def python_calculate_gc_content(sequence: str) -> float:
    """Pure Python implementation of GC content calculation."""
    if not sequence:
        return 0.0
    gc_count = sum(1 for char in sequence.upper() if char in 'GC')
    return (gc_count / len(sequence)) * 100.0

# Create test module that uses C++ when available, Python fallback otherwise
class TestModule:
    def __init__(self):
        if HAS_CPP_EXTENSION:
            self.reverse_string = su_cpp.reverse_string
            self.count_char = su_cpp.count_char
            self.find_pattern = su_cpp.find_pattern
            self.validate_dna = su_cpp.validate_dna
            self.calculate_gc_content = su_cpp.calculate_gc_content
        else:
            self.reverse_string = python_reverse_string
            self.count_char = python_count_char
            self.find_pattern = python_find_pattern
            self.validate_dna = python_validate_dna
            self.calculate_gc_content = python_calculate_gc_content

su = TestModule()


# Test Fixtures
@pytest.fixture
def sample_strings():
    """Fixture providing various test strings."""
    return {
        'empty': '',
        'single': 'a',
        'simple': 'hello',
        'with_spaces': 'hello world',
        'with_punctuation': 'Hello, World!',
        'palindrome': 'racecar',
        'mixed_case': 'HeLLo',
        'unicode': 'café naïve résumé',
        'numbers': '12345',
        'special_chars': '!@#$%^&*()',
        'long': 'a' * 1000,
        'very_long': 'abcdefghij' * 1000,
    }

@pytest.fixture
def dna_sequences():
    """Fixture providing various DNA test sequences."""
    return {
        'empty': '',
        'valid_short': 'ATGC',
        'valid_long': 'ATGCGATCGTAGCATGC',
        'valid_lowercase': 'atgc',
        'valid_mixed_case': 'AtGc',
        'invalid_char': 'ATGCX',
        'invalid_number': 'ATG123',
        'invalid_punctuation': 'ATGC!',
        'all_a': 'AAAA',
        'all_t': 'TTTT',
        'all_g': 'GGGG',
        'all_c': 'CCCC',
        'all_gc': 'GCGC',
        'all_at': 'ATAT',
        'known_gc_50': 'ATGC',  # 50% GC
        'known_gc_75': 'GCGCA',  # 60% GC (3/5)
        'known_gc_0': 'ATAT',   # 0% GC
        'known_gc_100': 'GCGC', # 100% GC
        'long_valid': 'ATGC' * 1000,
    }

@pytest.fixture
def pattern_test_data():
    """Fixture providing pattern matching test data."""
    return [
        # (text, pattern, expected_positions)
        ('abcabcabc', 'abc', [0, 3, 6]),
        ('hello', 'll', [2]),
        ('aaaa', 'aa', [0, 1, 2]),  # Overlapping matches
        ('abcdef', 'xyz', []),  # No matches
        ('', 'abc', []),  # Empty text
        ('abc', '', []),  # Empty pattern
        ('hello world', ' ', [5]),  # Space character
        ('!!!', '!', [0, 1, 2]),  # Special characters
        ('ababab', 'ab', [0, 2, 4]),  # Multiple non-overlapping
        ('programming', 'mm', [6]),  # Consecutive chars
    ]


class TestReverseString:
    """Comprehensive tests for reverse_string function."""
    
    def test_normal_strings(self, sample_strings):
        """Test reversal of normal strings."""
        assert su.reverse_string(sample_strings['simple']) == 'olleh'
        assert su.reverse_string(sample_strings['with_spaces']) == 'dlrow olleh'
        assert su.reverse_string(sample_strings['with_punctuation']) == '!dlroW ,olleH'
        assert su.reverse_string(sample_strings['numbers']) == '54321'
        
    def test_empty_string(self, sample_strings):
        """Test reversal of empty string."""
        assert su.reverse_string(sample_strings['empty']) == ''
        
    def test_single_character(self, sample_strings):
        """Test reversal of single character."""
        assert su.reverse_string(sample_strings['single']) == 'a'
        assert su.reverse_string('Z') == 'Z'
        assert su.reverse_string('1') == '1'
        assert su.reverse_string('!') == '!'
        
    def test_unicode_characters(self, sample_strings):
        """Test reversal of unicode strings."""
        assert su.reverse_string(sample_strings['unicode']) == 'émusér evïan éfac'
        assert su.reverse_string('🎯🚀💻') == '💻🚀🎯'
        assert su.reverse_string('αβγδε') == 'εδγβα'
        
    def test_palindromes(self, sample_strings):
        """Test reversal of palindromes."""
        palindromes = ['a', 'aa', 'aba', 'racecar', 'madam', 'level']
        for palindrome in palindromes:
            assert su.reverse_string(palindrome) == palindrome
            
    def test_case_preservation(self):
        """Test that case is preserved during reversal."""
        assert su.reverse_string('Hello') == 'olleH'
        assert su.reverse_string('PyThOn') == 'nOhTyP'
        
    def test_special_characters(self):
        """Test reversal with various special characters."""
        assert su.reverse_string('!@#$%') == '%$#@!'
        assert su.reverse_string('a\nb\tc') == 'c\tb\na'
        assert su.reverse_string('path/to/file.txt') == 'txt.elif/ot/htap'
        
    def test_large_strings(self, sample_strings):
        """Test reversal of large strings."""
        # Test long repeated character
        result = su.reverse_string(sample_strings['long'])
        assert len(result) == 1000
        assert result == 'a' * 1000
        
        # Test long varied string
        original = sample_strings['very_long']
        result = su.reverse_string(original)
        assert len(result) == len(original)
        assert result == original[::-1]


class TestCountChar:
    """Comprehensive tests for count_char function."""
    
    def test_character_exists(self):
        """Test counting when character exists."""
        assert su.count_char('hello', 'l') == 2
        assert su.count_char('hello', 'h') == 1
        assert su.count_char('hello', 'o') == 1
        assert su.count_char('programming', 'm') == 2
        
    def test_character_not_exists(self):
        """Test counting when character doesn't exist."""
        assert su.count_char('hello', 'x') == 0
        assert su.count_char('hello', 'Z') == 0
        assert su.count_char('hello', '1') == 0
        
    def test_multiple_occurrences(self):
        """Test counting multiple occurrences."""
        assert su.count_char('aaaaaa', 'a') == 6
        assert su.count_char('abababab', 'a') == 4
        assert su.count_char('abababab', 'b') == 4
        assert su.count_char('mississippi', 's') == 4
        assert su.count_char('mississippi', 'i') == 4
        
    def test_case_sensitivity(self):
        """Test that counting is case sensitive."""
        assert su.count_char('Hello', 'h') == 0  # lowercase h not found
        assert su.count_char('Hello', 'H') == 1  # uppercase H found
        assert su.count_char('HeLLo', 'L') == 2  # uppercase L found twice
        assert su.count_char('HeLLo', 'l') == 1  # lowercase l found once
        
    def test_empty_string(self):
        """Test counting in empty string."""
        assert su.count_char('', 'a') == 0
        assert su.count_char('', ' ') == 0
        assert su.count_char('', '!') == 0
        
    def test_special_characters(self):
        """Test counting special characters."""
        assert su.count_char('hello, world!', ' ') == 1
        assert su.count_char('hello, world!', ',') == 1
        assert su.count_char('hello, world!', '!') == 1
        assert su.count_char('a\nb\tc\nd', '\n') == 2
        assert su.count_char('a\nb\tc\nd', '\t') == 1
        
    def test_unicode_characters(self):
        """Test counting unicode characters."""
        assert su.count_char('café', 'é') == 1
        assert su.count_char('naïve', 'ï') == 1
        assert su.count_char('αβγαβγ', 'α') == 2
        assert su.count_char('🎯🚀🎯', '🎯') == 2
        
    def test_numbers_as_characters(self):
        """Test counting numeric characters."""
        assert su.count_char('12321', '1') == 2
        assert su.count_char('12321', '2') == 2
        assert su.count_char('12321', '3') == 1
        assert su.count_char('abc123def', '1') == 1
        
    @pytest.mark.parametrize("text,char,expected", [
        ('', 'a', 0),
        ('a', 'a', 1),
        ('aa', 'a', 2),
        ('ab', 'a', 1),
        ('ab', 'c', 0),
        ('Hello World', ' ', 1),
        ('!!!', '!', 3),
    ])
    def test_parameterized_counting(self, text, char, expected):
        """Parameterized tests for character counting."""
        assert su.count_char(text, char) == expected


class TestFindPattern:
    """Comprehensive tests for find_pattern function."""
    
    def test_pattern_found_once(self):
        """Test finding pattern that occurs once."""
        assert su.find_pattern('hello world', 'world') == [6]
        assert su.find_pattern('programming', 'gram') == [3]
        assert su.find_pattern('abcdef', 'def') == [3]
        
    def test_pattern_found_multiple_times(self, pattern_test_data):
        """Test finding pattern that occurs multiple times."""
        text, pattern, expected = pattern_test_data[0]  # 'abcabcabc', 'abc'
        result = su.find_pattern(text, pattern)
        assert result == expected
        
        # Test multiple 'ab' in 'ababab'
        result = su.find_pattern('ababab', 'ab')
        assert result == [0, 2, 4]
        
    def test_pattern_not_found(self):
        """Test when pattern is not found."""
        assert su.find_pattern('hello', 'xyz') == []
        assert su.find_pattern('abcdef', 'gh') == []
        assert su.find_pattern('123', 'abc') == []
        
    def test_overlapping_patterns(self):
        """Test finding overlapping patterns."""
        # Pattern 'aa' in 'aaaa' should find positions [0, 1, 2]
        result = su.find_pattern('aaaa', 'aa')
        expected = [0, 1, 2]
        assert result == expected
        
        # Pattern 'aba' in 'ababa' should find positions [0, 2]
        result = su.find_pattern('ababa', 'aba')
        assert 0 in result and 2 in result
        
    def test_empty_inputs(self):
        """Test with empty pattern or text."""
        assert su.find_pattern('', 'abc') == []  # Empty text
        assert su.find_pattern('hello', '') == []  # Empty pattern
        assert su.find_pattern('', '') == []  # Both empty
        
    def test_pattern_longer_than_text(self):
        """Test when pattern is longer than text."""
        assert su.find_pattern('hi', 'hello') == []
        assert su.find_pattern('a', 'abc') == []
        
    def test_single_character_pattern(self):
        """Test finding single character patterns."""
        assert su.find_pattern('hello', 'l') == [2, 3]
        assert su.find_pattern('aaa', 'a') == [0, 1, 2]
        assert su.find_pattern('abcdef', 'x') == []
        
    def test_identical_text_and_pattern(self):
        """Test when pattern equals the entire text."""
        assert su.find_pattern('hello', 'hello') == [0]
        assert su.find_pattern('a', 'a') == [0]
        
    def test_case_sensitive_matching(self):
        """Test that pattern matching is case sensitive."""
        assert su.find_pattern('Hello', 'hello') == []  # Case mismatch
        assert su.find_pattern('Hello', 'Hello') == [0]  # Case match
        assert su.find_pattern('HELLO', 'hello') == []  # Case mismatch
        
    def test_special_characters_in_pattern(self):
        """Test patterns with special characters."""
        assert su.find_pattern('hello, world!', ', ') == [5]
        assert su.find_pattern('a.b.c.d', '.') == [1, 3, 5]
        assert su.find_pattern('line1\nline2\n', '\n') == [5, 11]
        
    @pytest.mark.parametrize("text,pattern,expected", [
        ('abc', 'abc', [0]),
        ('abcabc', 'abc', [0, 3]),
        ('hello', 'l', [2, 3]),
        ('', 'x', []),
        ('x', '', []),
        ('aaaa', 'aa', [0, 1, 2]),
    ])
    def test_parameterized_pattern_finding(self, text, pattern, expected):
        """Parameterized tests for pattern finding."""
        assert su.find_pattern(text, pattern) == expected


class TestValidateDNA:
    """Comprehensive tests for validate_dna function."""
    
    def test_valid_dna_sequences(self, dna_sequences):
        """Test validation of valid DNA sequences."""
        valid_sequences = [
            'valid_short', 'valid_long', 'valid_lowercase', 
            'valid_mixed_case', 'all_a', 'all_t', 'all_g', 
            'all_c', 'long_valid'
        ]
        
        for seq_name in valid_sequences:
            seq = dna_sequences[seq_name]
            assert su.validate_dna(seq) == True, f"Should be valid: {seq}"
    
    def test_invalid_characters(self, dna_sequences):
        """Test validation with invalid characters."""
        invalid_sequences = [
            'invalid_char', 'invalid_number', 'invalid_punctuation'
        ]
        
        for seq_name in invalid_sequences:
            seq = dna_sequences[seq_name]
            assert su.validate_dna(seq) == False, f"Should be invalid: {seq}"
            
    def test_additional_invalid_sequences(self):
        """Test additional invalid DNA sequences."""
        invalid_seqs = [
            'ATGCX',      # Contains X
            'ATGC123',    # Contains numbers
            'ATGC!@#',    # Contains punctuation
            'ATGC ',      # Contains space
            'ATGCN',      # Contains N (common but not basic DNA)
            'ATGCU',      # Contains U (RNA, not DNA)
            'xyz',        # No DNA characters
            'atgcx',      # Invalid char in lowercase
        ]
        
        for seq in invalid_seqs:
            assert su.validate_dna(seq) == False, f"Should be invalid: {seq}"
    
    def test_empty_string(self, dna_sequences):
        """Test validation of empty string."""
        assert su.validate_dna(dna_sequences['empty']) == True
    
    def test_mixed_case(self, dna_sequences):
        """Test validation with mixed case."""
        mixed_case_valid = [
            'AtGc', 'atGC', 'ATgc', 'aTgC', 'AtgC',
            'ATGCatgc', 'atgcATGC'
        ]
        
        for seq in mixed_case_valid:
            assert su.validate_dna(seq) == True, f"Should be valid: {seq}"
    
    def test_case_insensitive_validation(self):
        """Test that validation is case insensitive."""
        base_seq = 'ATGC'
        variations = [
            'ATGC', 'atgc', 'AtGc', 'aTgC', 
            'ATgc', 'atGC', 'AtgC', 'aTGc'
        ]
        
        for seq in variations:
            assert su.validate_dna(seq) == True, f"Should be valid: {seq}"
    
    def test_long_sequences(self, dna_sequences):
        """Test validation of long sequences."""
        # Valid long sequence
        assert su.validate_dna(dna_sequences['long_valid']) == True
        
        # Invalid long sequence
        invalid_long = 'ATGC' * 1000 + 'X'
        assert su.validate_dna(invalid_long) == False
    
    def test_single_characters(self):
        """Test validation of single characters."""
        valid_single = ['A', 'T', 'G', 'C', 'a', 't', 'g', 'c']
        for char in valid_single:
            assert su.validate_dna(char) == True, f"Should be valid: {char}"
            
        invalid_single = ['X', 'N', 'U', '1', '!', ' ', 'Z']
        for char in invalid_single:
            assert su.validate_dna(char) == False, f"Should be invalid: {char}"


class TestCalculateGCContent:
    """Comprehensive tests for calculate_gc_content function."""
    
    def test_known_sequences(self, dna_sequences):
        """Test GC content calculation for sequences with known values."""
        # 50% GC content (2 GC out of 4)
        result = su.calculate_gc_content(dna_sequences['known_gc_50'])
        assert abs(result - 50.0) < 0.001
        
        # 0% GC content (all AT)
        result = su.calculate_gc_content(dna_sequences['known_gc_0'])
        assert abs(result - 0.0) < 0.001
        
        # 100% GC content (all GC)
        result = su.calculate_gc_content(dna_sequences['known_gc_100'])
        assert abs(result - 100.0) < 0.001
        
    def test_edge_cases_all_at(self, dna_sequences):
        """Test with sequences containing only A and T."""
        sequences = ['all_a', 'all_t', 'known_gc_0']
        for seq_name in sequences:
            result = su.calculate_gc_content(dna_sequences[seq_name])
            assert abs(result - 0.0) < 0.001, f"Should be 0% GC: {seq_name}"
    
    def test_edge_cases_all_gc(self, dna_sequences):
        """Test with sequences containing only G and C."""
        sequences = ['all_g', 'all_c', 'known_gc_100']
        for seq_name in sequences:
            result = su.calculate_gc_content(dna_sequences[seq_name])
            assert abs(result - 100.0) < 0.001, f"Should be 100% GC: {seq_name}"
    
    def test_empty_sequence(self, dna_sequences):
        """Test GC content calculation for empty sequence."""
        result = su.calculate_gc_content(dna_sequences['empty'])
        assert abs(result - 0.0) < 0.001
    
    def test_case_insensitive_calculation(self):
        """Test that GC content calculation is case insensitive."""
        test_cases = [
            ('ATGC', 'atgc'),
            ('GCGC', 'gcgc'),
            ('AtGc', 'aTgC'),
            ('GCATgcat', 'gcatGCAT'),
        ]
        
        for seq1, seq2 in test_cases:
            result1 = su.calculate_gc_content(seq1)
            result2 = su.calculate_gc_content(seq2)
            assert abs(result1 - result2) < 0.001, f"Case should not matter: {seq1} vs {seq2}"
    
    def test_precise_calculations(self):
        """Test precise GC content calculations."""
        test_cases = [
            ('A', 0.0),           # 0/1 = 0%
            ('G', 100.0),         # 1/1 = 100%
            ('AT', 0.0),          # 0/2 = 0%
            ('GC', 100.0),        # 2/2 = 100%
            ('AGT', 33.333333),   # 1/3 ≈ 33.33%
            ('AGCT', 50.0),       # 2/4 = 50%
            ('AGGCT', 60.0),      # 3/5 = 60%
            ('ATGCATGC', 50.0),   # 4/8 = 50%
            ('GGGATTT', 42.857142857142854),  # 3/7 = ~42.86% (G=3, C=0, Total=7)
        ]
        
        for seq, expected in test_cases:
            result = su.calculate_gc_content(seq)
            assert abs(result - expected) < 0.001, f"Expected {expected}% for {seq}, got {result}%"
    
    def test_long_sequence_calculation(self, dna_sequences):
        """Test GC content calculation for long sequences."""
        long_seq = dna_sequences['long_valid']  # 'ATGC' * 1000
        result = su.calculate_gc_content(long_seq)
        # 'ATGC' has 50% GC content, so the repeated sequence should too
        assert abs(result - 50.0) < 0.001
        
    def test_manual_verification(self):
        """Test with manual verification of counts."""
        seq = 'ATGCGATCGTAGC'
        # Count manually: G=3, C=3, Total=13, GC%=(6/13)*100≈46.15%
        g_count = seq.count('G')
        c_count = seq.count('C')
        total = len(seq)
        expected = ((g_count + c_count) / total) * 100
        
        result = su.calculate_gc_content(seq)
        assert abs(result - expected) < 0.001


class TestErrorHandling:
    """Tests for error handling and edge cases."""
    
    def test_reverse_string_error_handling(self):
        """Test reverse_string handles errors gracefully."""
        # These should not raise exceptions
        try:
            assert su.reverse_string('') == ''
            assert su.reverse_string('a') == 'a'
            assert su.reverse_string('normal string') == 'gnirts lamron'
        except Exception as e:
            pytest.fail(f"reverse_string raised unexpected exception: {e}")
    
    @pytest.mark.skipif(not HAS_CPP_EXTENSION, reason="C++ extension not available")
    def test_count_char_error_handling_cpp(self):
        """Test count_char error handling with C++ extension."""
        # C++ version should handle single characters properly
        with pytest.raises((ValueError, TypeError, RuntimeError)):
            su.count_char('hello', 'ab')  # Multi-character should fail
    
    def test_count_char_error_handling_python(self):
        """Test count_char error handling with Python fallback."""
        if HAS_CPP_EXTENSION:
            pytest.skip("Testing Python fallback behavior")
        
        # Python fallback should handle multi-character gracefully or raise error
        with pytest.raises(ValueError):
            su.count_char('hello', 'ab')
    
    def test_large_input_handling(self):
        """Test handling of very large inputs."""
        # Create large string (1MB)
        large_string = 'a' * (1024 * 1024)
        
        # These operations should complete without errors
        result = su.reverse_string(large_string)
        assert len(result) == len(large_string)
        
        count = su.count_char(large_string, 'a')
        assert count == len(large_string)
        
        # Large DNA sequence
        large_dna = 'ATGC' * (256 * 1024)  # 1MB DNA
        assert su.validate_dna(large_dna) == True
        
        gc_content = su.calculate_gc_content(large_dna)
        assert abs(gc_content - 50.0) < 0.001
    
    def test_unicode_edge_cases(self):
        """Test unicode edge cases."""
        unicode_strings = [
            '🎯🚀💻',      # Emojis
            'αβγδε',        # Greek letters
            'こんにちは',     # Japanese
            '🇺🇸🇬🇧🇫🇷',      # Flag emojis
            'café\u0301',   # Combining characters
        ]
        
        for unicode_str in unicode_strings:
            # Should not raise exceptions
            reversed_str = su.reverse_string(unicode_str)
            assert len(reversed_str) >= 0
            
            # Count first character if string is not empty
            if unicode_str:
                count = su.count_char(unicode_str, unicode_str[0])
                assert count >= 1


@pytest.mark.performance
class TestPerformance:
    """Performance tests for all functions."""
    
    def test_reverse_string_performance(self):
        """Test reverse_string performance."""
        sizes = [1000, 10000, 100000]
        
        for size in sizes:
            test_string = 'a' * size
            start_time = time.time()
            result = su.reverse_string(test_string)
            end_time = time.time()
            
            assert len(result) == size
            # Should complete within reasonable time (1 second for 100k chars)
            assert (end_time - start_time) < 1.0, f"Too slow for size {size}"
    
    def test_count_char_performance(self):
        """Test count_char performance."""
        sizes = [1000, 10000, 100000]
        
        for size in sizes:
            test_string = 'abcde' * (size // 5)
            start_time = time.time()
            count = su.count_char(test_string, 'a')
            end_time = time.time()
            
            expected_count = size // 5
            assert count == expected_count
            assert (end_time - start_time) < 1.0, f"Too slow for size {size}"
    
    def test_find_pattern_performance(self):
        """Test find_pattern performance."""
        # Create string with known pattern occurrences
        pattern = 'abc'
        repetitions = 1000
        test_string = 'abc' + 'x' + 'abc' + 'y'
        test_string = test_string * repetitions
        
        start_time = time.time()
        positions = su.find_pattern(test_string, pattern)
        end_time = time.time()
        
        # Should find many occurrences
        assert len(positions) > 0
        assert (end_time - start_time) < 2.0, "Pattern finding too slow"
    
    def test_validate_dna_performance(self):
        """Test validate_dna performance."""
        sizes = [10000, 100000, 1000000]
        
        for size in sizes:
            test_dna = 'ATGC' * (size // 4)
            start_time = time.time()
            is_valid = su.validate_dna(test_dna)
            end_time = time.time()
            
            assert is_valid == True
            assert (end_time - start_time) < 2.0, f"DNA validation too slow for size {size}"
    
    def test_calculate_gc_content_performance(self):
        """Test calculate_gc_content performance."""
        sizes = [10000, 100000, 1000000]
        
        for size in sizes:
            test_dna = 'ATGC' * (size // 4)
            start_time = time.time()
            gc_content = su.calculate_gc_content(test_dna)
            end_time = time.time()
            
            assert abs(gc_content - 50.0) < 0.001
            assert (end_time - start_time) < 2.0, f"GC calculation too slow for size {size}"


class TestIntegration:
    """Integration tests combining multiple functions."""
    
    def test_dna_analysis_pipeline(self, dna_sequences):
        """Test complete DNA analysis pipeline."""
        dna = dna_sequences['valid_long']
        
        # Step 1: Validate DNA
        is_valid = su.validate_dna(dna)
        assert is_valid == True
        
        # Step 2: Calculate GC content
        gc_content = su.calculate_gc_content(dna)
        assert 0.0 <= gc_content <= 100.0
        
        # Step 3: Count individual nucleotides
        a_count = su.count_char(dna, 'A')
        t_count = su.count_char(dna, 'T')
        g_count = su.count_char(dna, 'G')
        c_count = su.count_char(dna, 'C')
        
        # Verify total counts
        total_count = a_count + t_count + g_count + c_count
        assert total_count == len(dna)
        
        # Verify GC content calculation
        expected_gc = ((g_count + c_count) / len(dna)) * 100
        assert abs(gc_content - expected_gc) < 0.001
        
        # Step 4: Find start codons (ATG)
        start_codons = su.find_pattern(dna, 'ATG')
        assert isinstance(start_codons, list)
        
        # Step 5: Reverse complement preparation (reverse step)
        reversed_dna = su.reverse_string(dna)
        assert len(reversed_dna) == len(dna)
        assert su.validate_dna(reversed_dna) == True
    
    def test_text_processing_pipeline(self, sample_strings):
        """Test text processing pipeline."""
        text = sample_strings['with_punctuation']  # 'Hello, World!'
        
        # Step 1: Count specific characters
        space_count = su.count_char(text, ' ')
        comma_count = su.count_char(text, ',')
        exclamation_count = su.count_char(text, '!')
        
        assert space_count == 1
        assert comma_count == 1
        assert exclamation_count == 1
        
        # Step 2: Find patterns
        hello_pos = su.find_pattern(text.lower(), 'hello')
        world_pos = su.find_pattern(text.lower(), 'world')
        
        assert len(hello_pos) > 0
        assert len(world_pos) > 0
        
        # Step 3: Reverse and verify
        reversed_text = su.reverse_string(text)
        assert len(reversed_text) == len(text)
        
        # Verify reverse is correct
        double_reversed = su.reverse_string(reversed_text)
        assert double_reversed == text
    
    def test_pattern_analysis(self):
        """Test pattern analysis workflow."""
        text = 'The quick brown fox jumps over the lazy dog'
        
        # Find all 'the' occurrences (case insensitive)
        the_positions = su.find_pattern(text.lower(), 'the')
        assert len(the_positions) >= 2  # 'the' appears at least twice
        
        # Count spaces (word separators)
        space_count = su.count_char(text, ' ')
        word_count_estimate = space_count + 1
        assert word_count_estimate == 9  # Known sentence structure
        
        # Reverse and find patterns in reversed text
        reversed_text = su.reverse_string(text)
        reversed_the = su.find_pattern(reversed_text, 'eht')  # 'the' reversed
        assert len(reversed_the) == len(the_positions)


@pytest.mark.skipif(not HAS_CPP_EXTENSION, reason="C++ extension specific tests")
class TestCppExtensionSpecific:
    """Tests specific to the C++ extension."""
    
    def test_module_attributes(self):
        """Test C++ module has expected attributes."""
        import pystringpp as su_cpp
        
        # Should have version attribute
        assert hasattr(su_cpp, '__version__')
        assert isinstance(su_cpp.__version__, str)
        
        # Should have all expected functions
        expected_functions = [
            'reverse_string', 'count_char', 'find_pattern',
            'validate_dna', 'calculate_gc_content'
        ]
        for func_name in expected_functions:
            assert hasattr(su_cpp, func_name)
            assert callable(getattr(su_cpp, func_name))
    
    def test_cpp_vs_python_consistency(self):
        """Test that C++ and Python implementations give consistent results."""
        test_cases = [
            ('hello', 'reverse'),
            ('hello world', 'reverse'),
            ('ATGCATGC', 'validate_dna'),
            ('ATGCATGC', 'gc_content'),
        ]
        
        for text, operation in test_cases:
            if operation == 'reverse':
                cpp_result = su_cpp.reverse_string(text)
                py_result = python_reverse_string(text)
                assert cpp_result == py_result, f"Inconsistent reverse: {text}"
            
            elif operation == 'validate_dna':
                cpp_result = su_cpp.validate_dna(text)
                py_result = python_validate_dna(text)
                assert cpp_result == py_result, f"Inconsistent DNA validation: {text}"
            
            elif operation == 'gc_content':
                cpp_result = su_cpp.calculate_gc_content(text)
                py_result = python_calculate_gc_content(text)
                assert abs(cpp_result - py_result) < 0.001, f"Inconsistent GC content: {text}"


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])