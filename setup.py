"""
Setup script for RAG Graph Wiki Base
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rag-graph-wiki-base",
    version="0.1.0",
    author="tunghauvan-interspace",
    description="A simple LLM chat application with Neo4j storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tunghauvan-interspace/rag-graph-wiki-base",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.3.0",
        "langchain-community>=0.3.27",
        "langchain-openai>=0.2.0",
        "neo4j>=5.15.0",
        "python-dotenv>=1.0.0",
        "openai>=1.7.0",
    ],
)
