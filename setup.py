from setuptools import setup

setup(
    name='modem-tester',
    version='0.0.1',
    author='Eden Candelas',
    description='Modem testing for serial commands',
    long_description='Modem testing for devices with serial command interface',
    url='https://github.com/eacandelas/modem_tester',
    keywords='testing, modems, serial, iot',
    python_requires='>=3.7, <4',
    packages=find_packages(include=['lib', 'lib.*']),
    install_requires=[
        "args",
        "click",
        "prompt-toolkit",
        "pyfiglet",
        "pyserial",
        "regex",
        "six",
        "termcolor",
        "wcwidth"
    ]
)