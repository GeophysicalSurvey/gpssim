from setuptools import setup
import subprocess

setup(
    name = 'gpssim',
    version = subprocess.check_output(['hg', 'log', '-r', 'limit(.::, 1)', '--template', '{latesttag}.{latesttagdistance}']),
    description = 'A Python GPS simulation library',
    author = 'Wei Li Jiang',
    author_email = 'wjiang87@gmail.com',
    url = 'https://bitbucket.org/wjiang/gpssim',
    keywords = ['gps', 'nmea', 'simulator'],
    install_requires=["pySerial>=2.5-rc2", "geographiclib"],
    test_suite="tests",    
    packages=["gpssim"]
)