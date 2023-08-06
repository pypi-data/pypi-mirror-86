import setuptools

with open('README.md') as f:
    read_me = f.read()


setuptools.setup(
    name="deltalanguage",
    version="0.0.0",
    author="Riverlane",
    author_email="deltaflow@riverlane.com",
    long_description=read_me,
    long_description_content_type='text/markdown',
    copyright="Copyright (C) 2020 River Lane Research Ltd",
    license= "MIT License with Commons Clause",
    packages=setuptools.find_packages(
        include=['deltalanguage', 'deltalanguage.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Emulators'
    ],
    python_requires='>=3.8'
)
