from setuptools import setup
setup(
    name = 'gpssim',
    py_modules=['gpssim'],
    version = '0.6.0',
    description = 'A Python GPS simulation library',
    author = 'Wei Li Jiang',
    author_email = 'wjiang87@gmail.com',
    url = 'https://bitbucket.org/wjiang/gpssim',
    keywords = ['gps', 'nmea', 'simulator'],
    install_requires=["pySerial>=2.5-rc2", "geographiclib"]
)