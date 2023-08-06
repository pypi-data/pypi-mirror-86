import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stuart_dataops", # Replace with your own username
    version="0.1.0",
    author="Lan Row KOK",
    author_email="r.kok@stuart.com",
    description="Package used by the French Dataops team of Stuart",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StuartApp/ops-aws-scripts/tree/master/fr-scripts/stuart_dataops",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2',
    py_modules=['dataops']
)


# to refresh the wheel package do:
# python3.7 setup.py sdist bdist_wheel

# to new version to pypi
# twine upload --repository-url https://upload.pypi.org/legacy/ --skip-existing dist/*
