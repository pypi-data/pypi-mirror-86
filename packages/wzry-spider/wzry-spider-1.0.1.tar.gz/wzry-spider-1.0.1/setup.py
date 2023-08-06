import setuptools

setuptools.setup(
    name="wzry-spider",
    version="1.0.1",
    author="super_chao",
    author_email="3160889328@qq.com",
    description="A spider to download wzry-hero image",
    long_description="A spider to download wzry-hero image",
    url="https://github.com/y-super-y/",
    packages=setuptools.find_packages(),
    license='MIT',
    keywords=['wzry', 'image', 'spider', 'download'],
    install_requires=[
        "requests",
        "tqdm",
        'lxml'
    ]
)