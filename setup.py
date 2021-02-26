import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()


setuptools.setup(
    name="funksnake",
    version="0.0.2",
    author="Wolfgang Fischer",
    author_email="31348226+gammelalf@users.noreply.github.com",
    description="Python wrapper for funkwhale api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gammelalf/funksnake",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=requirements
)
