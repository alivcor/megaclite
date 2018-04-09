from setuptools import setup, find_packages

try:
    long_desc = open('README.md').read()
except:
    long_desc = 'Megaclite'

setup(
    name="megaclite",
    url="https://github.com/alivcor/megaclite",
    author="Abhinandan Dubey",
    author_email="abhinandandubey@live.com",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "jupyter>=1",
        "sudospawner>=0.1",
        "jupyterhub>=0.0.1"
    ],
    include_package_data=True,
    description="Resource Manager for Jupyter. A moon too.",
    keywords = ['jupyterhub', 'memory', 'nbextension', 'jupyter', 'extension'], # arbitrary keywords
    long_description=long_desc,
)