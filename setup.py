import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='manpasswd',
    packages=setuptools.find_packages(),
    version='1.0.0',
    license='Apache License, Version 2.0',
    description='Password Manager using PostgreSQL',
    author='Gowthaman',
    author_email='rgngowthaman1@gmail.com',
    url='https://github.com/Gowthaman1401/Manpasswd',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'psycopg2',
        'tabulate',
        'genpasswd'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
    ],
    entry_points={'console_scripts': ['manpasswd=manpasswd.__main__:main']
                  },
    python_requires='>=3.6',
)
