from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mechanicus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.2",
    description="",
    url="https://bitbucket.org/shmyga/mechanicus",
    author="shmyga",
    author_email="shmyga.z@gmail.com",
    license="MIT",
    package_dir={"": "src"},
    packages=[
        "mechanicus.core",
        "mechanicus",
    ],
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3",
        "aiofiles>=0",
    ]
)
