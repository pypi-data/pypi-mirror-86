import setuptools

with open("easy_communication/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy_communication", # Replace with your own username
    version="0.0.1",
    author="Mikel de Velasco",
    author_email="develascomikel@gmail.com",
    description="A simple communication between processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/develask/easy_communication",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)