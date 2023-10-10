#/usr/bin/env python

import sys
from setuptools import setup

def main():
    setup(
        name='undiscord',
        version='1.47',
        author="HardcodedCat",
        scripts=['undiscord'],
        py_modules=['undiscord'],
        description='Bulk wipe messages in a Discord server or DM using a Python interpreter on Android or PC.',
        install_requires=['furl', 'pwinput', 'icmplib', 'progress'],
        keywords=['setuptools', 'undiscord', 'discord', 'wipe', 'delete', 'erase', 'messages', 'selfbot', 'userscript'],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Natural Language :: Portuguese",
            "Natural Language :: Portuguese (Brazilian)",
            "Operating System :: Android",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: OS Independent",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Communications :: Chat",
            "Topic :: Communications :: Chat :: Internet Relay Chat",
            "Topic :: Internet",
            "Topic :: Utilities",
            "Typing :: Typed"
        ],
        python_requires='>=3.7',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        platforms=['any'],
        url='https://github.com/HardcodedCat/undiscord-python',
        license="MIT"
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
