from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'road-collisions-base'
)

setup(
    name='road_collisions_canada',
    version='0.0.2',
    python_requires='>=3.6',
    description='Road collision data for Canada',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/road-collisions-canda',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    package_data={
        'road_collisions_canada': [
            'resources/canada/ca.csv.tgz'
        ]
    },
    entry_points={
        'console_scripts': [
            'load_road_collisions_canada = road_collisions_canada.bin.load:main',
        ]
    }
)
