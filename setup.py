from setuptools import setup, find_packages

setup(
    name="cato-blog",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "markdown>=3.5.2",
        "python-frontmatter>=1.1.0",
        "Jinja2>=3.1.3",
        "PyYAML>=6.0.1",
        "watchdog>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cato=cato.cato.cli:main",
        ],
    },
    package_data={
        "cato": [
            "templates/*",
            "templates/admin/*",
            "templates/themes/default/*",
            "templates/themes/default/css/*",
            "templates/themes/pink/*",
            "templates/themes/pink/css/*",
            "templates/themes/sticky/*",
            "templates/themes/sticky/css/*",
            "config.yml",
        ],
    },
    author="Jeffrey-done",
    author_email="jeffrey@example.com",
    description="一个简单的静态博客生成器",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jeffrey-done/cato-blog",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 