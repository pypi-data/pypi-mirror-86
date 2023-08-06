from distutils.core import setup
import setuptools
from pathlib import Path

setup(
    name='PlayReleaseApi',         # How you named your package folder (MyLib)
    # Start with a small number and increase it with every change you make
    version='0.0.1',
    packages=setuptools.find_packages(exclude=["tests", "data"]),
    long_description=Path("README.md").read_text(),
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Release Api script for github and Google Play Console',
    author='mahee96',                   # Type in your name
    author_email='developer.mahee96@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/mahee96/PlayReleaseApi',
    # I explain this later on
    download_url='https://github.com/mahee96/PlayReleaseApi/releases/download/v0.0.1/PlayReleaseApi.zip',
    # Keywords that define your package best
    keywords=['Play', 'GooglePlay', 'Console', 'Play Console',
              'python script', 'Github',
              'Release Api',
              'REST Api',
              'CI',
              'CD',
              'CICD',
              'Continuous Integration'],
    install_requires=[            # I get to this in a second
        'json',
        'os',
        're',
        'requests',
        'subprocess',
        'sys',
        'datetime',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
    ],
)
