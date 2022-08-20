import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='FilMoreBlanks',
    version='v1.0.1',
    url='https://github.com/OObasuyi/FilMoreBlanks/tree/master',
    license='MIT',
    author='osamuede obasuyi',
    author_email='eddieobasuyi@gmail.com',
    description='CSV fill in the blank editor',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    py_modules=["BlanketFill"],

)
