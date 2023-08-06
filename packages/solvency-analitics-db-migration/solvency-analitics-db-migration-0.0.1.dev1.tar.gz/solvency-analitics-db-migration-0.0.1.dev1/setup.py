import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="solvency-analitics-db-migration", # Replace with your own username
    version="0.0.1dev1",
    author="Andras Kohlmann",
    author_email="metuoku@outlook.com",
    description="Nano db migration framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andraskohlmann/solvency-analitics-db-migration",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)