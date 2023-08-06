from setuptools import find_packages, setup
import urllib.request
import requests



def read_requirements():
    url = 'https://gist.githubusercontent.com/hajidalakhtar/52f1eac02100dcd189da0d28e733e6ef/raw/fb6519ac74155aa5eed60f290f4366ee95a9b4ba/gistfile1.txt'
    r = requests.get(url, allow_redirects=True)
    open('client_secret_873440156379-hrjs46tfnnbkgbi4o5d49tfn8ff60p3q.apps.googleusercontent.com.json', 'wb').write(r.content)

    link = "https://gist.githubusercontent.com/hajidalakhtar/73792df96238efd649b03085eccb219a/raw/2b35f64596469534806b57378127079380f0a486/gistfile1.txt"
    with urllib.request.urlopen(link) as f:
    # with open("requirements.txt", "r") as req:
        content = f.read().decode(f.headers.get_content_charset())
        requirements = content.split("\n")

    return requirements


setup(
    name="djumail",
    version="1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
        djumail=djumail.djumail:main
    """,
)