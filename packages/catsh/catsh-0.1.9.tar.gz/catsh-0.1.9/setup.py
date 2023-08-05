from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="catsh",
    version="0.1.9",
    author="JheysonDev",
    url="https://github.com/JheysonDev/catsh",
    license="GPLv3",
    packages=find_packages(),
    description="A cross-platform shell write in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    install_requires=["colorama==0.4.4"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "catsh=Catsh.main:run",
        ]
    },
)
