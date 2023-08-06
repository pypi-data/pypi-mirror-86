from setuptools import setup, find_packages

VERSION = '0.1.3'
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='phbdl',
      version=VERSION,
      description="a tiny and smart cli video downloader for pxxxhub",
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='video downloader',
      author='sunbless',
      author_email='sunblessliu@gmail.com',
      url='https://github.com/yontonl/phbdl',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'requests', 'js2py', 'bs4'
      ],
      entry_points={
          'console_scripts': [
              'phbdl = phbdl.main:main'
          ]
      },
      )
