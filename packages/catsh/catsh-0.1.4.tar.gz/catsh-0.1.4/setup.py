from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="catsh",
    version="0.1.4",
    author="JheysonDev",
    url="https://github.com/JheysonDev/catsh",
    license="GNU Public License",
    packages=find_packages(),
    description="A cross-platform shell write in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.6",
)
