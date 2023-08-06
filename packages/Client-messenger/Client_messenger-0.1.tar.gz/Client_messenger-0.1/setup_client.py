from setuptools import setup, find_packages

setup(name="Client_messenger",
      version="0.1",
      description="Client_messenger",
      author="Pavel Usov",
      author_email=" ",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
