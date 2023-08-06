from distutils.core import setup

# This is a list of files to install, and where
# (relative to the 'root' dir, where setup.py is)
# You could be more specific.
files = []

# with open('requirements.txt', 'r') as f:
#     install_requires = f.read().splitlines()

setup(name="rho-pysparnn",
      version="0.4.2",
      description="Sparse (approximate) nearest neighbor search for python!",
      author="Spencer Beecher",
      author_email="spencebeecher@gmail.com",
      # url = "",
      # Name the folder where your packages live:
      # (If you have other packages (dirs) or modules (py files) then
      # put them into the package directory - they will be found
      # recursively.)
      packages=['pysparnn'],
      # 'package' package must contain files (see list above)
      # I called the package 'package' thus cleverly confusing the whole issue...
      # This dict maps the package name =to=> directories
      # It says, package *needs* these files.
      # package_data = {},
      # 'runner' is in the root.
      # scripts = [],
      long_description="""Sparse (approximate) nearest neighbor search for python!""",
      install_requires=[
            'numpy>=1.11.2',
            'scipy>=0.18.1',
            'scikit_learn>=0.17.1'
      ]
      #
      # This next part it for the Cheese Shop, look a little down the page.
      # classifiers = []
      )
