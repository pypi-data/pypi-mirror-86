from setuptools import setup

setup(name='pyerlamsa',
      version='0.1.1',
      description='Python client for erlamsa fuzzer',
      url='http://github.com/Darkkey/pyerlamsa',
      author='Alexander Bolshev',
      license='MIT',
      packages=['pyerlamsa'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)