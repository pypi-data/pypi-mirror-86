from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(
    name="toolbox502",
    version="1.0",
    description="Toolbox trial of Edgar Minault",
    long_description="Develop a package that outputs the exchange rate between two countries.",
    packages=find_packages(),
    url="https://github.com/edgarminault/toolbox502",
    test_suite="tests",
    # include_package_data: to install data from MANIFEST.in
    include_package_data=True,
    # scripts=["scripts/toolbox502-run"],
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6'
    )
)
