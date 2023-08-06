import codecs
import os
import sys
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(HERE, *parts), 'rb', 'utf-8') as f:
        return f.read()


install_requires = [
    'babel',
    'beautifulsoup4==4.6.0',
    'cached-property',
    'celery<4.0',
    'cookiecutter==1.0.0',
    'dj-database-url',
    'Django~=2.2.5',
    'django-cas-ng~=3.6.0',
    'django-el-pagination==3.1.0',
    'django-extensions>=1,<2',
    'django-google-analytics-app~=4.4.0',
    'django-libsass',
    'django-mptt~=0.10.0',
    'djangorestframework==3.10.3',
    'django-phonenumber-field==1.3.0',
    'django-import-export',
    'django-daterange-filter',
    'markdown>=3.0.1',
    'mote-praekelt~=0.1.6',
    'raven~=6.10.0',
    'redis',
    'requests',
    'setuptools>=18.5',
    'six>=1.12.0',
    'ujson==1.35',
    'unicodecsv==0.14.1',
    'unicore.content',
    'wagtail~=2.6.2',
    'wagtailmedia~=0.3.1',
    'ImageHash==3.4',
    'boto==2.49.0',
    'django-storages==1.7.1',
    'Unidecode==0.04.16',
    'django-treebeard==4.2.0',
    'django-prometheus',
    'prometheus_client',
    'django-enumfield==1.5',
    'html2markdown',
]

# we need to only install typing for python2
if sys.version_info < (3, 5):
    install_requires.append('typing')

setup(name='molo.core',
      version=read('VERSION'),
      description=('Molo is a set of tools for publishing mobi sites with a '
                   'community focus.'),
      long_description=read('README.rst'),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
      ],
      author='Praekelt.org',
      author_email='dev@praekelt.org',
      url='http://github.com/praekelt/molo',
      license='BSD',
      keywords='praekelt, mobi, web, django',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      namespace_packages=['molo'],
      install_requires=install_requires,
      entry_points={
          'console_scripts': ['molo = molo.core.scripts.cli:main'],
      })
