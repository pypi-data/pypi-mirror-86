import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytorch2tf",
    version="0.0.1",
    author="Jeffrey Pan",
    author_email="jeffreyzpan@gmail.com",
    description="A pipeline to convert pretrained PyTorch image models to Tensorflow format for deployment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeffreyzpan/pytorch-2-tf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
