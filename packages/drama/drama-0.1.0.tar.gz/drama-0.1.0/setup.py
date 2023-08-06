import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drama",
    version="0.1.0",
    author="Paco Lopez Dekker",
    author_email="F.LopezDekker@tudelft.nl",
    description="Delft Radar Modelling and perfornance Analysis (DRaMA)",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://gitlab.tudelft.nl/drama/drama",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=[
        "numpy>1.15",
        "scipy",
        "numexpr>=2.7",
        "matplotlib",
    ],
    python_requires=">=3.7",
)
