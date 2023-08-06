import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cptsao", # Replace with your own username
    version="0.0.1",
    author="C.P. Tsao",
    author_email="cptsao@gmail.com",
    description="example-pkg-Check_Prime_No.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cptsao/PythonStudies.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)