import setuptools

setuptools.setup(
    name="qportalwrapper",
    version="1.0.0",
    author="Vincent Wang",
    author_email="vwangsf@gmail.com",
    description="An unofficial Python wrapper for interfacing with Q Portal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/bbworld1/qportalwrapper",
    download_url="",
    packages=setuptools.find_packages(),
    keywords="qportal qconnection qstudent",
    install_requires=[
        "requests",
        "lxml"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3'
    ],
)
