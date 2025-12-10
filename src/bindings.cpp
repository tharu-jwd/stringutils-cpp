#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "stringutils.h"

namespace py = pybind11;

PYBIND11_MODULE(pystring, m) {
    m.doc() = "High-performance string processing library with C++/Python bindings";
    
    // String processing functions
    m.def("reverse_string", &stringutils::reverse_string, "Reverse a string");
    m.def("count_char", &stringutils::count_char, "Count occurrences of a character");
    m.def("find_pattern", &stringutils::find_pattern, "Find pattern positions using KMP algorithm");
    
    m.attr("__version__") = "0.1.0";
}