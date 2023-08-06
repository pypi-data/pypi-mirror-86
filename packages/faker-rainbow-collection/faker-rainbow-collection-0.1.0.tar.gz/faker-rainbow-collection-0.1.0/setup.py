from setuptools import find_packages, setup

setup(
    name="faker-rainbow-collection",
    version="0.1.0",
    license='MIT',
    author='Daniil Trishkin',
    description="A collection of provides for the Faker data generator.",
    package_data={
        "": ["data/*.yml"],
    },
    packages=find_packages(),
)
