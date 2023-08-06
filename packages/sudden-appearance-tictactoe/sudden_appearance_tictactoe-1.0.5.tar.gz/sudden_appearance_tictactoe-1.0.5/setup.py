from setuptools import setup

setup(name='sudden_appearance_tictactoe',
      version='1.0.5',
      description='Calc',
      packages=['sudden_appearance_tictactoe'],
      install_requires=['colorama'],
      entry_points={
          'console_scripts': [
              'tic-tac-toe=sudden_appearance_tictactoe.Game:run'
          ]
      },
      author_email='kuz.damir.01@gmail.com',
      zip_safe=False)
