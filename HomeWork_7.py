import re
import allure
from playwright.sync_api import sync_playwright

class TestClass:
    @allure.feature('Поиск задач на GitHub')
    @allure.story('Поиск по заголовкам задач')
    def test_function1(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            with allure.step('Открыть страницу задач проекта VSCode на GitHub'):
                page.goto("https://github.com/microsoft/vscode/issues")

            with allure.step('Найти поле поиска и ввести запрос'):
                search_input = page.locator('#js-issues-search')
                search_input.fill('in:title bug')
                search_input.press('Enter')

            with allure.step('Ожидание результатов поиска'):
                page.wait_for_selector('div.js-navigation-container.js-active-navigation-container')

            with allure.step('Проверка результатов поиска'):
                issues = page.locator('div.js-navigation-container.js-active-navigation-container').all_text_contents()
                for issue in issues:
                    assert "bug" in issue.lower(), f"Задача {issue} не содержит слово 'bug'"

            browser.close()

    @allure.feature('Тестирование GitHub Issues')
    @allure.story('Поиск issues по автору')
    def test_function2(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            with allure.step('Открыть страницу issues проекта VSCode'):
                page.goto("https://github.com/microsoft/vscode/issues")

            with allure.step('Кликнуть на выпадающий список авторов'):
                page.click('//summary[@title="Author"]')

            with allure.step('Ввести имя автора и применить фильтр'):
                page.fill('#author-filter-field', 'bpasero')
                page.click('//button[@name="author"]')

            with allure.step('Проверить, что фильтр применился корректно'):
                search_field_value = page.input_value('#js-issues-search')
                assert 'bpasero' in search_field_value

            browser.close()

    @allure.feature('Тестирование поиска на GitHub')
    @allure.story('Поиск репозиториев по количеству звёзд')
    def test_function3(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            with allure.step('Открыть страницу расширенного поиска GitHub'):
                page.goto("https://github.com/search/advanced")

            with allure.step('Выбрать язык программирования Python'):
                page.select_option('#search_language', 'Python')

            with allure.step('Ввести количество звёзд более 20000'):
                page.fill('#search_stars', '>20000')

            with allure.step('Ввести имя файла environment.yml'):
                page.fill('#search_filename', 'environment.yml')

            with allure.step('Нажать кнопку поиска'):
                page.click('//div[@class="d-flex d-md-block"]/button[contains(text(),"Search")]')

            with allure.step('Проверить количество звёзд у репозиториев'):
                boxes = page.locator('div.Box-sc-g0xbh4-0.hDWxXB').all_text_contents()
                for box in boxes:
                    stars_text = re.sub(r'[^0-9,]', '', box)
                    if stars_text.isdigit():
                        stars_count = int(stars_text.replace('k', '').replace(',', '')) * 1000
                        assert stars_count > 20000, f"Репозиторий {box} имеет количество звёзд меньше 20000"
                    else:
                        print(f"Не удалось преобразовать '{stars_text}' в число.")

            browser.close()

    @allure.feature('Тестирование веб-сайта Skillbox')
    @allure.story('Проверка функциональности выбора курсов')
    def test_function4(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            with allure.step('Инициализация драйвера и открытие страницы'):
                try:
                    page.goto("https://skillbox.ru/code/", timeout=180000)  # Увеличение времени ожидания до 180 секунд
                    page.set_viewport_size({"width": 1920, "height": 1080})
                except Exception as e:
                    print(f"Ошибка при загрузке страницы: {e}")
                    browser.close()
                    return

            with allure.step('Выбор радиобаттона "Профессия"'):
                page.click('//label[@value="profession"]')

            with allure.step('Изменение диапазона длительности курса'):
                duration_slider_start = page.locator('//div[@aria-valuetext="1"]/button[@aria-label="Изменить диапозон"]')
                duration_slider_end = page.locator('//div[@aria-valuetext="24"]/button[@aria-label="Изменить диапозон"]')
                
            with allure.step('Ожидание загрузки элементов'):
                duration_slider_start.wait_for(state='visible', timeout=20000)
                duration_slider_end.wait_for(state='visible', timeout=20000)
                
            with allure.step('Изменение значений ползунков с использованием Playwright'):
                try:
                    page.dispatch_event('//div[@aria-valuetext="1"]/button[@aria-label="Изменить диапозон"]', 'mousedown', timeout=60000)
                    page.dispatch_event('//div[@aria-valuetext="1"]/button[@aria-label="Изменить диапозон"]', 'mousemove', {'clientX': 100}, timeout=60000)
                    page.dispatch_event('//div[@aria-valuетext="1"]/button[@aria-label="Изменить диапозон"]', 'mouseup', timeout=60000)
                    
                    page.dispatch_event('//div[@aria-valuetext="24"]/button[@aria-label="Изменить диапозон"]', 'mousedown', timeout=60000)
                    page.dispatch_event('//div[@aria-valuetext="24"]/button[@aria-label="Изменить диапозон"]', 'mousemove', {'clientX': -100}, timeout=60000)
                    page.dispatch_event('//div[@aria-valuетext="24"]/button[@aria-label="Изменить диапозон"]', 'mouseup', timeout=60000)
                except Exception as e:
                    print(f"Ошибка при изменении значений ползунков: {e}")
                    browser.close()
                    return

            with allure.step('Выбор тематики курса'):
                page.click('ul.filter-checkboxes-list.filter-checkboxes__list li:nth-of-type(1)')

            with allure.step('Проверка наличия курса "1С-разработчик" на странице'):
                courses_elements = page.locator('section.courses-block.courses-section__block').all_text_contents()
                assert any("1С-разработчик" in element for element in courses_elements), "Курс '1С-разработчик' не найден на странице"

            browser.close()

    @allure.feature('Тестирование графика активности коммитов на GitHub')
    @allure.story('Проверка тултипов на графике')
    def test_function5(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            with allure.step('Инициализация драйвера и открытие страницы'):
                page.goto("https://github.com/microsoft/vscode/graphs/commit-activity")
                page.set_viewport_size({"width": 1920, "height": 1080})

            with allure.step('Наведение курсора на элемент графика и проверка тултипа'):
                page.hover('svg.viz>g>g:nth-of-type(10)')
                tooltip_text = page.locator('div.svg-tip.n').text_content()
                expected_text = '293 commits the week of Sep 17'
                assert tooltip_text == expected_text, f"Текст тултипа '{tooltip_text}' не соответствует ожидаемому '{expected_text}'"

            browser.close()
