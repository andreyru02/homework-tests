import pytest
from yandex import YaUploader
import config


class TestCreateFolder:

    def setup(self):
        self.token_ya = config.TOKEN_YA_DISK
        self.token_vk = config.TOKEN_VK
        self.yauploader = YaUploader(self.token_ya, self.token_vk, '5.130')
        print("method setup")

    @pytest.mark.parametrize('folder_name, expected_result', [(123123, 123123),
                                                              ('test folder name', 'test folder name'),
                                                              (123123, 409)])
    def test_create_folder(self, folder_name, expected_result):
        assert self.yauploader.create_folder(folder_name) == expected_result

    def teardown(self):
        print("method teardown")
