import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
    name="duco-miner-reVox96", # Replace with your own username
    version="1.7",
    author="Robert Piotrowski",
    author_email="robik123.345@gmail.com",
    description="Official Duino-Coin Python Miner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://duinocoin.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.5',
)
