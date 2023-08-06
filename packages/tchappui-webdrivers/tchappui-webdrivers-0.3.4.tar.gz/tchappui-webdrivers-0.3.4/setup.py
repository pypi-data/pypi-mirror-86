#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests']

setup_requirements = []

test_requirements = []

setup(
    author="Thierry Chappuis",
    author_email='tchappui@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Script to install the latest versions of chromedriver and geckodriver on travis",
    entry_points={
        'console_scripts': [
            'install-webdrivers=webdrivers.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='geckodriver, chromedriver',
    name='tchappui-webdrivers',
    packages=find_packages(include=['webdrivers', 'webdrivers.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/pythonmentor/tchappui-webdrivers',
    version='0.3.4',
    zip_safe=False,
)
