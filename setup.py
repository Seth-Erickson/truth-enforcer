from setuptools import setup

setup(
    name="truth-enforcer",
    version="0.1.1",  # Bumped version to show progress
    description="A Topological Hallucination Detection System for LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Seth Erickson",  # Matches your GitHub
    author_email="Manifold.tinket389@passmail.com",
    url="https://github.com/Seth-Erickson/truth-enforcer",
    py_modules=["truth_enforcer"], # CRITICAL: Matches the new underscore filename
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
    python_requires='>=3.8',
)
