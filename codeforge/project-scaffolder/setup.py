from setuptools import setup, find_packages
import os

def read_requirements():
    """Read requirements from requirements.txt file."""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

def read_readme():
    """Read the README.md file."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Only call setup() when this file is run directly, not when imported
if __name__ == '__main__':
    # This ensures the setup() function is only called when running setup.py directly
    # and not during imports for testing
    setup(
        name='project-scaffolder',
        version='1.0.0',
        description='A CLI tool for scaffolding software projects',
        long_description=read_readme(),
        long_description_content_type='text/markdown',
        author='Developer',
        author_email='developer@example.com',
        url='https://github.com/example/project-scaffolder',
        license='MIT',
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Operating System :: OS Independent',
        ],
        keywords='project scaffolding, template, generator',
        packages=find_packages(where='src'),
        package_dir={'': 'src'},
        python_requires='>=3.7',
        install_requires=read_requirements(),
        entry_points={
            'console_scripts': [
                'project-scaffolder=main:main',
            ],
        },
    )