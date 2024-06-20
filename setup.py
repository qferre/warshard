from setuptools import setup, find_packages

setup(
    name="warshard",
    version="1.0",
    description="A simplified modern wargame designed to facilitate AI modeling.",
    url="http://github.com/qferre/warshard",
    author="Quentin Ferré",
    author_email="quentin.q.ferre@gmail.com",
    # install_requires=[], # list from requirements.txt to be added here
    license="Apache 2",
    packages=find_packages(),  # ['warshard'],
    include_package_data=True,
    package_data={"warshard": ["assets/*/*.jpg", "assets/*/*.png", "assets/*/*.gif"]},
    zip_safe=False,
)
