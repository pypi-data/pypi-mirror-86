import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GML_KIN",
    version="0.0.1",
    author="Pedram Dadkhah",
    author_email="Pedram.Dadkhah1374@gmail.com",
    description="K Immediate Neighbours aka KIN is inspired by KNN (K Nearest Neighbors) and adjusted to graph-structured data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PinaxX/KIN",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)