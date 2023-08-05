import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ParAlg",
    version="0.0.1",
    author="Ashwin",
    author_email="bosshere2@gmail.com",
    description="Parallel Implementations of Algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ashwin-op/paralg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
