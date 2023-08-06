from setuptools import setup


setup(name='sudden_appearance_calc',
      version='1.0.1',
      description='Calc',
      packages=['sudden_appearance_calc'],
      entry_points={
          'console_scripts': [
              'calculator=sudden_appearance_calc.Calculator.Calculator:main'
          ]
      },
      author_email='kuz.damir.01@gmail.com',
      zip_safe=False)