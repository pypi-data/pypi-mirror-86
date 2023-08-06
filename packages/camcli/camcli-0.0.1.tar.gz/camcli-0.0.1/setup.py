from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_install_requires():
    reqs = [
        'requests',
        'pytest'
    ]
    return reqs


setup(name='camcli',
      version='0.0.1',
      description='camcli',
      url='https://github.com/iminders/camcli',
      author='liuwen',
      author_email='liuwen.w@qq.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
      python_requires='>=3',
      install_requires=read_install_requires(),
      )
