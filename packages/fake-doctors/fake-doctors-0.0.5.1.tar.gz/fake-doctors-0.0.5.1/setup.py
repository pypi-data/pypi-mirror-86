import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='fake-doctors',
    version='0.0.5.1',
    author='Kim Du Nam',
    author_email='timecostslives@gmail.com',
    description='Tools for handling whole slide image',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/timecostslives/fake-doctors',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
)
