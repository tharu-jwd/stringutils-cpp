from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir
import pybind11

ext_modules = [
    Pybind11Extension(
        "stringutils_cpp",
        [
            "src/stringutils.cpp",
            "src/bindings.cpp",
        ],
        include_dirs=[
            "src/",
            pybind11.get_include(),
        ],
        cxx_std=17,
    ),
]

from setuptools import setup

setup(
    name="stringutils-cpp",
    version="0.1.0",
    author="Your Name",
    description="High-performance string processing library",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
)