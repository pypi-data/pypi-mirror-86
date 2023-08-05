import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(name='tmqc',
    version='0.0.1',
    description='tian ma quant cloud',
    author='tmqc',
    author_email='tmqc@gmail.com',
    url="https://github.com/tmqc/tmqc",
    license='LGPT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='==3.6.5',
    include_package_data=True,
    zip_safe=False)