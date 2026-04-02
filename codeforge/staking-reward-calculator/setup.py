from setuptools import setup, find_packages

setup(
    name="staking-reward-calculator",
    version="0.1.0",
    author="Staking Calculator Team",
    author_email="staking.calculator@example.com",
    description="A calculator for staking rewards with APY and compound interest calculations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/staking-calculator/staking-reward-calculator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "argparse",
        "decimal"
    ],
    entry_points={
        "console_scripts": [
            "staking-calculator=cli:main",
        ]
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.8",
        ],
    },
    keywords="staking, calculator, apy, compound interest, finance, cryptocurrency, defi",
    project_urls={
        "Bug Reports": "https://github.com/staking-calculator/staking-reward-calculator/issues",
        "Source": "https://github.com/staking-calculator/staking-reward-calculator",
    }
)