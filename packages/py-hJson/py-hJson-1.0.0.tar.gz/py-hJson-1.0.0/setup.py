import setuptools

setuptools.setup(
    name="py-hJson",
    version="1.0.0",
    license='GNU General Public License v3.0',
    author="Tim232",
    author_email="endbot4023@gmail.com",
    description="A package for handling json files",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tim232/hJson",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent"
    ],
)