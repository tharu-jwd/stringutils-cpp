#include "stringutils.h"
#include <string>
#include <unordered_map>
#include <algorithm>
#include <vector>
#include <cctype>
#include <numeric>

namespace stringutils {

std::string reverse_string(const std::string& input) {
    // Handle empty string edge case
    if (input.empty()) {
        return input;
    }
    
    // Use move semantics for optimal performance
    std::string result = input;
    std::reverse(result.begin(), result.end());
    return result;
}

std::unordered_map<char, int> count_chars(const std::string& input) {
    std::unordered_map<char, int> counts;
    for (char c : input) {
        counts[c]++;
    }
    return counts;
}

std::string remove_duplicates(const std::string& input) {
    std::string result;
    std::unordered_map<char, bool> seen;
    
    for (char c : input) {
        if (seen.find(c) == seen.end()) {
            seen[c] = true;
            result += c;
        }
    }
    return result;
}

bool is_palindrome(const std::string& input) {
    std::string cleaned;
    for (char c : input) {
        if (std::isalnum(c)) {
            cleaned += std::tolower(c);
        }
    }
    
    std::string reversed = cleaned;
    std::reverse(reversed.begin(), reversed.end());
    return cleaned == reversed;
}

std::string longest_common_subsequence(const std::string& str1, const std::string& str2) {
    int m = str1.length();
    int n = str2.length();
    
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (str1[i-1] == str2[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = std::max(dp[i-1][j], dp[i][j-1]);
            }
        }
    }
    
    std::string result;
    int i = m, j = n;
    while (i > 0 && j > 0) {
        if (str1[i-1] == str2[j-1]) {
            result = str1[i-1] + result;
            i--;
            j--;
        } else if (dp[i-1][j] > dp[i][j-1]) {
            i--;
        } else {
            j--;
        }
    }
    
    return result;
}

int levenshtein_distance(const std::string& str1, const std::string& str2) {
    int m = str1.length();
    int n = str2.length();
    
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1));
    
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (str1[i-1] == str2[j-1]) {
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = 1 + std::min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]});
            }
        }
    }
    
    return dp[m][n];
}

int count_char(const std::string& input, char c) {
    // Handle empty string edge case
    if (input.empty()) {
        return 0;
    }
    
    // Use std::count for optimal performance - it's highly optimized
    return static_cast<int>(std::count(input.begin(), input.end(), c));
}

std::vector<int> find_pattern(const std::string& text, const std::string& pattern) {
    std::vector<int> positions;
    
    // Handle edge cases
    if (pattern.empty() || text.empty() || pattern.length() > text.length()) {
        return positions;
    }
    
    // Build KMP failure function for optimal O(n+m) performance
    auto build_failure_function = [](const std::string& pattern) {
        std::vector<int> failure(pattern.length(), 0);
        int j = 0;
        
        for (size_t i = 1; i < pattern.length(); ++i) {
            while (j > 0 && pattern[i] != pattern[j]) {
                j = failure[j - 1];
            }
            if (pattern[i] == pattern[j]) {
                ++j;
            }
            failure[i] = j;
        }
        return failure;
    };
    
    // KMP pattern matching algorithm
    const auto failure = build_failure_function(pattern);
    int j = 0;
    
    for (size_t i = 0; i < text.length(); ++i) {
        while (j > 0 && text[i] != pattern[j]) {
            j = failure[j - 1];
        }
        if (text[i] == pattern[j]) {
            ++j;
        }
        if (static_cast<size_t>(j) == pattern.length()) {
            positions.push_back(static_cast<int>(i - pattern.length() + 1));
            j = failure[j - 1];
        }
    }
    
    return positions;
}

bool validate_dna(const std::string& sequence) {
    // Empty sequence is considered valid
    if (sequence.empty()) {
        return true;
    }
    
    // Use std::all_of for optimal performance and readability
    return std::all_of(sequence.begin(), sequence.end(), [](char c) {
        // Convert to uppercase for case-insensitive comparison
        char upper_c = static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
        return upper_c == 'A' || upper_c == 'T' || upper_c == 'G' || upper_c == 'C';
    });
}

double calculate_gc_content(const std::string& sequence) {
    // Handle empty sequence edge case
    if (sequence.empty()) {
        return 0.0;
    }
    
    // Count G and C nucleotides using std::count_if for performance
    const int gc_count = std::count_if(sequence.begin(), sequence.end(), [](char c) {
        char upper_c = static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
        return upper_c == 'G' || upper_c == 'C';
    });
    
    // Calculate percentage - use double division to avoid integer truncation
    return (static_cast<double>(gc_count) / static_cast<double>(sequence.length())) * 100.0;
}

}