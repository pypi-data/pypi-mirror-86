import os
import pathlib
from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
# def load_requirements(path_dir=here, comment_char="#"):
#     with open(os.path.join(path_dir, "requirements.txt"), "r") as file:
#         lines = [line.strip() for line in file.readlines()]
#     requirements = []
#     for line in lines:
#         # filer all comments
#         if comment_char in line:
#             line = line[: line.index(comment_char)]
#         if line:  # if requirement is not empty
#             requirements.append(line)
#     return requirements


setup(
    name="simplelayout-AnjaZhang",
    version="0.0.4",
    description="A sample Python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/idrl-assignment/3-simplelayout-package-AnjaZhang',
    author="zhangxiaoya",
    author_email="zhangxiaoya09@nudt.edu.cn",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    # install_requires=load_requirements()
    install_requires=['numpy', 'matplotlib', 'scipy', 'pytest'],
    entry_points={
        "console_scripts": ["simplelayout = simplelayout:main",]
    },
)
