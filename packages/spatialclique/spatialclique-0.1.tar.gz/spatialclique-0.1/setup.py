from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name                        = 'spatialclique',
    version                     = '0.1',
    description                 = 'Maximum clique for 2D or 3D points',
    long_description            = readme(),
    long_description_content_type = 'text/markdown',
    url                         = 'https://github.com/pjhartzell/max-clique',
    author                      = 'Preston Hartzell',
    author_email                = 'preston.hartzell@gmail.com',
    license                     = 'MIT',
    keywords                    = 'maximum clique spatial',
    packages                    = [
        'spatialclique'
    ],
    install_requires            = [
        'numpy',
        'networkx'
    ],
    include_package_data        = True
)