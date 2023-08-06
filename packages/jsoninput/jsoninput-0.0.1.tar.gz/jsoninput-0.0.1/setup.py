import setuptools
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsoninput",
    version="0.0.1",
    author="Riley Hall",
    author_email="riley.hall.va@gmail.com",
    description="A utility for loading and checking JSON files against a schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rileychall/json-input",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    py_modules=[Path(path).stem() for path in Path(".").glob("src/*.py")],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["jsonschema"],
)
