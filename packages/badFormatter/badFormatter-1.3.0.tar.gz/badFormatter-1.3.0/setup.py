import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="badFormatter", # Replace with your own username
    version="1.3.0",
    author="John Montgomery",
    author_email="john@johnmontgomery.tech",
    description="This is a package to format your code into hell. Designed for people who like python and hate '}', '{' and ';'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnmontgomery2003/badFormatter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
