from setuptools import setup, find_packages

setup(
    name="green_api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
    ],
    description="Модуль для работы с API Green API",
    author="Tsunami43",
    url="https://github.com/Tsunami43/green_api",
)
