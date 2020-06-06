import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    author="Carlos A Molina",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="Python's requests with custom configuration",
    include_package_data=True,
    install_requires=requirements,
    long_description_content_type="text/markdown",
    long_description=long_description,
    name="requests_custom",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    url="https://github.com/carlosamolina/requests_custom",
    version="0.0.3",
)