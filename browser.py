import pytest
import logging
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from logging_config import setup_logging


@pytest.fixture()
def set_up_browser():
    options = Options()
    options.page_load_strategy = 'normal'
    driver = Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def browser():
    setup_logging()
    # Логирование перед запуском браузера
    logging.info('Запуск браузера')
    
    # Здесь код для запуска браузера
    
    yield browser  # Возвращаем экземпляр браузера для тестов
    
    # Логирование после закрытия браузера
    logging.info('Закрытие браузера')
    # Здесь код для закрытия браузера
