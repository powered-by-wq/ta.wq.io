import os
from setuptools import setup, find_packages

LONG_DESCRIPION = """
Build interactive presentations with YAML, Markdown, and jQuery Mobile.
Powered by wq.app.
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
    version='0.3.0',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='http://ta.wq.io',
    license='MIT',
    packages=find_packages(),
    package_data=package_data,
    description='Build presentations with YAML, Markdown, and jQuery Mobile',
    long_description=long_description(),
    install_requires=['wq.app>=0.5.0', 'pyyaml', 'pystache'],
    scripts=['tawq/bin/tawq'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: JavaScript',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
    ]
)
