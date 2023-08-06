from setuptools import setup

with open("./README.md", "rb") as fh:
    long_description = fh.read()

setup(
    name='PyPark',
    version='0.0.4',
    description='PyPark',
    author='liuzhuogood',
    author_email='liuzhuogood@foxmail.com',
    long_description=str(long_description, encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/liuzhuogood/PyPark',
    download_url='https://github.com/liuzhuogood/PyPark',
    packages=['PyPark', 'PyPark.nat', 'PyPark.shootback', 'PyPark.util'],
    package_data={'PyPark': ['README.md', 'LICENSE']},
    install_requires=['tornado~=6.1', 'PyYAML~=5.3.1', 'kazoo~=2.8.0', 'requests~=2.25.0', 'ruamel.yaml']
)
