from setuptools import setup, find_packages

# Safely read README file
def read_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return 'Staking reward calculator with compound interest'

README = read_readme()

setup(
    name='staking-reward-calculator',
    version='1.0.0',
    description='A library for calculating staking rewards with compound interest and penalty calculations',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Staking Rewards Team',
    author_email='contact@stakingrewards.example.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'dataclasses',
        'typing',
        'decimal'
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='staking, rewards, calculator, compound interest, blockchain, cryptocurrency',
    project_urls={
        'Documentation': 'https://github.com/staking-rewards/staking-reward-calculator',
        'Source': 'https://github.com/staking-rewards/staking-reward-calculator',
        'Tracker': 'https://github.com/staking-rewards/staking-reward-calculator/issues'
    }
)