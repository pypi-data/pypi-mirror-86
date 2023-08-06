from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), "VERSION")) as file:
    version = file.read().strip()

setup(name='tinysbus',
      version=version,
      description='Small SAIA SBUS implementation for Python',
      packages=['tinysbus'],
      install_requires=['pyserial'])