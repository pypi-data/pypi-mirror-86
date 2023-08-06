from setuptools import setup, find_packages

# specify requirements of your package here
REQUIREMENTS = ['python-exchangeratesapi', 'flask', 'wheel']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8'
    ]

# calling the setup function 
setup(name='eliwog',
      version='4.0.0',
      description='DevOps course project',
      long_description='This package will install my devops course project. use python: import eliwog',
      url='https://github.com/EliGolan69/WorldOfGames.git',
      author='Eli Golan',
      author_email='1eligolan@gmail.com',
      license='MIT',
      packages=['eliwog'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='DevOps',
      include_package_data = True
      )
