import subprocess


def vcs_version():
    return subprocess.check_output(['hg', 'log', '-r', 'limit(.::, 1)', '--template', '{latesttag}.{latesttagdistance}'])

if __name__ == '__main__':
    print '__version__ ="%s"' % vcs_version()
