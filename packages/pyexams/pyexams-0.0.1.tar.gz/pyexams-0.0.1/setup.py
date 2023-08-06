import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyexams",
    version="0.0.1",
    author="Pablo Angulo",
    author_email="pablo.angulo@upm.es",
    description="Generates variants of exam questions using texsurgery, keeps a question database, exports to pdf and moodle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://framagit.org/pang/pyexams",
    packages=setuptools.find_packages(),
    install_requires=[
      'texsurgery',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
