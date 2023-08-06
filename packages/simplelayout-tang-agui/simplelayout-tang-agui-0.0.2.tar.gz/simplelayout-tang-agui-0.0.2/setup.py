import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplelayout-tang-agui", # Replace with your own username
    version="0.0.2",
    author="Tang guijian",
    author_email="tangbanllniu@163.com",
    # license="MIT",
    description="A simplelayout package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idrl-assignment/3-simplelayout-package-tang-agui",
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="Simplelayout package",
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'pytest',
        'numpy',
        'matplotlib',
        'scipy'
    ],
    python_requires='>=3.6',
    entry_point={
        'console_scripts':[
            'simplelayout=simplelayout.__main__:main'
        ]
    }
)