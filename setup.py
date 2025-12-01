from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'stringutils_cpp',
        [
            'src/stringutils.cpp',
            'src/bindings.cpp',
        ],
        include_dirs=[
            'src/',
            pybind11.get_include(),
        ],
        language='c++',
        extra_compile_args=['-std=c++17'],
    ),
]

setup(
    name="stringutils-cpp",
    version="0.1.0",
    author="Your Name", 
    description="High-performance string processing library",
    ext_modules=ext_modules,
    zip_safe=False,
    python_requires=">=3.7",
)