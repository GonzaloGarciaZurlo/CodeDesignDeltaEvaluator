"""
module with the setup configuration
"""
from setuptools import setup, find_packages


setup(
    name="delta-design-evaluator",
    version="0.1.0",
    author="Gonzalo García Zurlo",
    author_email="gonzalo.garcia.zurlo@mi.unc.edu.ar",
    description="A system for evaluating implicit design changes in code during agile reviews",
    url="https://github.com/GonzaloGarciaZurlo/CodeDesignDeltaEvaluator",
    packages=find_packages(),
    python_requires='>=3.12',
    install_requires=[
        "networkx",
        "pyparsing",
        "pytest",
        "pylint",
        "re"
    ],
)
