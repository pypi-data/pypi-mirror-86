import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kommand",
    version="0.3",
    author="kzulfazriawan",
    author_email="kzulfazriawan@gmail.com",
    description="This is your kommand, CLI interactive with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kzulfazriawan/kommand",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
