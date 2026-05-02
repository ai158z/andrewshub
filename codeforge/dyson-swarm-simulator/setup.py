from setuptools import setup, find_packages

setup(
    name="dyson-swarm-simulator",
    version="0.1.0",
    author="Dyson Swarm Simulator Team",
    author_email="contact@dysonswarm.com",
    description="A Dyson Swarm simulation tool for modeling solar collector deployment",
    long_description=open("README.md").read() if open("README.md").readable() else "Dyson Swarm Simulator - Simulate the deployment and efficiency of a Dyson Swarm",
    long_description_content_type="text/markdown",
    url="https://github.com/example/dyson-swarm-simulator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires='>=3.8',
    install_requires=[
        "click",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "dyson-simulate=dyson_simulator.cli:cli",
        ],
    },
    long_description_content_type="text/markdown",
    url="https://github.com/example/dyson-swarm-simulator",
)