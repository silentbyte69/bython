from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bf2py",
    version="0.1.0",
    author="Dmitry Seksov",
    author_email="dmitrypidaras89@gmail.com",
    description="A library that converts Brainfuck code to Python and executes it",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/silentbyte69/bf2py",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "bf2py=bf2py.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
