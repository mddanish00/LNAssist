from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lnassist',
    version='1.0.74',
    packages=['lnassist'],
    url='https://github.com/Miracutor/LNAssist',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Miracutor',
    author_email='miracleexecutors@gmail.com',
    description='', install_requires=['requests', 'beautifulsoup4', 'readability-lxml', 'lxml', 'tqdm'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.7'
)
