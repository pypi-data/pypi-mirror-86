import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="askew3",
    version="0.0.1",
    author="Original Author: Hou-Ning Hu / @eborboihuc",
    author_email="rinconrex@gmail.com",
    description="3D perspective transformation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRincon/askew3",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'opencv-python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
