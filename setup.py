import os
from setuptools import setup, find_packages

LONG_DESCRIPION = """
JavaScript web apps with RequireJS, jQuery Mobile, Mustache, and Leaflet
"""

def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION

def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


package_data = get_package_data('tawq')

setup(
    name='tawq',
    version='0.2.0-dev',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='http://ta.wq.io',
    license='MIT',
    packages=find_packages(),
    package_data=package_data,
    description='Build presentations with YAML, Markdown, and jQuery Mobile',
    long_description=long_description(),
    install_requires=['wq.app>=0.4.2', 'pyyaml', 'pystache'],
    scripts=['tawq/bin/tawq'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: JavaScript',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
