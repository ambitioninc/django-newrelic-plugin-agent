import re
from setuptools import setup, find_packages

# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
assert multiprocessing


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'newrelic_plugin_agent/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


def get_lines(file_path):
    return open(file_path, 'r').read().split('\n')


install_requires = get_lines('requirements/requirements.txt')
tests_require = get_lines('requirements/requirements-testing.txt')


setup(
    name='django-newrelic-plugin-agent',
    version=get_version(),
    description='Publish arbitrary metrics to New Relic from within Django application',
    long_description=open('README.rst').read(),
    url='https://github.com/ambitioninc/django-newrelic-plugin-agent',
    author='Ryan Bales',
    author_email='opensource@ambition.com',
    keywords='',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
    ],
    license='MIT',
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='run_tests.run_tests',
    include_package_data=True,
    zip_safe=False,
)
