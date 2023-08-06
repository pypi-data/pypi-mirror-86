import pygame
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ArriveTheSpaceship",
    version="0.0.1.dev1",
    author="Vinícius Azevedo",
    author_email="sousa0240@gmail.com",
    description="A frogger-like game made with Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/viniciussousaazevedo/arrive_the_spaceship",
    packages=setuptools.find_packages(),
    install_requires = ['pygame >= 2.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts':['arrive-the-spaceship = src.__main__:start']
    },
    python_requires='>=3.6',
)