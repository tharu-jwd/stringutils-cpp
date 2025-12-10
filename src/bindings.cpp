#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "pystringpp.h"

namespace py = pybind11;

PYBIND11_MODULE(pystringpp, m) {
    m.doc() = "High-performance string processing library with C++/Python bindings";
    
    // String processing functions
    m.def("reverse_string", &pystringpp::reverse_string, "Reverse a string");
    m.def("count_char", &pystringpp::count_char, "Count occurrences of a character");
    m.def("find_pattern", &pystringpp::find_pattern, "Find pattern positions using KMP algorithm");
    
    m.attr("__version__") = "0.1.0";
}