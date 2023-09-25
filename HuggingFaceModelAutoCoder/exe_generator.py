import subprocess

def generate_exe(py_file):
    subprocess.run(["pyinstaller", "--onefile", py_file])
