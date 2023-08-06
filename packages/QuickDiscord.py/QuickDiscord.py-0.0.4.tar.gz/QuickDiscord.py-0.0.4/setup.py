from setuptools import setup, find_packages
import quickdiscord

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name='QuickDiscord.py',
    version=quickdiscord.__version__,
    license='MIT',
    author='Team Wezacon',
    author_email='wezacon.com@gmail.com',
    description='The package that makes coding discord bots quicker!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'bots',
        'discord-py',
        'wezacon'
    ],
    install_requires=[
        'discord.py',
        'ujson',
        'requests'
    ],
    setup_requires=[
        'wheel'
    ],
    packages=find_packages()
)
