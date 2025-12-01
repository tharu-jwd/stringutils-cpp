#pragma once

#include <string>
#include <vector>
#include <unordered_map>

/**
 * @file stringutils.h
 * @brief High-performance string utilities library
 * 
 * This header defines a collection of optimized string processing functions
 * designed for maximum performance using modern C++17 features.
 */

namespace stringutils {

    /**
     * @brief Efficiently reverse a string in-place using iterators
     * 
     * This function reverses the input string using the most efficient
     * approach available in the STL. It handles empty strings gracefully.
     * 
     * @param input The string to reverse (passed by const reference for efficiency)
     * @return std::string A new string containing the reversed input
     * 
     * Time Complexity: O(n) where n is the length of the string
     * Space Complexity: O(n) for the return value
     * 
     * @example
     * std::string result = reverse_string("hello");
     * // result == "olleh"
     */
    std::string reverse_string(const std::string& input);

    /**
     * @brief Count occurrences of a specific character in a string
     * 
     * Efficiently counts how many times a specific character appears in the
     * input string. The search is case-sensitive and handles null characters.
     * 
     * @param input The string to search in (passed by const reference)
     * @param c The character to count
     * @return int The number of times the character appears in the string
     * 
     * Time Complexity: O(n) where n is the length of the string
     * Space Complexity: O(1)
     * 
     * @example
     * int count = count_char("hello world", 'l');
     * // count == 3
     */
    int count_char(const std::string& input, char c);

    /**
     * @brief Find all positions where a pattern occurs in text using KMP algorithm
     * 
     * Uses the Knuth-Morris-Pratt (KMP) algorithm for efficient pattern matching.
     * Returns all starting positions where the pattern is found in the text.
     * Handles edge cases like empty patterns or text.
     * 
     * @param text The text to search in (passed by const reference)
     * @param pattern The pattern to search for (passed by const reference)
     * @return std::vector<int> Vector of 0-based indices where pattern starts
     * 
     * Time Complexity: O(n + m) where n is text length, m is pattern length
     * Space Complexity: O(m) for the failure function
     * 
     * @example
     * auto positions = find_pattern("abcabcabc", "abc");
     * // positions == {0, 3, 6}
     */
    std::vector<int> find_pattern(const std::string& text, const std::string& pattern);

    /**
     * @brief Validate if a string represents a valid DNA sequence
     * 
     * Checks if the input string contains only valid DNA nucleotide characters:
     * A, T, G, C (case-insensitive). Empty strings are considered valid.
     * 
     * @param sequence The DNA sequence to validate (passed by const reference)
     * @return bool True if sequence contains only A, T, G, C; false otherwise
     * 
     * Time Complexity: O(n) where n is the length of the sequence
     * Space Complexity: O(1)
     * 
     * @example
     * bool valid = validate_dna("ATGC");
     * // valid == true
     * bool invalid = validate_dna("ATGX");
     * // invalid == false
     */
    bool validate_dna(const std::string& sequence);

    /**
     * @brief Calculate GC content percentage in a DNA sequence
     * 
     * Computes the percentage of Guanine (G) and Cytosine (C) nucleotides
     * in the given DNA sequence. The calculation is case-insensitive.
     * Returns 0.0 for empty sequences or sequences with no valid nucleotides.
     * 
     * @param sequence The DNA sequence to analyze (passed by const reference)
     * @return double GC content as a percentage (0.0 to 100.0)
     * 
     * Time Complexity: O(n) where n is the length of the sequence
     * Space Complexity: O(1)
     * 
     * @example
     * double gc = calculate_gc_content("ATGC");
     * // gc == 50.0 (2 GC out of 4 total)
     */
    double calculate_gc_content(const std::string& sequence);

    // Legacy functions (maintained for backward compatibility)
    std::unordered_map<char, int> count_chars(const std::string& input);
    std::string remove_duplicates(const std::string& input);
    bool is_palindrome(const std::string& input);
    std::string longest_common_subsequence(const std::string& str1, const std::string& str2);
    int levenshtein_distance(const std::string& str1, const std::string& str2);

} // namespace stringutils