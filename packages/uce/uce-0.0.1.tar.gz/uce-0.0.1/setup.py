import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uce",
    version="0.0.1",
    author="Bülent Aldemir",
    author_email="buelent@e-evolution.de",
    description="µce",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lmrck/dnb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)