import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="huny_case", # Replace with your own username
    version="0.0.3",
    author="Huny",
    author_email="hy546880109@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.cnblogs.com/huny/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)