from setuptools import setup, find_packages

setup(
    name='staking-reward-calculator',
    version='0.1.0',
    description='A library for calculating staking rewards and compound interest',
    author='Unknown',
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'test': [
            'pytest>=6.0',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        'console_scripts': [
        ]
    },
    package_data={
        '': ['README.md', 'LICENSE'],
    },
    license='MIT',
    keywords='staking, rewards, calculator, compound interest, APY',
    url='https://github.com/unknown/staking-reward-calculator',
    project_urls={
        'Bug Reports': 'https://github.com/unknown/staking-reward-calculator/issues',
        'Source': 'https://github.com/unknown/staking-reward-calculator',
    }
)