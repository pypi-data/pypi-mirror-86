from setuptools import setup


setup(name='sudden_appearance_calc',
      version='1.0.0',
      description='Calc',
      packages=['sudden_appearance_calc'],
      entry_points={
          'console_script': [
              'calculator=sudden_appearance_calc.Calculator.Calculator:main'
          ]
      },
      author_email='kuz.damir.01@gmail.com',
      zip_safe=False)