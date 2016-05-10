from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='dcoutside',
    version='0.1',
    description='An easy-to-use DC Inside Gallery (http://gall.dcinside.com) crawler written in Python.',
    keywords='DCInside Gallery crawler post comment 크롤러 포스트 댓글',
    url='http://github.com/j1wan/dcoutside',
    author='Jiwan Jeong',
    author_email='jiwanjeong@gmail.com',
    packages=['dcoutside'],
    install_requires=['requests', 'bs4'],
    zip_safe=False
)