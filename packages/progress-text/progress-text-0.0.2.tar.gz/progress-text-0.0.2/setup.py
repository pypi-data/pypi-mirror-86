import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="progress-text", # Replace with your own package name
    version="0.0.2",
    author="Linjian Li",
    author_email="author@example.com",
    description="Python package for printing progress in text.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LinjianLi/progress-text",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
