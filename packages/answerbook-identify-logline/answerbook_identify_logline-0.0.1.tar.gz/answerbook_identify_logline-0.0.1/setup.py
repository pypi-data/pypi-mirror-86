from setuptools import setup, find_packages
from sys import path

from identify_logline import __version__

path.insert(0, '.')

NAME = "answerbook_identify_logline"

if __name__ == "__main__":

    with open('requirements.txt') as f:
        requirements = f.read().splitlines()

    setup(
        name=NAME,
        version=__version__,
        author="Jonathan Kelley",
        author_email="jonkelley@gmail.com",
        url="https://github.com/jondkelley/identify_logline",
        license='Copyleft',
        packages=find_packages(),
        package_dir={NAME: NAME},
        description="answerbook_identify_logline - Identify log lines",

        install_requires=requirements,

        entry_points={
            'console_scripts': ['answerbook_identify_logline = identify_logline.identify:main'],
        }
    )
