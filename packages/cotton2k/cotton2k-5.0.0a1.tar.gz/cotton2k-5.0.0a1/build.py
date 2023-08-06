from Cython.Build import cythonize
from setuptools import Extension


def build(setup_kwargs):
    setup_kwargs.update({
        "ext_modules": cythonize(Extension(
            "cotton2k",
            sources=["cotton2k.pyx"],
            language="c++",
            extra_compile_args=["-std=c++17"],
        ), language_level=3,),
    })
