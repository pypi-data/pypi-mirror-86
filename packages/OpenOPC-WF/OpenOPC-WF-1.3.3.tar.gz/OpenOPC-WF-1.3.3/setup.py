from setuptools import setup

setup(
    description=" OPC (OLE for Process Control) toolkit for Python 3.x with fixes.",
    install_requires=['Pyro4>=4.61'],
    keywords='python, opc, openopc',
    license='GPLv2',
    maintainer = 'Bebeto Alves',
    maintainer_email = 'bebeto@alu.ufc.br',
    name="OpenOPC-WF",
    package_dir={'':'src'},
    py_modules=['OpenOPC'],
    url='https://github.com/bebetoalves/openopc',
    version="1.3.3",
)
