import setuptools

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylyric", # Replace with your own usernamepy
    version="0.0.2",
    author="aeg0n",
    author_email="chandu199827@gmail.com",
    description="A package for sentimental analysis of a song",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aegon47/pylyric.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['algorithmia'],
    entry_points={
        'console_scripts': [
            'pylyric=src.ex:main',
        ],
    },
)