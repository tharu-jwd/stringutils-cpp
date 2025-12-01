#!/usr/bin/env python3
"""
Test suite for StringUtils-CPP
"""

def test_functions():
    """Test string processing functions"""
    try:
        import stringutils_cpp as su
        print("✓ C++ extension loaded")
    except ImportError:
        print("✗ C++ extension not available")
        return False
    
    # Test reverse_string
    assert su.reverse_string("hello") == "olleh"
    assert su.reverse_string("") == ""
    print("✓ reverse_string tests passed")
    
    # Test count_char
    assert su.count_char("hello", "l") == 2
    assert su.count_char("hello", "x") == 0
    print("✓ count_char tests passed")
    
    # Test find_pattern
    assert su.find_pattern("abcabc", "abc") == [0, 3]
    assert su.find_pattern("hello", "xyz") == []
    print("✓ find_pattern tests passed")
    
    return True

def main():
    print("StringUtils-CPP Test Suite")
    print("=" * 30)
    
    if test_functions():
        print("\n✓ All tests passed")
        return True
    else:
        print("\n✗ Tests failed")
        return False

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)