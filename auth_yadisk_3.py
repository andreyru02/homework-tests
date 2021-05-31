from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config

LINK = 'https://passport.yandex.ru/auth/'
login_ya = config.LOGIN_YA_DISK
password_ya = config.PASSWORD_YA_DISK


class AuthYaDisk:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def auth(self, login, password):
        try:
            self.driver.get(LINK)  # Переходим по ссылке
            self.driver.find_element_by_id('passp-field-login').send_keys(login)  # Вводим логин
            self.driver.find_element_by_xpath(
                '//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[3]/button').click()  # Клик войти
            # Если поле ввода логина пустое - останавливаем выполнение
            if self.driver.find_element_by_class_name('Textinput-Hint').text == 'Логин не указан':
                return 'Логин не указан'
            elif self.driver.find_element_by_class_name('Textinput-Hint').text == 'Такой логин не подойдет':
                return 'Некорректный логин'
        except NoSuchElementException:
            pass

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'passp-field-passwd')))  # Ожидаем поля для ввода пароля

        try:
            self.driver.find_element_by_id('passp-field-passwd').send_keys(password)  # Вводим пароль
            self.driver.find_element_by_xpath(
                '//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/form/div[3]/button').click()  # Клик войти
            # Если поле ввода логина пустое - останавливаем выполнение
            if self.driver.find_element_by_class_name('Textinput-Hint').text == 'Пароль не указан':
                return 'Пароль не указан'
        except NoSuchElementException:
            pass

        try:
            # Если видим поле "Неверный пароль" - останавливаем выполнение
            if self.driver.find_element_by_class_name('Textinput-Hint').text == 'Неверный пароль':
                return 'Неверный пароль'
        except NoSuchElementException:
            return 'Авторизация выполнена'

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    auth = AuthYaDisk()
    print(auth.auth(login_ya, password_ya))
