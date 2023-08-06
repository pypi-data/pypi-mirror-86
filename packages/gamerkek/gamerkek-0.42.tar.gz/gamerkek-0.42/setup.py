import setuptools
from pathlib import Path

setuptools.setup(
    name="gamerkek",
    version=0.420,
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=["data", "tests"])
)


# setuptools , uknow its like setup for games
# u get it na ???

# setuptools.setup()
# has keyword arguments

# we need to specify the "name" for our package when we upload na ??
# better be specific

# we need to tell what version it is na ?? prob 0.00 but ours start with 0.420 🤘

# long_description

# lets read the license from license file to desc. that is the description

# we need to find packages in our dir na ??
# setuptools.find_packages() is used for it. we exclude data and test since we dont need it
