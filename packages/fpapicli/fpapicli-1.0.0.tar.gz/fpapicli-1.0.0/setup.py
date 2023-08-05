from setuptools import setup,find_packages

setup(
    name="fpapicli",
    version='1.0.0',
    author="Pranav V P",
    author_email="pranavvp07@gmail.com",
    description="CLI for Football Player API",
    long_description="CLI for football player API. API source : http://footballplayerapi.herokuapp.com/",
    packages=find_packages(),
    install_requires=[
        'Click',
        'Requests'
    ],
    keywords=['python', 'cli','api'],
    entry_points='''
        [console_scripts]
        fpapicli=fpapicli.fpapicli:fpapicli
    ''',
    classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)