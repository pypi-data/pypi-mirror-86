import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kranthoslib",
    version="0.0.3",
    author="Kranthos",
    author_email="kranthosathens@gmail.com",
    description="Kranthos Python Library",
    long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/Kranthos/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)