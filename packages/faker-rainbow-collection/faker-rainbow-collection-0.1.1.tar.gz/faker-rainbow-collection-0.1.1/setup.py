from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="faker-rainbow-collection",
    version="0.1.1",
    license='MIT',
    author='Daniil Trishkin',
    description="A collection of provides for the Faker data generator.",
    package_data={
        "": ["data/*.yml"],
    },
    install_requires=required,
    packages=find_packages(),
)
