from setuptools import setup

setup(name='ad7124',
      version='0.1',
      description='AD7124 driver used on ADC6 Click board',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
      ],
      url='https://github.com/AndyBlightLeeds/adc6click.git',
      author='Andy Blight',
      author_email='a.j.blight@leeds.ac.uk',
      license='MIT',
      packages=['ad7124'],
      install_requires=[
          'pigpio',
          'pdoc3',
      ],
      zip_safe=False)
