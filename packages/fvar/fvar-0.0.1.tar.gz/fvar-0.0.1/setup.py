import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fvar", # Replace with your own username
    version="0.0.1",
    author="Dan W-B",
    author_email="d@nielwb.com",
    description="Scratch-based weakly typed variables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dantechguy/fv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)