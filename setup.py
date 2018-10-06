from setuptools import setup

setup(name='PropositionTable',
	description='Draw table of all possible values of a propsition',
	version='0.0.2b',
	url='https://github.com/Dragneel1234/PropositionTable',
	author='Dragneel1234',
    author_email='blwal7057@gmail.com',
    license='GPL-3.0',
    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: End Users/Desktop'
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3 :: Only'
      ],
    packages=['proposition_table'],
    entry_points={
          'console_scripts': [
              'propositiontable = proposition_table.proposition_table:main'
          ]
      },
	)