import requests

class TestCreateJokeCategory:

    url = "https://api.chucknorris.io/jokes"

    def get_categories(self, expected_status_code):
        # получаем список всех категорий и проверяем статус код
        path_category = '/categories'
        url_category = self.url + path_category

        result = requests.get(url_category)

        print(f'Получение списка категорий: {url_category}')
        print(f'Статус-код: {result.status_code}')
        assert result.status_code == expected_status_code
        print('Статус-код корректен')

        categories = result.json()
        print('Список всех категорий: ', categories)
        return categories

    def get_joke_by_category(self, category):
        #Извлекает одну случайную шутку для данной категории.
        path_random_joke = '/random'
        params = {'category': category}
        url_joke = self.url + path_random_joke

        print(f'\nПолучение шутки из категории: ')
        result = requests.get(url_joke, params=params)
        result.raise_for_status()

        joke_data = result.json()
        # API возвращает значение шутки в поле 'value'.
        return joke_data.get('value')

    def print_jokes_for_all_categories(self):
    #выводим по одной шутке для каждой доступной категории.
    #вызываем get_categories, чтобы получить список категорий.
        categories = self.get_categories(200)

        print("\n--- Получение по одной шутке из каждой категории ---")
        for category in categories:
            joke = self.get_joke_by_category(category)
            print(f"\nКатегория '{category}':")
            if joke:
                print(f"Шутка: {joke}")
            else:
                print("Шутка не найдена.")


start = TestCreateJokeCategory()
start.print_jokes_for_all_categories()
print('Тест прошел успешно')
