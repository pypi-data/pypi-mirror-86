import setuptools
import pySystem
setuptools.setup(
    name="pySystem",
    version=pySystem.__version__,
    author="Joran Beasley",
    author_email="joranbeasley@gmail.com",
    url="https://github.com/joranbeasley/PySystem",
    description="A simple tool to help interfacing with simple os calls",
    packages=['pySystem'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
