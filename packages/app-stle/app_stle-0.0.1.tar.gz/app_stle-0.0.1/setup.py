import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='app_stle',
      version='0.0.1',
      url='https://gjhunt.github.io/app/',
      author='Gregory J. Hunt',
      author_email='ghunt@wm.edu',
      description='Adaptive pressure profile tracking of the shock-train leading edge.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='GPL3',
      packages=setuptools.find_packages(),
      install_requires=[
          'numpy',
          'scipy',
          'sklearn',
          'nlopt'
          ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Operating System :: OS Independent",
          'Topic :: Scientific/Engineering',
      ],
    zip_safe=True)
