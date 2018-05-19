import os
import sys


def parse_arguments(arguments):
    parsed_command = {
        'set_update': False,
        'get_update': False,
        'install_update': False,
        'set_upgrade': False,
        'get_upgrade': False,
        'install_upgrade': False,
        'set_dist-upgrade': False,
        'get_dist-upgrade': False,
        'install_dist-upgrade': False,
        'set_install': False,
        'get_install': False,
        'install_install': False
    }

    if '--help' in arguments or '-h' in arguments:
        display_help_menu()
        sys.exit(0)

    if arguments[0] not in parsed_command:
        raise ValueError("You have entered an invalid command, please use --help for correct syntax")

    parsed_command[arguments[0]] = True

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
    usage: python3 apt-py [command] [space separated package list if needed]
    
    Command options:
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


def main(command):
    pass


if __name__ == '__main__':
    arguments = sys.argv[1:]
    command = parse_arguments(arguments)
    main(command)
