from setuptools import setup, find_packages

long_description = open("README.md").read()

setup(
        name='rc522',
        version='0.0.1.1',
        description='RFID Utility',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author_email='william.wyatt@cgu.edu',
        url='https://github.com/Tsangares/rc522',
        include_package_data=True,
        packages=find_packages(),
        install_requires=[
            'pi-rc522',
            ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
)
