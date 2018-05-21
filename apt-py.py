import sys
import subprocess
import os
from apt import tools


def parse_arguments(arguments):
    parsed_command = {
        'set_update': [False, tools.set_update],
        'get_update': [False, tools.get_update],
        'install_update': [False, tools.install_update],
        'set_upgrade': [False, tools.set_upgrade],
        'get_upgrade': [False, tools.get_upgrade],
        'install_upgrade': [False, tools.install_upgrade],
        'set_dist-upgrade': [False, tools.set_dist_upgrade],
        'get_dist-upgrade': [False, tools.get_dist_upgrade],
        'install_dist-upgrade': [False, tools.install_dist_upgrade],
        'set_install': [False, tools.set_install],
        'get_install': [False, tools.get_install],
        'install_install': [False, tools.install_install]
    }

    if '--help' in arguments or '-h' in arguments:
        display_help_menu()
        sys.exit(0)

    if arguments[0] not in parsed_command:
        raise ValueError("You have entered an invalid command, please use --help for correct syntax")

    parsed_command[arguments[0]][0] = True

    if arguments[0] in ['set_install', 'get_install', 'install_install']:
        if not arguments[1:]:
            raise ValueError("You did not provide a package list with your package install command."
                             "Please provide a space delimited list")
        for package in arguments[1:]:
            if ',' in package:
                raise ValueError("You appear to have inserted commas into your package list,"
                                 "please use single spaces between packages")

        parsed_command['package_list'] = arguments[1:]

    return parsed_command


def display_help_menu():
    menu = """
    Usage: python3 apt-py [command] [space separated package list if needed]
    
    Command Options:
        set_update: Generates an update signature on your offline system
        get_update: Downloads the package list from the repo on the online system
        install_update: Installs the package list on the offline system to update apt
        set_upgrade: Generates a signature file to download packages for a apt-get upgrade
        get_upgrade: Downloads the packages necessary for an apt-get upgrade
        install_upgrade: Installs the packages necessary for an apt-get upgrade
        set_dist-upgrade: Same as upgrade version, but for apt-get dist-upgrade
        get_dist-upgrade: Same as upgrade version, but for apt-get dist-upgrade
        install_dist-upgrade: Same as upgrade version, but for apt-get dist-upgrade
        set_install: Generates a signature file to install a list of space separated packages
        get_install: Downloads the packages from the install signature file
        install_install: Installs the packages from the install signature file
        
    This tool is designed to be run on a USB drive. 
    
    Place this package on a USB drive to easily do offline updates for an airgapped/offline system. 
    
    Both systems must have Python3 and be apt based upgrade mechanisms.
    
    """

    print(menu)


def clear_cache():
    downloads_dir = os.path.join(os.getcwd(), 'downloads')
    signatures_dir = os.path.join(os.getcwd(), 'signatures')

    sigs = [os.path.join(signatures_dir, x) for x in os.listdir(signatures_dir)]
    downloads = [os.path.join(downloads_dir, x) for x in os.listdir(downloads_dir)]

    files_list = sigs + downloads

    for file_path in files_list:
        subprocess.run(['rm', file_path])


def main(command):

    download_dir = os.path.join(os.getcwd(), 'downloads')
    sig_dir = os.path.join(os.getcwd(), 'sigantures')

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if not os.path.exists(sig_dir):
        os.makedirs(sig_dir)

    if command['set_update'][0] or command['set_upgrade'][0] or command['set_dist-upgrade'][0] or command['set_install'][0]:
        clear_cache()  # If we're doing a set command, we're starting a new operation

    for option in command:
        if command[option][0]:
            command[option][1]()


if __name__ == '__main__':
    arguments = sys.argv[1:]
    command = parse_arguments(arguments)
    main(command)
