import os

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file.
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="nexus-sdk",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="CAMH KCNI version of Python SDK for Blue Brain Nexus.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="kcni nexus sdk",
    url="https://github.com/krembilneuroinformatics/kcni-nexus-python-sdk",
    license="Apache License, Version 2.0",
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=[
        "puremagic",
        "requests",
        "sseclient==0.0.22",
        "rdflib",
        "SPARQLWrapper",
        "pandas"
    ],
    extras_require={
        "test": ["pytest", "pytest-cov"],
        "doc": ["sphinx"],
    },
    data_files=[("", ["LICENSE.txt"])],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Topic :: Database",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Natural Language :: English",
    ]
)
