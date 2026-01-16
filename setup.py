from setuptools import setup, find_packages

setup(
    name="truth-enforcer",
    version="0.1.0",
    description="A Topological Hallucination Detection System for LLMs",
    author="Axion Research",
    packages=find_packages(),
    install_requires=[
        "sentence-transformers>=2.2.2",
        "ripser>=0.6.4",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
