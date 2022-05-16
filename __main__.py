"""Start gunicorn in debugging mode
"""

import sys
import os


if __name__ == '__main__':
    major, minor = sys.version_info[:2]

    if major < 3 or minor < 8:
        raise Exception("[module]: require Python 3.8 or higher")

    os.chdir(os.path.realpath(os.path.dirname(__file__)))
    os.system('gunicorn --reload')
