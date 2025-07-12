"""
Setup script for Financial Data Fetcher package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="financial-data-fetcher",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for fetching and analyzing financial data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/financial-data-fetcher",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "financial-data-fetcher=financial_data_fetcher.example:main",
        ],
    },
    include_package_data=True,
    package_data={
        "financial_data_fetcher": [
            "*.yml",
            "*.yaml",
            "*.json",
            "*.txt",
            "*.md",
        ],
    },
    zip_safe=False,
)
