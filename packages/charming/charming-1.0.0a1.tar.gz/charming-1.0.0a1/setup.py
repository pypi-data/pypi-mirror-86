import re
from setuptools import setup

with open("src/charming/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

print('*' * 5)
print(version)
print('*' * 5)
setup(
    name="charming",
    version=version,
    install_requires=[
        'pyfiglet >= 0.7.2',
        'Pillow >= 2.7.0',
    ]
)
