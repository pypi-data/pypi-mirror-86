from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        content = f.read()
    return content


setup(
    name="codetrace-pse",
    # use_scm_version=True,
    version="1.1.0",
    description="Just another package for GitLab CI/CD Demo",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/melcdn/codetrace-pse",
    author="Mel Cadano",
    author_email="mel.cdn@outlook.ph",
    packages=find_packages(),
    # package_dir={"": "src"},
    # include_package_data=True,
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
    setup_requires=[
        'setuptools_scm',
        'wheel'
    ],
    entry_points={
        "console_scripts": [
            "pse-cli = src.codetrace_pse.cli:main",
        ]
    },
)
