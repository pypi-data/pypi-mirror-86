import setuptools
with open("README.md",'r',encoding='utf8') as f:
    long_description = f.read()
setuptools.setup(
    name ="vipcode_summer",
    version="1.0",
    author="vipcode_summer",
    author_email="930172567@qq.com",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages=setuptools.find_packages(),
    url="https://www.vipcode.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',


)