<div align="center">
  <img src="pystringpp-logo.png" alt="pystringpp Logo" width="600">
</div>

# pystringpp

C++/Python integration using pybind11 for high-performance string processing.

## Functions

- `reverse_string(text)` - String reversal using std::reverse
- `count_char(text, char)` - Character counting with STL algorithms  
- `find_pattern(text, pattern)` - KMP pattern matching algorithm

## Performance

C++ implementation provides significant speedups over pure Python:
- Character counting: ~15x faster
- Pattern matching: ~24x faster  
- String reversal: ~10x faster

## Installation

```bash
git clone https://github.com/tharu-jwd/pystringpp.git
cd pystringpp
pip install pybind11
pip install -e .
```

## Usage

```python
import pystringpp as su

result = su.reverse_string("hello world")
count = su.count_char("programming", "m")
positions = su.find_pattern("abcabcabc", "abc")
```

## Testing

```bash
python test_pystringpp.py
```

## Technical Details

- C++17 with STL algorithms
- pybind11 for Python bindings
- Cross-platform compatibility
- Optimized for performance