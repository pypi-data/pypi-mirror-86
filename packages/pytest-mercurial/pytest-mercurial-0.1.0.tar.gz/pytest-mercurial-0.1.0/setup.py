from setuptools import setup, find_packages

with open('install-requirements.txt', 'r') as install_reqf:
    install_req = [req.strip() for req in install_reqf]

setup(
    name='pytest-mercurial',
    version='0.1.0',
    author='Georges Racinet',
    author_email='georges.racinet@octobus.net',
    url='https://foss.heptapod.net/mercurial/pytest',
    description="pytest plugin to write integration tests for "
    "projects using Mercurial Python internals",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='hg mercurial testing pytest',
    license='GPLv2+',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved"
        " :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Version Control :: Mercurial",
    ],
    install_requires=install_req,
)
