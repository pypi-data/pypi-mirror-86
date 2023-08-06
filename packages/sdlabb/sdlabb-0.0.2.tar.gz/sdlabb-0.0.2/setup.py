from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()
    
setup(name = 'sdlabb',
      version = '0.0.2',
      description = 'Code for the språkdatalabb project',
      author = 'Fredrik Möller',
      author_email = 'fredrikmoller@recordefuture.com',
      long_description = readme(),
      long_description_content_type = 'text/markdown',
      url = 'https://github.com/BernhardMoller/sdlabb',
      packagages = find_packages(exclude=("tests",)),
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
      python_requires='>=3.6',
      )

 