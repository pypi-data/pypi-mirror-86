from setuptools import find_packages, setup
import urllib.request



def read_requirements():
    link = "https://gist.githubusercontent.com/hajidalakhtar/73792df96238efd649b03085eccb219a/raw/2b35f64596469534806b57378127079380f0a486/gistfile1.txt"
    with urllib.request.urlopen(link) as f:
    # with open("requirements.txt", "r") as req:
        content = f.read().decode(f.headers.get_content_charset())
        requirements = content.split("\n")

    return requirements


setup(
    name="djumail",
    version="1.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
        djumail=djumail.djumail:main
    """,
)