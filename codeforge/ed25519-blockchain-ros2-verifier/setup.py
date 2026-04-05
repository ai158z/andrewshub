from setuptools import setup, find_packages
import os

# Read the README file for the long description
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

# Store setup arguments in variables for testing
name = 'ed25519-blockchain-ros2-verifier'
version = '1.0.0'
description = 'ED25519 signature verification library with blockchain and ROS2 integration'
author = 'Security Engineering Team'
author_email = 'security@example.com'
license = 'MIT'
url = 'https://github.com/ed25519-blockchain-ros2-verifier'
packages = find_packages()
install_requires = [
    'cryptography>=3.4.7',
    'base58',
    'requests',
    'pycryptodome',
    'ecdsa'
]
python_requires = '>=3.8'
classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Security :: Cryptography',
    'Topic :: Software Development :: Libraries :: Python Modules'
]
keywords = 'ed25519 cryptography blockchain verification ros2 security'
project_urls = {
    'Bug Reports': 'https://github.com/ed25519-blockchain-ros2-verifier/issues',
    'Source': 'https://github.com/ed25519-blockchain-ros2-verifier',
    'Documentation': 'https://github.com/ed25519-blockchain-ros2-verifier/wiki'
}
long_description_content_type = 'text/markdown'

if __name__ == "__main__":
    setup(
        name=name,
        version=version,
        description=description,
        long_description=long_description,
        long_description_content_type=long_description_content_type,
        author=author,
        author_email=author_email,
        license=license,
        url=url,
        packages=packages,
        install_requires=install_requires,
        python_requires=python_requires,
        classifiers=classifiers,
        keywords=keywords,
        project_urls=project_urls,
    )