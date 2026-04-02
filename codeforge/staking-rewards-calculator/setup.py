from setuptools import setup, find_packages
import os

def read_readme():
    try:
        if os.path.exists("README.md"):
            with open("README.md", "r") as fh:
                return fh.read()
        else:
            return "A library for calculating staking rewards"
    except:
        return "A library for calculating staking rewards"

setup(
    name="staking-rewards-calculator",
    version="0.1.0",
    author="OpenDevs",
    author_email="contact@opendevs.example.com",
    description="A library for calculating staking rewards with configurable APY, compounding frequency, and penalties",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/opendevs/staking-rewards-calculator",
    project_urls={
        "Bug Tracker": "https://github.com/opendevs/staking-rewards-calculator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "staking-calculator=src.staking_calculator:main",
        ]
    },
)