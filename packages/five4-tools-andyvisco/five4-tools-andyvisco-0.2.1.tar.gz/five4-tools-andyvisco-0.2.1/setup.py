import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="five4-tools-andyvisco", # Replace with your own username
    version="0.2.1",
    author="Andres Visco",
    author_email="visco.andres@gmail.com",
    description="Tools for Data Manipulation and Cleaning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andresvisco",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)