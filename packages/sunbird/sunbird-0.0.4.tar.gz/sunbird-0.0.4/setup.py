import setuptools

#with open("README.md", "r") as fh:
  # long_description = fh.read()

setuptools.setup(
    name="sunbird", # Replace with your own username
    version="0.0.4",
    author=["Vivek Pisal","Vaishnavi Ghadge"],
    author_email="vivekpisal12345@gmail.com",
    description="",
    long_description="Sunbird library is created for feature engineering purpose.In this library you will get different different techniques to handle outliers ,missing values,variety of encoding techniques, normalization and feature selection techniques.",
    long_description_content_type="text/markdown",
    url="http://www.sunbird.ml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pandas','numpy','sklearn','scipy','seaborn']
)


#python3 setup.py sdist bdist_wheel
#twine upload --repository-url https://upload.pypi.org/legacy/ dist/*