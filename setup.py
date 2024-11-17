#if __init__ than python declare it as local pacakage, to install that local package we use setup.py

from setuptools import find_packages,setup

setup(
    name='mcq-generator',
    version='0.0.1',
    author='Dhruv Agrawal',
    author_email='thehackerschoice1@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2","langchain_nvidia_ai_endpoints"],
    packages=find_packages()
)