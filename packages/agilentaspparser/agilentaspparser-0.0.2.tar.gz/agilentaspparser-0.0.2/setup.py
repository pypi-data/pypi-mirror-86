import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agilentaspparser", # Replace with your own username
    version="0.0.2",
    author="Eduardo Gonik",
    author_email="gonik@quimica.unlp.edu.ar",
    description="Parser for Agilent IR .asp files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/egonik-unlp/agilent_ir",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
