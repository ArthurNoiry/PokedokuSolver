from setuptools import setup, find_packages

setup(
    name="PokedokuSolver",
    version="1.0.0",
    description="A program and a database aimed at solving any grid of pokedoku",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Arthur Noiry",
    author_email="arthur.noiry@gmail.com",
    url="https://github.com/ArthurNoiry/PokedokuSolver",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.1.2",
        "pytest>=7.4.2",
        "openpyxl>=3.1.2"
    ],
    license="CC BY-NC-SA 4.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
