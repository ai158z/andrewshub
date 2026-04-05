from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(this_directory, "README.md")

# Check if README exists, if not, set long_description to empty string
if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = ""

setup(
    name="ai-skill-library-framework",
    version="1.0.0",
    author="AI Framework Team",
    author_email="ai.framework@example.com",
    description="A framework for managing AI skills with curiosity-driven task allocation and scoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/ai-skill-library-framework",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License", 
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "tensorflow>=2.8.0",
        "torch>=1.10.0",
        "numpy>=1.21.0",
        "gym>=0.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=3.0",
            "black>=21.0",
            "flake8>=4.0",
        ],
        "docs": [
            "sphinx>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-skill-library=src.cli:main",
        ]
    },
)