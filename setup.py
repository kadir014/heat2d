from setuptools import setup, find_packages
import os

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, path)

setup(
    name="heat2d",
    packages = find_packages(),
    include_package_data=True,
    version="0.0.5",
    author="Kadir Aksoy",
    author_email="kursatkadir014@gmail.com",
    description="A simple 2D game engine",
    url="https://github.com/kadir014/heat2d",
    project_urls={
    'Documentation': 'https://kadir014.github.io/projects/heat2d/index.html',
    },
    keywords='game engine development 2d',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
                      "pygame>=2.0.0.dev3",
                      "moderngl>=5.6.2",
                      "psutil>=5.7.3",
                      "py-cpuinfo>=7.0.0",
                      "requests>=2.25.0"
                      ]
)
