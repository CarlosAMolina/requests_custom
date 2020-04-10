import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="requests_custom",
    version="0.0.2",
    author="Carlos A Molina",
    description="Python's requests with custom configuration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carlosamolina/requests_custom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests == 2.23.0",
                      "requests-toolbelt == 0.9.1",],
    python_requires='>=3.6',
)
