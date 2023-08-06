import setuptools

setuptools.setup(
    name="app-name-generator",
    description="Generate available app names",
    version="0.1.1",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["appname = app_name_generator.__main__:main"]},
    install_requires=["dnspython"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
