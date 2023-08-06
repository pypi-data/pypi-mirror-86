import setuptools

with open("README.md",'r') as fh:
    long_description=fh.read()

setuptools.setup(
    name="kanofans",
    version="0.0.1",
    author="DTMKEN",
    author_emall="jlijian83@gmail.com",
    description="目前未完成,切勿pip b站:单推manKen,PyPi:DTMKEN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ken-kano/",
    packages=setuptools.find_packages(),
    classsifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: HIT License",
        "Operating System :: OS Independent",
    ],
)