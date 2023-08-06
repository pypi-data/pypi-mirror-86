import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="five4-tools-andyvisco", # Replace with your own username
    version="0.2.9.1",
    author="Andres Visco",
    author_email="andres.visco@five4.com.ar",
    description="Herramientas para entendimiento y modelado de datos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Five4-Argentina/five4_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'Color_Console',
        'pandas'
    ],
)