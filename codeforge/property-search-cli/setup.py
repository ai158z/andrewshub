from setuptools import setup, find_packages
import os

def setup_function():
    # Read README file
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            long_description = f.read()
    else:
        long_description = "A command-line property search tool"
    
    return setup(
        name="property-search-cli",
        version="1.0.0",
        description="A command-line property search tool",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Property Search CLI Team",
        author_email="property-search@example.com",
        packages=find_packages(),
        install_requires=[
            "argparse",
        ],
        entry_points={
            "console_scripts": [
                "property-search=src.main:main",
            ],
        },
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
        ],
        python_requires=">=3.7",
        extras_require={
            "dev": [
                "pytest>=6.0",
                "pytest-cov>=2.0",
            ],
        },
    )

if __name__ == "__main__":
    setup_function()