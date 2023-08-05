import setuptools

with open('README.md', 'rt') as f:
    long_description = f.read()


setuptools.setup(
    name='ndpy',
    version='0.0.0',
    author='Bill Zorn',
    author_email='bill.zorn@gmail.com',
    url='https://github.com/billzorn/ndpy',
    description='N-dimensional sequences for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['ndpy'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
