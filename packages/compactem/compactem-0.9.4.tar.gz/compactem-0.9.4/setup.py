import setuptools

setuptools.setup(
    name='compactem',
    version='0.9.4',
    description='compactem',
    license="Apache 2.0",
    packages=setuptools.find_packages(exclude=['docs']),
    url="https://bitbucket.org/aghose/compactem",
    classifiers=[
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3 :: Only',
    ],
    author="Abhishek Ghose",
    long_description="""This library implements a set of algorithms to create compact models: smaller versions of 
                        models with accuracy similar to their original version.  
                        
                        See https://compactem.readthedocs.io/en/latest/index.html""",
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    install_requires=['numpy', 'scipy', 'lightgbm', 'hyperopt',
                      'matplotlib', 'pandas', 'scikit_learn', 'seaborn']

)
