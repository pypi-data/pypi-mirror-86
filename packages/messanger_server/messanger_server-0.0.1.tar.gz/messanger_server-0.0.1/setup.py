from setuptools import setup, find_packages

setup(name="messanger_server",
      version="0.0.1",
      description="messanger_server",
      author="Yuliya Mgalobelova",
      author_email="jv-av@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
