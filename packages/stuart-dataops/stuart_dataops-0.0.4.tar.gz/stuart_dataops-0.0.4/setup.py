import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stuart_dataops", # Replace with your own username
    version="0.0.4",
    author="Lan Row KOK",
    author_email="r.kok@stuart.com",
    description="Package used by the French Dataops team of Stuart",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rowdotk/stuart_dataops",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2',
    py_modules=['dataops']
)
