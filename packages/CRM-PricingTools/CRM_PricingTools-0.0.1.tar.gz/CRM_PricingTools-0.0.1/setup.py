import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

deps_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

setuptools.setup(
    name = "CRM_PricingTools",
    version = "0.0.1",
    author = "Antonio Moreno Martín",
    author_email = "ant.moreno.martin@gmail.com",
    description = "CRM SDK for pricing models",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)