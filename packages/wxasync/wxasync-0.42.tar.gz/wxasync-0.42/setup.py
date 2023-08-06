from setuptools import setup

setup(name='wxasync',
      version='0.42',
      description='asyncio for wxpython',
      url='http://github.com/sirk390/wxasync',
      author='C.Bodt',
      author_email='sirk390@gmail.com',
      license='MIT',
      package_dir={'': 'src'},
      install_requires=[
          'wxpython',
      ],
      packages=[''],
      zip_safe=True)
