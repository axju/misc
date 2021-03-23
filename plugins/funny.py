import os
import time
import setuptools
import random
from pkg_resources import iter_entry_points

from joke import jokes


welcome_str = """
  _____                       _             _               _                           _       ___
 |  __ \\                     | |           | |             | |                         | |     |__ \\
 | |__) |   ___    __ _    __| |  _   _    | |_    ___     | |   __ _   _   _    __ _  | |__      ) |
 |  _  /   / _ \\  / _` |  / _` | | | | |   | __|  / _ \\    | |  / _` | | | | |  / _` | | '_ \\    / /
 | | \\ \\  |  __/ | (_| | | (_| | | |_| |   | |_  | (_) |   | | | (_| | | |_| | | (_| | | | | |  |_|
 |_|  \\_\\  \\___|  \\__,_|  \\__,_|  \\__, |    \\__|  \\___/    |_|  \\__,_|  \\__,_|  \\__, | |_| |_|  (_)
                                   __/ |                                         __/ |
                                  |___/                                         |___/
"""


def main():
    welcomes = [enp.load() for enp in iter_entry_points(group='funny.welcome')]
    print(random.choice(welcomes))
    time.sleep(2)
    print(jokes.chucknorris())


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    setuptools.setup(
        name='funny',
        version='0.1.0',
        py_modules=['funny'],
        entry_points={
            'console_scripts': [
                'funny=funny:main',
            ],
            'funny.welcome': [
                'default=funny:welcome_str',
            ],
        }
    )
