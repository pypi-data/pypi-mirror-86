import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plotpipe2d.py", # Replace with your own username
    version="1.0",
    description="Plot 2d spectra from NMRPIpe format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jlorieau/nmr/plots/plotpipe2d",
    packages=setuptools.find_packages('.'),
    data_files=[
        ('',['hsqc/trosy-fb.ft2']),
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['scripts/plotpipe2d.py',
             ],
    install_requires=[
        'nmrglue',
        'matplotlib',
        'numpy',
        'click',
    ],
)