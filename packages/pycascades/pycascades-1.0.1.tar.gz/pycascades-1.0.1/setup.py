import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycascades", # Replace with your own username
    version="1.0.1",
    author="Jonathan Krönke, Nico Wunderling, Jonathan Donges",
    author_email="nico.wunderling@pik-potsdam.de",
    description="PyCascades: Simulating tipping cascades on complex networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://zenodo.org/record/4153102#.X8DMhMIo9H4",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)