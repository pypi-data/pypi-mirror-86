import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="loler_spider",
    version="1.0.1",
    author="zzzzls",
    author_email="245129129@qq.com",
    description="A spider to download lol-hero image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zzzzls/",
    packages=setuptools.find_packages(),
    license='MIT',
    keywords=['lol', 'image', 'spider', 'download'],
    install_requires=[
        "requests",
        "tqdm"
    ]
)