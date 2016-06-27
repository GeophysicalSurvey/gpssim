from setuptools import setup

exec open('gpssim/version.py').read()

setup(
    name='gpssim',
    version=__version__,
    description='A Python GPS simulation library',
    author='Wei Li Jiang',
    author_email='wjiang87@gmail.com',
    url='https://bitbucket.org/wjiang/gpssim',
    keywords=['gps', 'nmea', 'simulator'],
    install_requires=["pySerial>=2.5-rc2", "geographiclib"],
    entry_points={'gui_scripts': ['gpssim = uilauncher:main']},
    test_suite="tests",
    py_modules=["uilauncher"],
    packages=["gpssim"]
)
