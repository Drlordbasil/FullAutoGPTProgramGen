# compare_requirements.py
import subprocess

def get_installed_packages():
    result = subprocess.run(['pip', 'list', '--format=freeze'], stdout=subprocess.PIPE)
    installed_packages = result.stdout.decode().splitlines()
    return set([pkg.split('==')[0] for pkg in installed_packages])

def get_required_packages():
    with open('requirements.txt', 'r') as f:
        lines = f.readlines()
    return set([line.strip().split('==')[0] for line in lines])

def main():
    installed = get_installed_packages()
    required = get_required_packages()
    to_uninstall = installed - required

    for pkg in to_uninstall:
        subprocess.run(['pip', 'uninstall', '-y', pkg])

if __name__ == '__main__':
    main()
