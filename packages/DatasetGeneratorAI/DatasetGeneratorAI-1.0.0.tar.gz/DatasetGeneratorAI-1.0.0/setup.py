import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DatasetGeneratorAI",
    version="1.0.0",
    author="Giron",
    author_email="alissongiron.hs@gmail.com",
    description="Geração de modelos a partir da coleta automática de dados",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlissonGiron/DatasetGenerator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)