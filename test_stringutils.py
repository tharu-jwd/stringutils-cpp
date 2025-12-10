#!/usr/bin/env python3
"""
Test suite for pystring++
"""

def test_functions():
    """Test string processing functions"""
    try:
        import pystring as su
        print("PASS: C++ extension loaded")
    except ImportError:
        print("FAIL: C++ extension not available")
        return False
    
    # Test reverse_string
    assert su.reverse_string("hello") == "olleh"
    assert su.reverse_string("") == ""
    print("PASS: reverse_string tests passed")
    
    # Test count_char
    assert su.count_char("hello", "l") == 2
    assert su.count_char("hello", "x") == 0
    print("PASS: count_char tests passed")
    
    # Test find_pattern
    assert su.find_pattern("abcabc", "abc") == [0, 3]
    assert su.find_pattern("hello", "xyz") == []
    print("PASS: find_pattern tests passed")
    
    return True

def main():
    print("pystring++ Test Suite")
    print("=" * 30)
    
    if test_functions():
        print("\nSUCCESS: All tests passed")
        return True
    else:
        print("\nFAILED: Tests failed")
        return False

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)