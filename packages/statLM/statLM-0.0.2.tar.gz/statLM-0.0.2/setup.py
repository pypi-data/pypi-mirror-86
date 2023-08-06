# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="statLM",
    version="0.0.2",
    author="Raphael Redmer",
    license="MIT",
    author_email="ra.redmer@outlook.com",
    description="Language models to predict words",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://github.com/RaRedmer/statLM",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=required,
)
