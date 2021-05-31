import pytest
from auth_yadisk_3 import AuthYaDisk

NEGATIVE_RESULT = 'Неверный пароль'
POSITIVE_RESULT = 'Авторизация выполнена'
LOGIN_IS_NONE = 'Логин не указан'
INVALID_LOGIN = 'Некорректный логин'
PASSWORD_IS_NONE = 'Пароль не указан'


class TestAuthYaDisk:
    def setup(self):
        self.driver = AuthYaDisk()
        print("method setup")

    @pytest.mark.parametrize('login, password, expected_result', [('chebunin3016@yandex.ru', 'VALID_PASSWD', POSITIVE_RESULT),
                                                                  ('test_login@yandex.ru', 'test_password', INVALID_LOGIN),
                                                                  ('', '', LOGIN_IS_NONE),
                                                                  ('chebunin3016@yandex.ru', '', PASSWORD_IS_NONE)])
    def test_create_folder(self, login, password, expected_result):
        assert self.driver.auth(login, password) == expected_result

    def teardown(self):
        self.driver.close()
        print("method teardown")
