import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='opencities',
    version='0.0.4',
    author='Zac Thiel',
    author_email='digitalservices@grcity.us',
    description='Packages for the OpenCities API',
    long_description_content_type='text/markdown',
    url='https://github.com/GRInnovation/opencities',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7.7',
)