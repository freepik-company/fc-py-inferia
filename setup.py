# coding: utf-8

from setuptools import setup, find_packages  # noqa: H301

name = "cogito"
version = "0.0.0"
python_requires = ">= 3.10"
description = "Cogito is a Python module designed to streamline the creation and deployment of inference services. It provides tools and abstractions to wrap machine learning models and expose them as robust, production-ready APIs with minimal effort."
long_description = """A longer description of the project."""
author = "freepik-company/tech-avengers"
author_email = "aivengers@freepik.com"
# Get the requirements from the requirements.txt file
requires = [line.strip() for line in open("requirements.txt")]

setup(
        name = name,
        version = version,
        description = description,
        author = author,
        author_email = author_email,
        url = "",
        python_requires = python_requires,
        install_requires = requires,
        packages = find_packages(exclude=["test", "tests"]),
        include_package_data = True,
        long_description_content_type = "text/markdown",
        long_description = long_description,
        package_data = {f"{name}": ["py.typed"]},
)