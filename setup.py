# coding: utf-8

from setuptools import setup, find_packages  # noqa: H301

name = "cogito"
version = "0.0.0"
python_requires = ">= 3.10"
description = "Cogito is a Python module designed to streamline the creation and deployment of inference services. It provides tools and abstractions to wrap machine learning models and expose them as robust, production-ready APIs with minimal effort."
long_description = """
Cogito is a versatile Python module aimed at simplifying the development and deployment of inference services. 
It allows users to wrap machine learning models or any computational logic into APIs effortlessly. 
With Cogito, you can focus on your core algorithmic functionality while the module takes care of the heavy lifting, including API structure, request handling, error management, and scalability.

Key features include:
	•	Ease of Use: Simplifies the process of converting your models into production-ready APIs with minimal boilerplate code.
	•	Customizable API: Provides flexibility to define endpoints, input/output formats, and pre/post-processing logic.
	•	Scalability: Optimized to handle high-throughput scenarios with support for modern server frameworks.
	•	Extensibility: Easily integrate with third-party libraries, monitoring tools, or cloud services.
	•	Error Handling: Built-in mechanisms to catch and handle runtime issues gracefully.
"""
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