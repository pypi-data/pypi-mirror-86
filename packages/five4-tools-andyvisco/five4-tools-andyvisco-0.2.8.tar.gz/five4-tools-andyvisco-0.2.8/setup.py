import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="five4-tools-andyvisco", # Replace with your own username
    version="0.2.8",
    author="Andres Visco",
    author_email="andres.visco@five4.com.ar",
    description="Tools for Data Manipulation and Cleaning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Five4-Argentina/five4_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Color_Console',
        'pandas',
    ],
)