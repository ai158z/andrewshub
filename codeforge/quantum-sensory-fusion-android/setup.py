from setuptools import setup, find_packages
import os

def read_requirements():
    """Read requirements from requirements.txt file."""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    else:
        # Fallback to hardcoded requirements if file doesn't exist
        return [
            'numpy>=1.20.0',
            'scipy>=1.7.0',
            'qiskit>=0.30.0',
            'scikit-learn>=1.0.0',
            'pandas>=1.3.0',
            'matplotlib>=3.3.0'
        ]

def read_readme():
    """Read README content for long description."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            return f.read()
    return "Quantum Sensory Fusion Android Library"

# Only run setup when this file is executed directly
if __name__ == '__main__':
    setup()
else:
    setup(
        name="quantum-sensory-fusion-android",
        version="1.0.0",
        author="Quantum Sensory Systems",
        author_email="contact@quantumsensory.ai",
        description="A library for quantum-enhanced sensory fusion on Android devices",
        long_description=read_readme(),
        long_description_content_type="text/markdown",
        url="https://github.com/quantum-sensory/quantum-sensory-fusion-android",
        project_urls={
            "Bug Tracker": "https://github.com/quantum-sensory/quantum-sensory-fusion-android/issues",
            "Documentation": "https://quantumsensory.github.io/quantum-sensory-fusion-android",
        },
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: Android",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Scientific/Engineering :: Physics",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ],
        package_dir={"": "src"},
        packages=find_packages(where="src", include=["quantum_sensory_fusion", "quantum_sensory_fusion.*"]),
        python_requires=">=3.8",
        install_requires=read_requirements(),
        include_package_data=True,
        zip_safe=False,
        extras_require={
            "dev": [
                "pytest>=6.0",
                "pytest-cov>=3.0",
                "black>=21.0",
                "flake8>=4.0",
            ],
            "docs": [
                "sphinx>=4.0",
                "sphinx-rtd-theme>=1.0",
            ],
        },
        entry_points={
            "console_scripts": [
                "qsf-android=quantum_sensory_fusion.cli:main",
            ],
        },
        package_data={
            "quantum_sensory_fusion": [
                "py.typed",
                "data/*",
                "config/*"
            ],
        },
    )