import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="times-ss", # Replace with your own username
    version="0.0.1",
    author="yljoke",
    author_email="895479558@qq.com",
    description="a time package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YYjoke/pysofa.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)