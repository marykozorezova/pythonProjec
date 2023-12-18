import yaml

from checkers import ssh_checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:

    def test_step1(self, make_bad_arx):
        result1 = ssh_checkout_negative("0.0.0.0", "user2", "2222",
                                        'cd {}; 7z e bad_arx2.7z -o/{} -y'.format(data['folder_out'],
                                                                                  data['folder_ext']), 'ERROR')
        assert result1, 'test1 FAIL'

    def test_step2(self):
        assert ssh_checkout_negative("0.0.0.0", "user2", "2222", 'cd{}; 7z t bad_arx2.7z'.format(data['folder_out']),
                                     'ERROR'), 'test2 FAIL'
