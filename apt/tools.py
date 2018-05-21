import subprocess
import os


def set_update():
    resp = subprocess.run(['sudo', 'apt-get', 'update', '--print-uris'], stdout=subprocess.PIPE)

    urls = []
    for line in resp.stdout.decode('utf-8').split('\n'):
        raw_url = line.split(' ')[0]
        final_url = raw_url.replace("'", "")
        if final_url:
            urls.append(final_url.strip())

    update_signature_file = os.path.join(os.getcwd(), 'signatures', 'update_sig.txt')

    with open(update_signature_file, 'w') as sig_file:
        sig_file.write(urls.pop(0))
        for url in urls:
            sig_file.write('\n')
            sig_file.write(url)


def get_update():
    update_signature_file = os.path.join(os.getcwd(), 'signatures', 'update_sig.txt')

    with open(update_signature_file, 'r') as input_sig:
        update_urls = [x.strip() for x in input_sig.readlines()]

    download_dir = os.path.join(os.getcwd(), 'downloads')

    for url in update_urls:
        subprocess.run(['wget', '-O', os.path.join(download_dir, url.split('//')[1].replace('/', '_')), url])

    for file in os.listdir(download_dir):
        file_path = os.path.join(download_dir, file)

        if os.path.getsize(file_path) == 0:
            os.remove(file_path)
            continue

        if '.xz' in file_path:
            subprocess.run(['xz', '--decompress', file_path])


def install_update():
    target_dir = '/var/lib/apt/lists'
    download_dir = os.path.join(os.getcwd(), 'downloads')

    for file in os.listdir(download_dir):
        subprocess.run(['sudo', 'cp', os.path.join(download_dir, file), os.path.join(target_dir, file)])


def set_upgrade():
    pass


def get_upgrade():
    pass


def install_upgrade():
    pass


def set_dist_upgrade():
    pass


def get_dist_upgrade():
    pass


def install_dist_upgrade():
    pass


def set_install():
    pass


def get_install():
    pass


def install_install():
    pass
