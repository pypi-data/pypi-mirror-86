import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhomotopy", 
    version="0.0.1",
    author="Polyneikis Strongylis",
    author_email="polyneikis11@gmail.com",
    description="A package to solve nonlinear equations with HAM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/polyneikis11/pyHAM",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
