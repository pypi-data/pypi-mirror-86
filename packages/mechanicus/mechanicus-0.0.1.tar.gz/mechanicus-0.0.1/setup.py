from setuptools import setup

setup(
    name="mechanicus",
    version="0.0.1",
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
        "aiohttp",
        "aiofiles",
    ]
)
