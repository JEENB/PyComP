from setuptools import setup

setup(
    name="PyComP - Python Compression Library",
    version="1.0",
    author="Jenish Raj Bajracharya",
    author_email="bjenish12@gmail.com",
    packages=["PyComP"],
    description="A small-scale library of common compressors",
    license="MIT",
    install_requires=[
        "pytest",
        "numpy",
        "bitarray",
        "typing",
        "pandas",    
    ],
)