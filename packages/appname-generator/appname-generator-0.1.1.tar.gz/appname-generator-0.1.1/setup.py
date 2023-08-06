import setuptools

setuptools.setup(
    name="appname-generator",
    description="Generate available app names",
    version="0.1.1",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["appname = appname_generator.__main__:main"]},
    install_requires=["dnspython", "tqdm"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
