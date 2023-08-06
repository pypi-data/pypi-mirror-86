import os
import os.path

from setuptools import find_packages, setup


def find_requires():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    requirements = []
    with open("{0}/requirements.txt".format(dir_path), "r") as reqs:
        requirements = reqs.readlines()
    return requirements


if __name__ == "__main__":
    setup(
        name='krestiki_noliki',
        version='0.1.0',
        description='Game krestiki_noliki.'
                    + 'for play write "krestiki_noliki --start" in console',
        packages=find_packages(),
        install_requires=find_requires(),
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'krestiki_noliki --start = krestiki_noliki.game:main',
            ]
        }
    )
