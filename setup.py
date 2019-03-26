from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name="rv-schubert-sdk",
    author="Raphael Schubert",
    author_email="rfswdp@gmail.com",
    description="SKD de integracao com RV Tecnologia",
    url="https://github.com/rfschubert/rv-schubert-sdk",
    version='1.0.0',
    packages=find_packages(exclude=('tests', 'docs')),
    long_description=readme,
    install_requires=[
        'xmltodict',
        'requests',
        'pendulum',
    ],
    include_package_data=True,
)
