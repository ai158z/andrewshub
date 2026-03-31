import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
import logging

def read_requirements():
    requirements = []
    if os.path.exists('requirements.txt'):
        with open('requirements.txt') as req_file:
            for req in req_file:
                req = req.strip()
                if req and not req.startswith('#'):
                    requirements.append(req)
    return requirements

def read_requirements_from_file():
    if os.path.exists('requirements.txt'):
        requirements = []
        with open('requirements.txt') as req_file:
            for line in req_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
        return requirements
    return []

# Only run setup() if the script is executed directly, not imported
if __name__ == "__main__":
    setup(
        name="quantum-sensory-android-embodiment",
        version="0.1.0",
        author="Quantum Android Project",
        author_email="contact@quantumandroid.org",
        description="A library for quantum sensory android embodiment systems",
        long_description=open("README.md").read() if os.path.exists("README.md") else "",
        long_description_content_type="text/markdown",
        url="https://quantumandroid.example.com",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
        python_requires=">=3.8",
        install_requires=read_requirements(),
        package_data={
            "quantum_sensors": ["data/*", "config/*"],
        },
        entry_points={
            "console_scripts": [
                "quantum-android=quantum_sensors.cli:main",
            ],
        },
    )