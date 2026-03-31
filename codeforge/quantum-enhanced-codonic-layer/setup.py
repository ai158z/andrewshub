from setuptools import setup, find_packages
import os

# Read long description from README.md if it exists
def read_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ''

setup_kwargs = {
    'name': 'quantum-enhanced-codonic-layer',
    'version': '0.1.0',
    'packages': find_packages(),
    'install_requires': [
        'numpy',
        'scipy',
        'networkx',
        'ros2'
    ],
    'extras_require': {
        'testing': [
            'pytest',
        ]
    },
    'python_requires': '>=3.8',
    'author': 'Quantum Codonic Research Team',
    'author_email': 'research@quantumcodonic.org',
    'description': 'A quantum-enhanced library for codonic layer implementation with quantum state management and interference tracking',
    'long_description': read_readme(),
    'long_description_content_type': 'text/markdown',
    'url': 'https://github.com/quantum-codonic/layer',
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    'entry_points': {
        'console_scripts': [
            'quantum-codonic-layer = codonic_layer.cli:main'
        ]
    }
}

# Only call setup if this file is run directly (not imported)
if __name__ == '__main__':
    setup(**setup_kwargs)