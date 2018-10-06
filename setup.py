from setuptools import setup

setup(name='PropositionTable',
	description='Draw table of all possible values of a propsition',
	version='0.0.3b',
	url='https://github.com/Dragneel1234/PropositionTable',
	author='Dragneel1234',
    author_email='blwal7057@gmail.com',
    license='GPL-3.0',
    classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3 :: Only'
      ],
    packages=['PropositionTable'],
    entry_points={
          'console_scripts': [
              'PropositionTable = PropositionTable.proposition_table:main'
          ]
      },
    install_requires=[
          'pywin32>=223',
          'pypiwin32>=223'
      ]
	)