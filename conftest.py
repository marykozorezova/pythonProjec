import random
import string

import yaml
import pytest
from checkers import ssh_checkout
from file import upload_files
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope='module')
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        'mkdir -p {} {} {} {}.'.format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                       data['folder_ext2']), "")


@pytest.fixture(autouse=True, scope='class')
def make_files():
    list_off_file = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "2222",
                        'cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock'.format(data['folder_in'],
                                                                                               filename, data['bs']),
                        ""):
            list_off_file.append(filename)
    return list_off_file


@pytest.fixture(autouse=True, scope='module')
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        'rm -rf {}/* {}/* {}/* {}/*'.format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                            data['folder_ext2']), "")


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "2222",
                 'cd {}; 7z a {}/bad_arx'.format(data['folder_in'], data['folder_out']),
                 "Everything is Ok")
    ssh_checkout("0.0.0.0", "user2", "2222",
                 'truncate -s 1 {}/bad_arx'.format(data['folder_out']),
                 "")


@pytest.fixture(autouse=True, scope='module')
def deploy():
    res = []
    upload_files('0.0.0.0', "user2", "2222", "/home/user/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | sudo -S dpkg -i /home/user2/p7zip-full.deb", 'Настраивается пакет'))
    res.append(ssh_checkout("0.0.0.0", "user2", '2222',
                            "echo '2222' | sudo -S dpkg -s dpkg -s p7zip-full" "Status: install ok installed"))
    return all(res)

# @pytest.fixture(autouse=True, scope='module')
# def start_time():
#     return datetime.now().strftime("%Y-@m-%d %H:%M:%S")
#
# def safe_log(name, starttime):
#     with open(name, 'w') as f:
#         f.write(ssh_get("0.0.0.0", "user2", "2222", "journalctl --since {}".format(starttime))

