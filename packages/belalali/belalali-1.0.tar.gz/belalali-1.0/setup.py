import setuptools
from pathlib import Path

setuptools.setup(
    name="belalali",
    version=1.0,
    lond_description=Path("README.md").read_text(),
    package=setuptools.find_packages(exclude=["test", "data"])
)
