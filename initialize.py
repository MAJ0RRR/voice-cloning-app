import os
import sys
import shutil
import subprocess


def create_venv(project_root):
    # path to new venv
    venv_path = os.path.join(project_root, 'venv')

    # create venv
    return os.system('python3.9 -m venv ' + venv_path + ' 2> /dev/null')


def install_requirements(project_root):
    # path to exisitng venv
    venv_path = os.path.join(project_root, 'venv')

    # path to requirements.txt
    req_path = os.path.join(project_root, 'requirements.txt')

    # install requirements
    return os.system(os.path.join(venv_path, 'bin/pip3.9') + ' install -r ' + req_path)


def initialize_directories(project_root):
    # Create all necessary directories

    necessary_directories = ['audiofiles', 'audiofiles/raw', 'audiofiles/splits', 'audiofiles/datasets',
                             'output',
                             'tools',
                             ]

    for nd in necessary_directories:
        path = os.path.join(project_root, nd)
        if not os.path.exists(path):
            os.mkdir(path)


def install_rnnoise(project_root):
    rnnoise_path = os.path.join(project_root, 'tools/rnnoise')

    if os.path.exists(rnnoise_path):
        shutil.rmtree(rnnoise_path)

    commands = [(os.system, 'git clone https://github.com/xiph/rnnoise.git ' + rnnoise_path),
                (os.chdir, rnnoise_path),
                (os.system, 'sh autogen.sh'),
                (os.system, 'sh configure'),
                (os.system, 'make clean'),
                (os.system, 'make rnnoise'),
                (os.chdir, project_root)
                ]

    for command, arg in commands:
        return_value = command(arg)
        if return_value is not None and return_value != 0:
            os.chdir(project_root)
            return return_value, arg

    return 0, None


def initialize():
    # set this to project root
    project_root = os.getcwd()

    # create venv with requirements
    if create_venv(project_root) != 0:
        print('\nPython 3.9 with venv is not installed!')
        sys.exit()

    # install requirements to venv
    if install_requirements(project_root) != 0:
        print('\nErorr while installing requirements')
        sys.exit()

    # create all directories
    initialize_directories(project_root)

    ret_val, failed_command = install_rnnoise(project_root)
    # install rnnoise
    if ret_val != 0:
        print('\nErorr while installing rnnoise')
        sys.exit()

    # print on success
    print('\nInitialized successfully')


def download_models():
    os.system('venv/bin/python download_models.py')


if __name__ == '__main__':
    initialize()
    download_models()
